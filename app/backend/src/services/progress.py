import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.progress_event import ProgressEvent
from src.schemas.progress import (
    ProgressEventRequest,
    ProgressEventResponse,
    ProgressStatsResponse,
    ProgressSummaryResponse,
)


class ProgressService:
    def __init__(self, db: Session):
        self.db = db

    async def record_event(self, user_id: str, request: ProgressEventRequest) -> ProgressEventResponse:
        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=request.event_type,
            document_id=request.document_id,
            section_id=request.section_id,
            event_data=request.event_data,
            duration=request.duration,
        )
        self.db.add(event)
        self.db.commit()
        return ProgressEventResponse(
            id=event.id,
            event_type=event.event_type,
            document_id=event.document_id,
            created_at=event.created_at,
        )

    async def get_progress(self, user_id: str, document_id: str | None = None) -> ProgressSummaryResponse:
        query = self.db.query(ProgressEvent).filter(ProgressEvent.user_id == user_id)

        if document_id:
            query = query.filter(ProgressEvent.document_id == document_id)

        events = query.order_by(ProgressEvent.created_at.desc()).limit(100).all()

        return ProgressSummaryResponse(
            events=[
                {
                    "id": e.id,
                    "event_type": e.event_type.value if e.event_type else "",
                    "document_id": e.document_id or "",
                    "created_at": e.created_at.isoformat() if e.created_at else "",
                }
                for e in events
            ],
            total_events=len(events),
        )

    async def get_stats(self, user_id: str, document_id: str | None = None) -> ProgressStatsResponse:
        query = self.db.query(
            func.count(ProgressEvent.id).label("total_events"),
            func.coalesce(func.sum(ProgressEvent.duration), 0).label("total_time"),
        ).filter(ProgressEvent.user_id == user_id)

        if document_id:
            query = query.filter(ProgressEvent.document_id == document_id)

        stats = query.first()

        return ProgressStatsResponse(
            total_events=stats.total_events or 0,
            total_time=stats.total_time or 0,
            documents_studied=0,
            average_score=0,
        )
