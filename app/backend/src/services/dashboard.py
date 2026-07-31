
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.progress_event import ProgressEvent, ProgressEventType
from src.schemas.dashboard import (
    ActivityItem,
    DashboardData,
    LearningStatistics,
    LearningStreak,
    RecentlyViewedDocument,
    StudyProgress,
)


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_data(self, user_id: str) -> DashboardData:
        return DashboardData(
            recent_activity=self.get_recent_activity(user_id),
            statistics=self.get_statistics(user_id),
            progress=self.get_study_progress(user_id),
            streak=self.get_learning_streak(user_id),
            recommendations=[],
            recently_viewed=self.get_recently_viewed(user_id),
        )

    def get_recent_activity(self, user_id: str, limit: int = 10) -> list[ActivityItem]:
        events = (
            self.db.query(ProgressEvent)
            .filter(ProgressEvent.user_id == user_id)
            .order_by(ProgressEvent.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            ActivityItem(
                id=event.id,
                event_type=event.event_type,
                document_id=event.document_id or "",
                document_title="Document",
                description=self._get_event_description(event),
                created_at=event.created_at,
            )
            for event in events
        ]

    def get_statistics(self, user_id: str) -> LearningStatistics:
        stats = (
            self.db.query(
                func.count(ProgressEvent.id).label("total_events"),
                func.coalesce(func.sum(ProgressEvent.duration), 0).label("total_time"),
                func.count(func.distinct(ProgressEvent.document_id)).label("documents"),
            )
            .filter(ProgressEvent.user_id == user_id)
            .first()
        )

        quiz_count = (
            self.db.query(func.count(ProgressEvent.id))
            .filter(
                ProgressEvent.user_id == user_id,
                ProgressEvent.event_type == ProgressEventType.quiz_completed,
            )
            .scalar()
        )

        return LearningStatistics(
            total_study_time=stats.total_time or 0,
            documents_studied=stats.documents or 0,
            quizzes_completed=quiz_count or 0,
            average_quiz_score=0,
            flashcards_reviewed=0,
            tutor_conversations=0,
        )

    def get_study_progress(self, user_id: str) -> StudyProgress:
        return StudyProgress(documents=[], overall_progress=0)

    def get_learning_streak(self, user_id: str) -> LearningStreak:
        return LearningStreak(
            current_streak=0,
            longest_streak=0,
            last_activity_date="",
            streak_active=False,
        )

    def get_recently_viewed(self, user_id: str, limit: int = 5) -> list[RecentlyViewedDocument]:
        return []

    def _get_event_description(self, event: ProgressEvent) -> str:
        descriptions = {
            ProgressEventType.quiz_completed: "Completed a quiz",
            ProgressEventType.flashcard_reviewed: "Reviewed flashcards",
            ProgressEventType.chapter_completed: "Completed a chapter",
            ProgressEventType.reading_progress: "Made reading progress",
            ProgressEventType.tutor_used: "Used AI Tutor",
            ProgressEventType.diagram_interacted: "Viewed a diagram",
            ProgressEventType.revision_completed: "Completed revision",
        }
        return descriptions.get(event.event_type, "Learning activity")
