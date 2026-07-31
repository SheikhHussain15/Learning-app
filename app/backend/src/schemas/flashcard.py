from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DifficultyRating(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Flashcard(BaseModel):
    id: str
    document_id: str
    front: str
    back: str
    order: int
    next_review_at: datetime | None = None
    review_count: int
    created_at: datetime


class FlashcardDeck(BaseModel):
    document_id: str
    title: str
    total_cards: int
    cards: list[Flashcard]
    created_at: datetime


class FlashcardReviewSubmission(BaseModel):
    difficulty: DifficultyRating
    review_duration: int | None = None


class FlashcardReviewResult(BaseModel):
    flashcard_id: str
    difficulty: DifficultyRating
    next_review_at: datetime
    review_count: int
    message: str


class FlashcardProgress(BaseModel):
    document_id: str
    total_cards: int
    reviewed_today: int
    due_for_review: int
    mastered: int
    learning: int
    new_cards: int


class FlashcardReviewHistory(BaseModel):
    id: str
    flashcard_id: str
    difficulty: DifficultyRating
    review_duration: int
    next_review_at: datetime
    reviewed_at: datetime


class FlashcardGenerateRequest(BaseModel):
    document_id: str
    section_id: str | None = None
    card_count: int = Field(default=10, ge=1, le=50)


class FlashcardGenerateResponse(BaseModel):
    document_id: str
    cards: list[Flashcard]
    total_cards: int


class FlashcardReviewRequest(BaseModel):
    flashcard_id: str
    difficulty: DifficultyRating
    review_duration: int | None = None


class FlashcardReviewResponse(BaseModel):
    flashcard_id: str
    difficulty: DifficultyRating
    next_review_at: datetime
    review_count: int
    message: str
