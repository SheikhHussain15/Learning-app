from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.schemas.diagram import (
    DiagramGenerateRequest,
    DiagramGenerateResponse,
)
from src.services.diagram import DiagramService

router = APIRouter(prefix="/diagram", tags=["diagram"])


@router.post("/generate", response_model=DiagramGenerateResponse)
async def generate_diagram(
    request: DiagramGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DiagramService(db)
    return await service.generate_diagram(request)


@router.get("/{document_id}")
async def get_diagrams(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DiagramService(db)
    return await service.get_diagrams(document_id)


@router.get("/{diagram_id}/detail")
async def get_diagram(
    diagram_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DiagramService(db)
    return await service.get_diagram(diagram_id)


@router.post("/{diagram_id}/interact")
async def interact_with_diagram(
    diagram_id: str,
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = DiagramService(db)
    await service.interact_with_diagram(current_user.id, diagram_id, document_id)
    return {"status": "recorded"}
