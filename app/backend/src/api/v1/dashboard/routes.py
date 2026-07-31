from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.schemas.dashboard import DashboardData
from src.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardData)
async def get_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = DashboardService(db)
    return service.get_dashboard_data(current_user.id)


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DashboardService(db)
    return service.get_recent_activity(current_user.id, limit)


@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = DashboardService(db)
    return service.get_statistics(current_user.id)


@router.get("/progress")
async def get_progress(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = DashboardService(db)
    return service.get_study_progress(current_user.id)


@router.get("/streak")
async def get_streak(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = DashboardService(db)
    return service.get_learning_streak(current_user.id)


@router.get("/recently-viewed")
async def get_recently_viewed(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DashboardService(db)
    return service.get_recently_viewed(current_user.id, limit)
