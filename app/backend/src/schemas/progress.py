from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class ProgressEventType(StrEnum):
    quiz_completed = "quiz_completed"
    flashcard_reviewed = "flashcard_reviewed"
    chapter_completed = "chapter_completed"
    reading_progress = "reading_progress"
    tutor_used = "tutor_used"
    diagram_interacted = "diagram_interacted"
    revision_completed = "revision_completed"
    document_viewed = "document_viewed"


class ProgressEventInput(BaseModel):
    event_type: ProgressEventType
    document_id: str | None = None
    section_id: str | None = None
    event_data: dict | None = None
    duration: int | None = None


class ProgressEvent(BaseModel):
    id: str
    user_id: str
    event_type: ProgressEventType
    document_id: str | None = None
    section_id: str | None = None
    event_data: dict = {}
    duration: int | None = None
    created_at: datetime


class ProgressSummary(BaseModel):
    total_events: int
    total_study_time: int
    events_by_type: dict[ProgressEventType, int]
    documents_studied: int
    average_daily_time: int


class LearningStreak(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: str
    streak_active: bool


class ProgressEventRequest(BaseModel):
    event_type: ProgressEventType
    document_id: str | None = None
    section_id: str | None = None
    event_data: dict | None = None
    duration: int | None = None


class ProgressEventResponse(BaseModel):
    id: str
    event_type: ProgressEventType
    document_id: str | None = None
    created_at: datetime | None = None


class ProgressSummaryResponse(BaseModel):
    events: list[dict] = []
    total_events: int = 0


class ProgressStatsResponse(BaseModel):
    total_events: int = 0
    total_time: int = 0
    documents_studied: int = 0
    average_score: float = 0.0
