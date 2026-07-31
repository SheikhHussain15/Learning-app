from src.agents.base import BaseAgent


class ProductionAgent(BaseAgent):
    """Base class for all production agents with output validation."""

    agent_type: str

    def validate_output(self, output: dict, schema: dict) -> bool:
        """Validate agent output against JSON Schema contract."""
        try:
            from jsonschema import validate
            validate(instance=output, schema=schema)
            return True
        except Exception:
            return False

    def make_source_refs(self, chunk_ids: list[str], document_id: str) -> list[dict]:
        """Create source references from chunk IDs."""
        return [{"chunk_id": cid, "document_id": document_id} for cid in chunk_ids]
