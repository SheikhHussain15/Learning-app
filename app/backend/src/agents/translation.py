import json
import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import NodeTranslation, TranslationOutput

logger = logging.getLogger(__name__)

TRANSLATION_PROMPT = """Translate the following text chunks to {target_language}.
Maintain the original meaning and terminology as closely as possible.

Text chunks:
{chunks}

Return ONLY valid JSON:
{{
  "translations": [
    {{
      "node_id": "string",
      "translated_text": "string",
      "source_chunk_ids": ["string"]
    }}
  ],
  "source_language": "en",
  "target_language": "{target_language}"
}}"""


class TranslationAgent(ProductionAgent):
    agent_type: str = "translation"

    @observe(name="agent.translation.invoke", as_type="span")
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
                    ErrorInfo(code="NO_INPUT", message="No chunks provided for translation", retryable=False)
                )

            target_language = envelope.agent_params.get("target_language", "Spanish")

            chunk_text = "\n\n".join([
                f"[{c.chunk_id}]: {c.text}" for c in chunks[:15]
            ])

            prompt = TRANSLATION_PROMPT.format(chunks=chunk_text, target_language=target_language)

            provider = create_openai_provider()
            client = AsyncOpenAI(api_key=provider.api_key, base_url=provider.base_url)

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)

            translations = [NodeTranslation(**t) for t in result.get("translations", [])]
            output = TranslationOutput(
                translations=translations,
                source_language=result.get("source_language", "en"),
                target_language=target_language,
            )

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
            logger.exception("TranslationAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="TRANSLATION_ERROR", message=str(e), retryable=False)
            )
