from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SectionType(StrEnum):
    summary = "summary"
    explanation = "explanation"
    translation = "translation"
    diagram = "diagram"
    quiz = "quiz"
    flashcard = "flashcard"
    revision_notes = "revision_notes"


class SectionStatus(StrEnum):
    not_requested = "not_requested"
    processing = "processing"
    failed = "failed"
    completed = "completed"


class TopicBase(BaseModel):
    id: str
    title: str
    order: int
    chapter_id: str


class ChapterBase(BaseModel):
    id: str
    title: str
    order: int
    topics: list[TopicBase]


class WorkspaceSectionBase(BaseModel):
    id: str
    document_id: str
    section_type: SectionType
    status: SectionStatus
    content: dict[str, Any] | None = None
    error_message: str | None = None
    requested_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class WorkspaceOverview(BaseModel):
    document_id: str
    title: str
    description: str
    metadata: dict[str, Any]
    chapters: list[ChapterBase]
    sections: list[WorkspaceSectionBase]


class SectionRequestResponse(BaseModel):
    section_id: str
    status: SectionStatus = SectionStatus.processing
    message: str


class SectionStatusResponse(BaseModel):
    section_id: str
    status: SectionStatus
    progress: float = Field(ge=0, le=100)
    error_message: str | None = None


class SectionContentResponse(BaseModel):
    section_id: str
    section_type: SectionType
    content: dict[str, Any]
    metadata: dict[str, Any] = {}
