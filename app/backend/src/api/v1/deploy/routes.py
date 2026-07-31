from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.schemas.production import DeploymentStatusResponse, RollbackRequest
from src.services.deployment_service import DeploymentService

router = APIRouter()


@router.get("/status", response_model=DeploymentStatusResponse)
def get_deployment_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DeploymentService(db)
    deployment = service.get_current_deployment()

    if not deployment:
        return JSONResponse(
            status_code=200,
            content={
                "current_version": "0.0.0",
                "environment": "staging",
                "deployed_at": None,
                "deployed_by": "system",
                "rollback_available": False,
            },
        )

    return DeploymentStatusResponse(
        current_version=deployment.version,
        environment=deployment.environment,
        deployed_at=deployment.deployed_at,
        deployed_by=deployment.deployed_by,
        rollback_available=service.is_rollback_available(),
    )


@router.post("/rollback", status_code=202)
def trigger_rollback(
    request: RollbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DeploymentService(db)
    result = service.rollback(reason=request.reason)

    if not result:
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "NO_ROLLBACK", "message": "No previous version to rollback to"}},
        )

    return {"message": "Rollback initiated", "deployment_id": result.id}
