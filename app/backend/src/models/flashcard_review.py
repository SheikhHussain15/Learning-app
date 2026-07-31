import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class DifficultyRating(enum.StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class FlashcardReview(Base):
    __tablename__ = "flashcard_reviews"

    id = Column(String, primary_key=True)
    flashcard_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    difficulty_rating = Column(Enum(DifficultyRating), nullable=False)
    review_duration = Column(Integer, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=False)
    next_review_at = Column(DateTime(timezone=True), nullable=False)
    review_count = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = ()
