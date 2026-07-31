from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.models.document import Document
from src.models.user import User
from src.schemas.workspace import (
    SectionContentResponse,
    SectionRequestResponse,
    SectionStatusResponse,
    SectionType,
    WorkspaceOverview,
)
from src.services.workspace import WorkspaceService

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("/{document_id}", response_model=WorkspaceOverview)
async def get_workspace(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == document_id, Document.owner_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    service = WorkspaceService(db)
    sections = service.get_sections_by_document(document_id)
    return WorkspaceOverview(
        document_id=document_id,
        title=doc.title,
        description="Document description",
        metadata={},
        chapters=[],
        sections=sections,
    )


@router.get("/{document_id}/sections/{section_type}/status", response_model=SectionStatusResponse)
async def get_section_status(document_id: str, section_type: SectionType, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WorkspaceService(db)
    section = service.get_section_by_type(document_id, section_type)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return SectionStatusResponse(
        section_id=section.id,
        status=section.status,
        progress=100 if section.status == "completed" else 0,
        error_message=section.error_message,
    )


@router.post("/{document_id}/sections/{section_type}/request", response_model=SectionRequestResponse)
async def request_generation(document_id: str, section_type: SectionType, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WorkspaceService(db)
    section = service.request_generation(document_id, section_type)
    return SectionRequestResponse(
        section_id=section.id,
        status="processing",
        message=f"Generation requested for {section_type}",
    )


@router.get("/{document_id}/sections/{section_type}/content", response_model=SectionContentResponse)
async def get_section_content(document_id: str, section_type: SectionType, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WorkspaceService(db)
    section = service.get_section_by_type(document_id, section_type)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    if section.status != "completed":
        raise HTTPException(status_code=400, detail="Section not ready")
    return SectionContentResponse(
        section_id=section.id,
        section_type=section.section_type,
        content=section.content or {},
        metadata={},
    )
