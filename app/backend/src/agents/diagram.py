import json
import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import DiagramData, DiagramOutput

logger = logging.getLogger(__name__)

DIAGRAM_PROMPT = """Generate a diagram representing the relationships and concepts in the following text.

Use Mermaid syntax for the diagram. Create flowcharts, concept maps, or sequence diagrams as appropriate.

Text content:
{chunks}

Return ONLY valid JSON:
{{
  "diagrams": [
    {{
      "diagram_type": "mermaid",
      "diagram_data": "graph TD\\n    A[Concept1] --> B[Concept2]\\n    B --> C[Concept3]",
      "description": "string",
      "source_chunk_ids": ["string"]
    }}
  ]
}}"""


class DiagramAgent(ProductionAgent):
    agent_type: str = "diagram"

    @observe(name="agent.diagram.invoke", as_type="span")
    async def invoke(self, envelope: RequestEnvelope) -> ResponseEnvelope:
        validation_error = self.validate_envelope(envelope)
        if validation_error:
            return self.make_error_response(validation_error)

        try:
            chunks = []
            if envelope.context and envelope.context.chunks:
                chunks = envelope.context.chunks

            if not chunks:
                return self.make_error_response(
                    ErrorInfo(code="NO_INPUT", message="No chunks provided for diagram generation", retryable=False)
                )

            chunk_text = "\n\n".join([
                f"[{c.chunk_id}]: {c.text}" for c in chunks[:10]
            ])

            prompt = DIAGRAM_PROMPT.format(chunks=chunk_text)

            provider = create_openai_provider()
            client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)

            diagrams = [DiagramData(**d) for d in result.get("diagrams", [])]
            output = DiagramOutput(diagrams=diagrams)

            source_refs = self.make_source_refs(
                [c.chunk_id for c in chunks],
                envelope.document_id,
            )

            usage = response.usage
            return ResponseEnvelope(
                status="success",
                output=output.model_dump(),
                source_refs=source_refs,
                usage=TokenUsage(
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                ),
            )

        except Exception as e:
            logger.exception("DiagramAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="DIAGRAM_ERROR", message=str(e), retryable=False)
            )
