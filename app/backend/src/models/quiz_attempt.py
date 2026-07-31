import enum

from sqlalchemy import JSON, Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class QuizAttemptStatus(enum.StrEnum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True)
    quiz_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=True)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=True)
    answers = Column(JSON, nullable=True)
    time_spent = Column(Integer, nullable=True)
    status = Column(Enum(QuizAttemptStatus), nullable=False, default=QuizAttemptStatus.in_progress)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = ()
