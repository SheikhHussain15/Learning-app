from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.schemas.production import ComponentHealth, HealthCheckResponse
from src.services.health_service import HealthService

router = APIRouter()


@router.get("", response_model=HealthCheckResponse)
def get_health(db: Session = Depends(get_db)):
    service = HealthService(db)
    result = service.check_all()

    from fastapi.responses import JSONResponse
    status_code = 200 if result["status"] == "healthy" else 503
    return JSONResponse(
        status_code=status_code,
        content=result,
    )


@router.get("/{component}", response_model=ComponentHealth)
def get_component_health(component: str, db: Session = Depends(get_db)):
    service = HealthService(db)
    result = service.check_component(component)

    from fastapi.responses import JSONResponse
    status_code = 200 if result["status"] == "healthy" else 503
    return JSONResponse(
        status_code=status_code,
        content=result,
    )
