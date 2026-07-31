
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.schemas.progress import (
    ProgressEventRequest,
    ProgressEventResponse,
    ProgressStatsResponse,
    ProgressSummaryResponse,
)
from src.services.progress import ProgressService

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/event", response_model=ProgressEventResponse)
async def record_event(
    request: ProgressEventRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ProgressService(db)
    return await service.record_event(current_user.id, request)


@router.get("", response_model=ProgressSummaryResponse)
async def get_progress(
    document_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ProgressService(db)
    return await service.get_progress(current_user.id, document_id)


@router.get("/stats", response_model=ProgressStatsResponse)
async def get_stats(
    document_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ProgressService(db)
    return await service.get_stats(current_user.id, document_id)
