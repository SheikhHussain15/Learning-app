import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.models.test_suite_result import TestSuiteType
from src.models.user import User
from src.schemas.production import TestResultResponse, TestRunRequest, TestRunResponse
from src.services.test_result_service import TestResultService

router = APIRouter()


@router.get("/results", response_model=list[TestResultResponse])
def get_test_results(
    suite_type: str | None = Query(None, description="Filter by suite type"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TestResultService(db)
    st = TestSuiteType(suite_type) if suite_type else None
    results = service.get_results(suite_type=st, limit=limit)
    return results


@router.post("/run", response_model=TestRunResponse, status_code=202)
def trigger_test_run(
    request: TestRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run_id = str(uuid.uuid4())
    return TestRunResponse(
        run_id=run_id,
        status="queued",
        estimated_duration_seconds=300,
    )
