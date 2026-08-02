import json
import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import ConceptExplanation, ExplanationOutput

logger = logging.getLogger(__name__)

EXPLANATION_PROMPT = """Explain the key concepts from the following text chunks. For each concept:
1. Provide a clear explanation
2. Give 2-3 examples
3. Rate complexity as "beginner", "intermediate", or "advanced"

Text chunks:
{chunks}

Return ONLY valid JSON:
{{
  "explanations": [
    {{
      "concept": "string",
      "explanation": "string",
      "examples": ["string"],
      "complexity_level": "beginner|intermediate|advanced",
      "source_chunk_ids": ["string"]
    }}
  ]
}}"""


class ExplanationAgent(ProductionAgent):
    agent_type: str = "explanation"

    @observe(name="agent.explanation.invoke", as_type="span")
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
                    ErrorInfo(code="NO_INPUT", message="No chunks provided for explanation", retryable=False)
                )

            chunk_text = "\n\n".join([
                f"[{c.chunk_id}]: {c.text}" for c in chunks[:15]
            ])

            prompt = EXPLANATION_PROMPT.format(chunks=chunk_text)

            provider = create_openai_provider()
            client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000,
            )

            result = json.loads(response.choices[0].message.content)

            explanations = [ConceptExplanation(**e) for e in result.get("explanations", [])]
            output = ExplanationOutput(explanations=explanations)

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
            logger.exception("ExplanationAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="EXPLANATION_ERROR", message=str(e), retryable=False)
            )
