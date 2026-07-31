import pytest
from src.orchestrator.retry import (
    RetryableError,
    NonRetryableError,
    classify_error,
)
from src.orchestrator.orchestrator import Orchestrator
from src.models.agent_run import AgentType, AgentStatus
from src.schemas.agent import RequestEnvelope
from src.orchestrator.router import register_agent
from src.agents.failing_agent import FailingAgent


class TestRetryClassification:
    def test_retryable_http_codes(self):
        for code in [429, 502, 503, 504]:
            exc = classify_error(code, "upstream error")
            assert isinstance(exc, RetryableError)

    def test_non_retryable_http_codes(self):
        for code in [400, 401, 403, 404]:
            exc = classify_error(code, "bad request")
            assert isinstance(exc, NonRetryableError)

    def test_retryable_timeout(self):
        exc = classify_error(None, "timeout error")
        assert isinstance(exc, RetryableError)

    def test_retryable_rate_limit(self):
        exc = classify_error(None, "rate limit exceeded")
        assert isinstance(exc, RetryableError)

    def test_non_retryable_invalid_contract(self):
        exc = classify_error(None, "invalid contract")
        assert isinstance(exc, NonRetryableError)

    def test_unknown_is_retryable(self):
        exc = classify_error(None, "unknown error")
        assert isinstance(exc, RetryableError)


class TestFailingAgent:
    @pytest.mark.asyncio
    async def test_retryable_error_triggers_backoff(self, mock_langfuse, db):
        failing_agent = FailingAgent(fail_count=1)
        register_agent(AgentType.echo, failing_agent)

        orchestrator = Orchestrator()
        envelope = RequestEnvelope(
            document_id="doc-retry-1",
            node_ids=[],
            trace_id="trace-retry-1",
        )

        agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
        assert agent_run.status == AgentStatus.succeeded
        assert agent_run.retry_count > 0

    @pytest.mark.asyncio
    async def test_max_retries_exhausted_fails(self, mock_langfuse, db):
        failing_agent = FailingAgent(fail_permanently=True)
        register_agent(AgentType.echo, failing_agent)

        orchestrator = Orchestrator()
        envelope = RequestEnvelope(
            document_id="doc-retry-2",
            node_ids=[],
            trace_id="trace-retry-2",
        )

        agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
        assert agent_run.status == AgentStatus.failed
        assert agent_run.retry_count > 0

    @pytest.mark.asyncio
    async def test_fallback_model_invoked(self, mock_langfuse, db):
        failing_agent = FailingAgent(fail_count=3)
        register_agent(AgentType.echo, failing_agent)

        orchestrator = Orchestrator()
        envelope = RequestEnvelope(
            document_id="doc-fallback-1",
            node_ids=[],
            trace_id="trace-fallback-1",
        )

        agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
        assert agent_run.status == AgentStatus.succeeded
        assert agent_run.fallback_used is True

    @pytest.mark.asyncio
    async def test_non_retryable_failure_no_retries(self, mock_langfuse, db):
        class ImmediateFailAgent(FailingAgent):
            async def invoke(self, envelope):
                from src.orchestrator.retry import NonRetryableError
                raise NonRetryableError("Invalid request", code="INVALID_REQUEST")

        agent = ImmediateFailAgent()
        register_agent(AgentType.echo, agent)

        orchestrator = Orchestrator()
        envelope = RequestEnvelope(
            document_id="doc-nonretry-1",
            node_ids=[],
            trace_id="trace-nonretry-1",
        )

        agent_run = await orchestrator.dispatch(AgentType.echo, envelope, db_session=db)
        assert agent_run.status == AgentStatus.failed
