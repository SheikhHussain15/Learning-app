import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from src.models.flashcard_review import FlashcardReview
from src.models.progress_event import ProgressEvent, ProgressEventType
from src.schemas.flashcard import (
    FlashcardGenerateRequest,
    FlashcardGenerateResponse,
    FlashcardReviewRequest,
    FlashcardReviewResponse,
)


class FlashcardService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_flashcards(self, request: FlashcardGenerateRequest) -> FlashcardGenerateResponse:
        return FlashcardGenerateResponse(
            document_id=request.document_id,
            cards=[],
            total_cards=0,
        )

    async def get_flashcards(self, user_id: str, document_id: str) -> list:
        return []

    async def review_flashcard(self, user_id: str, review: FlashcardReviewRequest) -> FlashcardReviewResponse:
        flashcard_review = FlashcardReview(
            id=str(uuid.uuid4()),
            flashcard_id=review.flashcard_id,
            user_id=user_id,
            difficulty_rating=review.difficulty,
            review_duration=review.review_duration,
            reviewed_at=datetime.now(UTC),
            next_review_at=datetime.now(UTC) + timedelta(days=1),
            review_count=1,
        )
        self.db.add(flashcard_review)

        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=ProgressEventType.flashcard_reviewed,
            event_data={"flashcard_id": review.flashcard_id, "difficulty": review.difficulty.value},
        )
        self.db.add(event)

        self.db.commit()

        return FlashcardReviewResponse(
            flashcard_id=review.flashcard_id,
            difficulty=review.difficulty,
            next_review_at=flashcard_review.next_review_at,
            review_count=1,
            message="Review recorded",
        )

    async def get_due_cards(self, user_id: str, document_id: str) -> list:
        return []

    async def get_review_stats(self, user_id: str, document_id: str) -> dict:
        return {
            "total_cards": 0,
            "reviewed_today": 0,
            "due_today": 0,
            "mastered": 0,
        }
