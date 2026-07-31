from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.schemas.flashcard import (
    FlashcardGenerateRequest,
    FlashcardGenerateResponse,
    FlashcardReviewRequest,
    FlashcardReviewResponse,
)
from src.services.flashcard import FlashcardService

router = APIRouter(prefix="/flashcard", tags=["flashcard"])


@router.post("/generate", response_model=FlashcardGenerateResponse)
async def generate_flashcards(
    request: FlashcardGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = FlashcardService(db)
    return await service.generate_flashcards(request)


@router.get("/{document_id}")
async def get_flashcards(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = FlashcardService(db)
    return await service.get_flashcards(current_user.id, document_id)


@router.post("/review", response_model=FlashcardReviewResponse)
async def review_flashcard(
    review: FlashcardReviewRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = FlashcardService(db)
    return await service.review_flashcard(current_user.id, review)


@router.get("/{document_id}/due")
async def get_due_cards(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = FlashcardService(db)
    return await service.get_due_cards(current_user.id, document_id)


@router.get("/{document_id}/stats")
async def get_review_stats(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = FlashcardService(db)
    return await service.get_review_stats(current_user.id, document_id)
