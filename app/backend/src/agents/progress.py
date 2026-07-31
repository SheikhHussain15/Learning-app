import logging

from langfuse import observe

from src.agents.production_base import ProductionAgent
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import ProgressOutput, UserProgressSummary
from src.services.progress_service import get_user_progress_summary, record_event

logger = logging.getLogger(__name__)


class ProgressAgent(ProductionAgent):
    agent_type: str = "progress"

    @observe(name="agent.progress.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        try:
            event_type = envelope.agent_params.get("event_type")
            if not event_type:
                return self.make_error_response(
                    ErrorInfo(code="MISSING_PARAM", message="event_type is required", retryable=False)
                )

            event_data = envelope.agent_params.get("event_data", {})
            user_id = envelope.agent_params.get("user_id", "anonymous")

            record_event(
                user_id=user_id,
                event_type=event_type,
                document_id=envelope.document_id,
                event_data=event_data,
            )

            progress = get_user_progress_summary(user_id)

            output = ProgressOutput(
                events_recorded=1,
                user_progress=UserProgressSummary(**progress),
            )

            return ResponseEnvelope(
                status="success",
                output=output.model_dump(),
                source_refs=[],
                usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )

        except Exception as e:
            logger.exception("ProgressAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="PROGRESS_ERROR", message=str(e), retryable=False)
            )
