import hashlib
import json
import logging

from src.core.database import SessionLocal
from src.models.agent_output import AgentOutput

logger = logging.getLogger(__name__)


def compute_params_hash(agent_params: dict) -> str:
    """Compute deterministic SHA256 hash of agent parameters."""
    serialized = json.dumps(agent_params, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


def get_cached_output(document_id: str, agent_type: str, agent_params: dict) -> dict | None:
    """Look up cached agent output by (document_id, agent_type, params_hash)."""
    params_hash = compute_params_hash(agent_params)
    db = SessionLocal()
    try:
        result = db.query(AgentOutput).filter(
            AgentOutput.document_id == document_id,
            AgentOutput.agent_type == agent_type,
            AgentOutput.params_hash == params_hash,
        ).first()
        if result:
            logger.info("Cache hit for %s/%s (hash=%s)", document_id, agent_type, params_hash[:8])
            return result.output_data
        logger.info("Cache miss for %s/%s (hash=%s)", document_id, agent_type, params_hash[:8])
        return None
    finally:
        db.close()


def store_output(
    document_id: str,
    agent_type: str,
    agent_params: dict,
    output_data: dict,
    source_refs: list[dict] | None = None,
    token_usage: dict | None = None,
) -> AgentOutput:
    """Store agent output in cache."""
    params_hash = compute_params_hash(agent_params)
    db = SessionLocal()
    try:
        existing = db.query(AgentOutput).filter(
            AgentOutput.document_id == document_id,
            AgentOutput.agent_type == agent_type,
            AgentOutput.params_hash == params_hash,
        ).first()

        if existing:
            existing.output_data = output_data
            existing.source_refs = source_refs or []
            existing.token_usage = token_usage or {}
            db.commit()
            db.refresh(existing)
            logger.info("Updated cached output for %s/%s", document_id, agent_type)
            return existing

        output = AgentOutput(
            document_id=document_id,
            agent_type=agent_type,
            params_hash=params_hash,
            output_data=output_data,
            source_refs=source_refs or [],
            token_usage=token_usage or {},
        )
        db.add(output)
        db.commit()
        db.refresh(output)
        logger.info("Stored new output for %s/%s (hash=%s)", document_id, agent_type, params_hash[:8])
        return output
    finally:
        db.close()


def invalidate_cache(document_id: str, agent_type: str | None = None) -> int:
    """Delete cached outputs for a document. Returns count of deleted entries."""
    db = SessionLocal()
    try:
        query = db.query(AgentOutput).filter(AgentOutput.document_id == document_id)
        if agent_type:
            query = query.filter(AgentOutput.agent_type == agent_type)
        count = query.count()
        query.delete()
        db.commit()
        logger.info("Invalidated %d cached outputs for document %s", count, document_id)
        return count
    finally:
        db.close()
