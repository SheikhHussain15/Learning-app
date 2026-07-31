import enum

from sqlalchemy import JSON, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class ProgressEventType(enum.StrEnum):
    quiz_completed = "quiz_completed"
    flashcard_reviewed = "flashcard_reviewed"
    chapter_completed = "chapter_completed"
    reading_progress = "reading_progress"
    tutor_used = "tutor_used"
    diagram_interacted = "diagram_interacted"
    revision_completed = "revision_completed"
    document_viewed = "document_viewed"


EventType = ProgressEventType


class ProgressEvent(Base):
    __tablename__ = "progress_events"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    event_type = Column(Enum(ProgressEventType), nullable=False)
    document_id = Column(String, nullable=True, index=True)
    section_id = Column(String, nullable=True)
    event_data = Column(JSON, nullable=True, default={})
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        {"schema": "learning"} if hasattr(Base, '__bind_key__') else {},
    )
