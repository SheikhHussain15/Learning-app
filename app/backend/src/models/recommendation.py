import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class RecommendationType(enum.StrEnum):
    document = "document"
    quiz = "quiz"
    flashcard = "flashcard"
    review = "review"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    recommendation_type = Column(Enum(RecommendationType), nullable=False)
    document_id = Column(String, nullable=True)
    section_id = Column(String, nullable=True)
    reason = Column(String, nullable=False)
    priority = Column(Integer, nullable=False, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = ()
