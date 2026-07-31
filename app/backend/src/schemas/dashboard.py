from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EventType(StrEnum):
    quiz_completed = "quiz_completed"
    flashcard_reviewed = "flashcard_reviewed"
    chapter_completed = "chapter_completed"
    reading_progress = "reading_progress"
    tutor_used = "tutor_used"
    diagram_interacted = "diagram_interacted"
    revision_completed = "revision_completed"


class ActivityItem(BaseModel):
    id: str
    event_type: EventType
    document_id: str
    document_title: str
    description: str
    created_at: datetime


class LearningStatistics(BaseModel):
    total_study_time: int
    documents_studied: int
    quizzes_completed: int
    average_quiz_score: float
    flashcards_reviewed: int
    tutor_conversations: int


class DocumentProgress(BaseModel):
    document_id: str
    title: str
    progress: float = Field(ge=0, le=100)
    last_studied: datetime


class StudyProgress(BaseModel):
    documents: list[DocumentProgress]
    overall_progress: float = Field(ge=0, le=100)


class LearningStreak(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: str
    streak_active: bool


class Recommendation(BaseModel):
    id: str
    recommendation_type: str
    document_id: str | None = None
    title: str
    description: str
    reason: str
    priority: int = Field(ge=1, le=10)


class RecentlyViewedDocument(BaseModel):
    document_id: str
    title: str
    progress: float = Field(ge=0, le=100)
    last_viewed: datetime


class DashboardData(BaseModel):
    recent_activity: list[ActivityItem]
    statistics: LearningStatistics
    progress: StudyProgress
    streak: LearningStreak
    recommendations: list[Recommendation]
    recently_viewed: list[RecentlyViewedDocument]
