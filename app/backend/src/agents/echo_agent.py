from langfuse import observe

from src.agents.base import BaseAgent
from src.schemas.agent import RequestEnvelope, ResponseEnvelope, TokenUsage


class EchoAgent(BaseAgent):
    agent_type: str = "echo"

    @observe(name="agent.echo.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        return ResponseEnvelope(
            status="success",
            output={
                "echoed_document_id": envelope.document_id,
                "echoed_node_ids": envelope.node_ids,
                "echoed_trace_id": envelope.trace_id,
                "received_agent_params": envelope.agent_params,
            },
            source_refs=[],
            usage=TokenUsage(prompt_tokens=50, completion_tokens=20, total_tokens=70),
            error=None,
        )
