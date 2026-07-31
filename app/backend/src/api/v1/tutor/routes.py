from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.schemas.tutor import (
    TutorConversationResponse,
    TutorMessageRequest,
    TutorMessageResponse,
)
from src.services.tutor import TutorService

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/message", response_model=TutorMessageResponse)
async def send_message(
    request: TutorMessageRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = TutorService(db)
    return await service.send_message(current_user.id, request)


@router.get("/conversation/{document_id}", response_model=TutorConversationResponse)
async def get_conversation(
    document_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = TutorService(db)
    return await service.get_conversation(current_user.id, document_id, limit)


@router.delete("/conversation/{document_id}")
async def clear_conversation(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return {"status": "cleared"}
