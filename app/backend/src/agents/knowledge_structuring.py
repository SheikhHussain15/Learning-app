import logging

from langfuse import observe
from openai import AsyncOpenAI

from src.agents.production_base import ProductionAgent
from src.agents.registry import create_openai_provider
from src.schemas.agent import ErrorInfo, RequestEnvelope, ResponseEnvelope, TokenUsage
from src.schemas.agent_outputs import KnowledgeStructuringOutput, NodeRelationship, ProcessingNodeData

logger = logging.getLogger(__name__)

STRUCTURING_PROMPT = """Analyze the following text chunks and create a hierarchical document structure.

For each chunk, classify it as:
- "chapter": Top-level document section
- "topic": Mid-level section within a chapter
- "subtopic": Detailed section within a topic

Return a JSON object with:
1. "nodes": List of ProcessingNodeData with node_id, node_type, title, content, parent_id (null for root), position, chunk_ids
2. "relationships": List of NodeRelationship with source_id, target_id, relationship_type ("contains", "related_to", "depends_on")

Text chunks:
{chunks}

Return ONLY valid JSON matching this schema:
{{
  "nodes": [
    {{
      "node_id": "string",
      "node_type": "chapter|topic|subtopic",
      "title": "string",
      "content": "string",
      "parent_id": "string|null",
      "position": 0,
      "chunk_ids": ["string"]
    }}
  ],
  "relationships": [
    {{
      "source_id": "string",
      "target_id": "string",
      "relationship_type": "contains|related_to|depends_on"
    }}
  ]
}}"""


class KnowledgeStructuringAgent(ProductionAgent):
    agent_type: str = "knowledge_structuring"

    @observe(name="agent.knowledge_structuring.invoke", as_type="span")
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
                    ErrorInfo(code="NO_INPUT", message="No chunks provided for structuring", retryable=False)
                )

            chunk_text = "\n\n".join([
                f"[Chunk {c.chunk_id}]: {c.text[:200]}..." for c in chunks[:20]
            ])

            prompt = STRUCTURING_PROMPT.format(chunks=chunk_text)

            provider = create_openai_provider()
            client = AsyncOpenAI(
                api_key=provider.api_key,
                base_url=provider.base_url,
            )

            response = await client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000,
            )

            import json
            result = json.loads(response.choices[0].message.content)

            nodes = [ProcessingNodeData(**n) for n in result.get("nodes", [])]
            relationships = [NodeRelationship(**r) for r in result.get("relationships", [])]

            output = KnowledgeStructuringOutput(
                nodes=nodes,
                relationships=relationships,
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
            logger.exception("KnowledgeStructuringAgent failed: %s", e)
            return self.make_error_response(
                ErrorInfo(code="STRUCTURING_ERROR", message=str(e), retryable=False)
            )
