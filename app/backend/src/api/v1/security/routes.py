from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.schemas.production import AuditLogEntry
from src.services.security_audit_service import SecurityAuditService

router = APIRouter()


@router.get("/audit-log", response_model=list[AuditLogEntry])
def get_audit_logs(
    event_type: str | None = Query(None, description="Filter by event type"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SecurityAuditService(db)
    logs = service.get_logs(
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
    return logs
