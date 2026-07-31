import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, Integer, String

from src.core.database import Base


def _utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


class AgentType(enum.StrEnum):
    echo = "echo"
    document_processing = "document_processing"
    knowledge_structuring = "knowledge_structuring"
    summary = "summary"
    explanation = "explanation"
    translation = "translation"
    diagram = "diagram"
    quiz = "quiz"
    revision = "revision"
    progress = "progress"
    recommendation = "recommendation"


class AgentStatus(enum.StrEnum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    orchestration_id = Column(String, nullable=True, index=True)
    agent_type = Column(Enum(AgentType), nullable=False)
    document_id = Column(String, nullable=True)
    node_ids = Column(JSON, default=list)
    trace_id = Column(String, nullable=False, index=True)
    request_envelope = Column(JSON, nullable=False)
    response_envelope = Column(JSON, nullable=True)
    status = Column(Enum(AgentStatus), nullable=False, default=AgentStatus.queued)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=6)
    errors = Column(JSON, default=list)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    model_used = Column(String, nullable=True)
    fallback_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)
