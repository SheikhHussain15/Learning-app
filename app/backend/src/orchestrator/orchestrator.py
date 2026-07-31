import asyncio
import contextlib
import logging
import random
import uuid
from datetime import UTC, datetime

from langfuse import get_client, observe

from src.agents.registry import get_model_config
from src.core.database import SessionLocal
from src.models.agent_run import AgentRun, AgentStatus, AgentType
from src.orchestrator.retry import NonRetryableError, RetryableError
from src.orchestrator.router import get_agent
from src.orchestrator.state_machine import InvalidTransitionError, validate_transition
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage

logger = logging.getLogger(__name__)


def _exponential_backoff(attempt: int, base: float = 1.0, max_delay: float = 30.0) -> float:
    delay = min(base * (2 ** (attempt - 1)), max_delay)
    jitter = random.uniform(0, delay * 0.25)
    return delay + jitter


async def _retry_invoke(agent, envelope: RequestEnvelope, max_attempts: int) -> tuple[ResponseEnvelope | None, list[dict], int, bool]:
    errors = []
    for attempt_num in range(1, max_attempts + 1):
        try:
            response = await agent.invoke(envelope)
            return response, errors, attempt_num, False
        except NonRetryableError as e:
            errors.append({
                "attempt": attempt_num, "code": e.code, "message": str(e),
                "timestamp": datetime.now(UTC).replace(tzinfo=None).isoformat(),
            })
            logger.warning("NonRetryableError on attempt %d: %s", attempt_num, e)
            return None, errors, attempt_num, True
        except RetryableError as e:
            errors.append({
                "attempt": attempt_num, "code": e.code, "message": str(e),
                "timestamp": datetime.now(UTC).replace(tzinfo=None).isoformat(),
            })
            logger.warning("RetryableError attempt %d/%d: %s", attempt_num, max_attempts, e)
            if attempt_num < max_attempts:
                delay = _exponential_backoff(attempt_num)
                logger.info("Backoff %.2fs before retry %d", delay, attempt_num + 1)
                await asyncio.sleep(delay)
    return None, errors, max_attempts, False


class Orchestrator:
    @observe(name="orchestrator.dispatch", as_type="span")
    async def dispatch(
        self,
        agent_type: AgentType,
        envelope: RequestEnvelope,
        db_session=None,
    ) -> AgentRun:
        run_id = str(uuid.uuid4())
        close_session = False
        if db_session is None:
            db_session = SessionLocal()
            close_session = True

        try:
            langfuse = get_client()
            langfuse.update_current_trace(
                name=f"agent.{agent_type.value}.invoke",
                metadata={"run_id": run_id, "agent_type": agent_type.value},
            )
        except Exception:
            pass

        agent_run = AgentRun(
            id=run_id,
            agent_type=agent_type,
            document_id=envelope.document_id,
            node_ids=envelope.node_ids,
            trace_id=envelope.trace_id,
            request_envelope=envelope.model_dump(),
            status=AgentStatus.queued,
            retry_count=0,
            max_retries=6,
            errors=[],
            created_at=datetime.now(UTC).replace(tzinfo=None),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
        )

        try:
            db_session.add(agent_run)
            db_session.commit()

            self._transition(agent_run, AgentStatus.running, db_session)
            agent_run.started_at = datetime.now(UTC).replace(tzinfo=None)
            db_session.commit()

            model_config = get_model_config(agent_type)
            agent = get_agent(agent_type)
            if agent is None:
                raise ValueError(f"No agent registered for {agent_type.value}")

            all_errors: list[dict] = []
            response: ResponseEnvelope | None = None
            fallback_used = False
            model_used = model_config.primary_model_id
            total_attempts = 0

            response, errors, attempts, non_retryable = await _retry_invoke(agent, envelope, 3)
            all_errors.extend(errors)
            total_attempts += attempts

            if response is None and not non_retryable:
                fallback_used = True
                model_used = model_config.fallback_model_id
                logger.info(
                    "Primary exhausted for %s, switching to fallback %s",
                    agent_type.value, model_config.fallback_model_id,
                )
                response, errors, attempts, _ = await _retry_invoke(agent, envelope, 3)
                all_errors.extend(errors)
                total_attempts += attempts

            agent_run.retry_count = total_attempts - 1
            agent_run.errors = all_errors

            if response is None:
                last_error = all_errors[-1] if all_errors else {
                    "attempt": 0, "code": "UNKNOWN", "message": "All retries exhausted",
                    "timestamp": datetime.now(UTC).replace(tzinfo=None).isoformat(),
                }
                agent_run.response_envelope = ResponseEnvelope(
                    status="error",
                    output={},
                    source_refs=[],
                    usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                    error=ErrorInfo(
                        code=last_error["code"],
                        message=last_error["message"],
                        retryable=False,
                    ),
                ).model_dump()
                self._transition(agent_run, AgentStatus.failed, db_session)
            else:
                agent_run.response_envelope = response.model_dump()
                if response.status == "error":
                    self._transition(agent_run, AgentStatus.failed, db_session)
                else:
                    self._transition(agent_run, AgentStatus.succeeded, db_session)

            agent_run.model_used = model_used
            agent_run.fallback_used = fallback_used
            agent_run.completed_at = datetime.now(UTC).replace(tzinfo=None)
            if agent_run.started_at:
                agent_run.duration_ms = int(
                    (agent_run.completed_at - agent_run.started_at).total_seconds() * 1000
                )
            db_session.commit()

            logger.info(
                "AgentRun %s completed: %s -> %s (model=%s, fallback=%s, retries=%d, duration=%dms)",
                run_id, agent_type.value, agent_run.status.value,
                model_used, fallback_used, agent_run.retry_count, agent_run.duration_ms or 0,
            )

            return agent_run

        except Exception as e:
            logger.exception("Orchestrator dispatch failed for run %s: %s", run_id, e)
            if agent_run:
                agent_run.response_envelope = ResponseEnvelope(
                    status="error",
                    output={},
                    source_refs=[],
                    usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                    error=ErrorInfo(code="ORCHESTRATION_ERROR", message=str(e), retryable=False),
                ).model_dump()
                agent_run.completed_at = datetime.now(UTC).replace(tzinfo=None)
                if agent_run.started_at:
                    agent_run.duration_ms = int(
                        (agent_run.completed_at - agent_run.started_at).total_seconds() * 1000
                    )
                with contextlib.suppress(InvalidTransitionError):
                    self._transition(agent_run, AgentStatus.failed, db_session)
                db_session.commit()
                return agent_run
            raise
        finally:
            if close_session:
                db_session.close()

    def _transition(self, run: AgentRun, new_status: AgentStatus, db_session) -> None:
        validate_transition(run.status, new_status)
        old_status = run.status
        run.status = new_status
        run.updated_at = datetime.now(UTC).replace(tzinfo=None)
        logger.info("AgentRun %s state: %s -> %s", run.id, old_status.value, new_status.value)


_orchestrator = Orchestrator()


def get_orchestrator() -> Orchestrator:
    return _orchestrator
