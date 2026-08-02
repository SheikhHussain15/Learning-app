import logging
import uuid

from src.core.database import SessionLocal
from src.models.progress_event import EventType, ProgressEvent

logger = logging.getLogger(__name__)


def record_event(
    user_id: str,
    event_type: str,
    document_id: str | None = None,
    event_data: dict | None = None,
) -> ProgressEvent:
    """Record a learning event."""
    db = SessionLocal()
    try:
        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=EventType(event_type),
            document_id=document_id,
            event_data=event_data or {},
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        logger.info("Recorded event %s for user %s", event_type, user_id)
        return event
    finally:
        db.close()


def get_user_events(user_id: str, limit: int = 100) -> list[ProgressEvent]:
    """Get recent events for a user."""
    db = SessionLocal()
    try:
        return (
            db.query(ProgressEvent)
            .filter(ProgressEvent.user_id == user_id)
            .order_by(ProgressEvent.created_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


def get_user_events_by_type(user_id: str, event_type: str) -> list[ProgressEvent]:
    """Get events for a user filtered by type."""
    db = SessionLocal()
    try:
        return (
            db.query(ProgressEvent)
            .filter(ProgressEvent.user_id == user_id, ProgressEvent.event_type == EventType(event_type))
            .order_by(ProgressEvent.created_at.desc())
            .all()
        )
    finally:
        db.close()


def get_user_progress_summary(user_id: str) -> dict:
    """Aggregate user progress from events."""
    db = SessionLocal()
    try:
        events = db.query(ProgressEvent).filter(ProgressEvent.user_id == user_id).all()

        documents_viewed = set()
        quiz_scores = []
        topics_mastered = []
        areas_needing_review = []

        for event in events:
            if event.event_type == EventType.document_viewed and event.document_id:
                documents_viewed.add(event.document_id)
            elif event.event_type == EventType.quiz_completed:
                data = event.event_data or {}
                if "score" in data and "total_questions" in data:
                    quiz_scores.append(data["score"] / data["total_questions"])

        total_quiz_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0

        return {
            "documents_studied": len(documents_viewed),
            "total_quiz_score": total_quiz_score,
            "topics_mastered": topics_mastered,
            "areas_needing_review": areas_needing_review,
        }
    finally:
        db.close()
