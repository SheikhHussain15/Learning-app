import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, String, UniqueConstraint

from src.core.database import Base


def _utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, nullable=False, index=True)
    agent_type = Column(String, nullable=False)
    params_hash = Column(String, nullable=False)
    output_data = Column(JSON, nullable=False)
    source_refs = Column(JSON, default=list)
    token_usage = Column(JSON, default=dict)
    created_at = Column(DateTime, default=_utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("document_id", "agent_type", "params_hash", name="uq_agent_output_cache"),
    )
