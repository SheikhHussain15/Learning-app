import enum

from sqlalchemy import JSON, Column, DateTime, Enum, String, Text
from sqlalchemy.sql import func

from src.core.database import Base


class SectionType(enum.StrEnum):
    summary = "summary"
    explanation = "explanation"
    translation = "translation"
    diagram = "diagram"
    quiz = "quiz"
    flashcard = "flashcard"
    revision_notes = "revision_notes"


class SectionStatus(enum.StrEnum):
    not_requested = "not_requested"
    processing = "processing"
    failed = "failed"
    completed = "completed"


class WorkspaceSection(Base):
    __tablename__ = "workspace_sections"

    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False, index=True)
    section_type = Column(Enum(SectionType), nullable=False)
    status = Column(Enum(SectionStatus), nullable=False, default=SectionStatus.not_requested)
    content = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    requested_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = ()
