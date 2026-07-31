from src.agents.base import BaseAgent
from src.orchestrator.retry import RetryableError
from src.schemas.agent import RequestEnvelope, ResponseEnvelope, TokenUsage


class FailingAgent(BaseAgent):
    agent_type: str = "failing"

    def __init__(self, fail_count: int = 0, fail_permanently: bool = False):
        self._invoke_count = 0
        self._fail_count = fail_count
        self._fail_permanently = fail_permanently

    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        self._invoke_count += 1

        if self._fail_permanently:
            raise RetryableError("Permanent failure for testing", code="TEST_FAILURE")

        if self._invoke_count <= self._fail_count:
            raise RetryableError(
                f"Simulated failure (attempt {self._invoke_count})",
                code="TEST_FAILURE",
            )

        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        return ResponseEnvelope(
            status="success",
            output={
                "echoed_document_id": envelope.document_id,
                "echoed_node_ids": envelope.node_ids,
                "echoed_trace_id": envelope.trace_id,
            },
            source_refs=[],
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
            error=None,
        )
