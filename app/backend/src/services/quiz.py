import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.models.progress_event import ProgressEvent, ProgressEventType
from src.models.quiz_attempt import QuizAttempt
from src.schemas.quiz import (
    QuizGenerateRequest,
    QuizGenerateResponse,
    QuizSubmitResponse,
)


class QuizService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_quiz(self, request: QuizGenerateRequest) -> QuizGenerateResponse:
        return QuizGenerateResponse(
            quiz_id=str(uuid.uuid4()),
            document_id=request.document_id,
            title="Quiz",
            questions=[],
            total_questions=0,
            difficulty=request.difficulty or "medium",
        )

    async def submit_quiz(self, user_id: str, document_id: str, answers: list[dict]) -> QuizSubmitResponse:
        score = self._calculate_score(answers)

        attempt = QuizAttempt(
            id=str(uuid.uuid4()),
            quiz_id=str(uuid.uuid4()),
            user_id=user_id,
            score=score,
            total_questions=len(answers),
            correct_answers=sum(1 for a in answers if a.get("is_correct")),
            answers=answers,
            time_spent=0,
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
        )
        self.db.add(attempt)

        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=ProgressEventType.quiz_completed,
            document_id=document_id,
            event_data={"score": score, "total": len(answers)},
        )
        self.db.add(event)

        self.db.commit()

        return QuizSubmitResponse(
            attempt_id=attempt.id,
            score=score,
            total_questions=len(answers),
            correct_answers=attempt.correct_answers or 0,
        )

    def _calculate_score(self, answers: list[dict]) -> float:
        if not answers:
            return 0.0
        correct = sum(1 for a in answers if a.get("is_correct", False))
        return correct / len(answers) * 100
