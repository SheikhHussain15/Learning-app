from abc import ABC, abstractmethod

from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage


class BaseAgent(ABC):
    agent_type: str

    @abstractmethod
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        ...

    def validate_envelope(self, envelope: RequestEnvelope) -> ErrorInfo | None:
        if not envelope.document_id:
            return ErrorInfo(code="INVALID_REQUEST", message="document_id is required", retryable=False)
        if not envelope.trace_id:
            return ErrorInfo(code="INVALID_REQUEST", message="trace_id is required", retryable=False)
        return None

    def make_error_response(self, error: ErrorInfo) -> ResponseEnvelope:
        return ResponseEnvelope(
            status="error",
            output={},
            source_refs=[],
            usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            error=error,
        )
