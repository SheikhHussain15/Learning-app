from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class QuizAttemptStatus(StrEnum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class QuestionOption(BaseModel):
    id: str
    text: str
    order: int


class Question(BaseModel):
    id: str
    text: str
    options: list[QuestionOption]
    order: int


class Quiz(BaseModel):
    id: str
    document_id: str
    title: str
    description: str
    questions: list[Question]
    total_questions: int
    created_at: datetime


class QuizAttempt(BaseModel):
    id: str
    quiz_id: str
    user_id: str
    status: QuizAttemptStatus
    current_question_index: int
    total_questions: int
    started_at: datetime
    completed_at: datetime | None = None


class AnswerSubmission(BaseModel):
    question_id: str
    option_id: str


class AnswerFeedback(BaseModel):
    question_id: str
    selected_option_id: str
    correct_option_id: str
    is_correct: bool
    explanation: str


class QuizResults(BaseModel):
    attempt_id: str
    score: float = Field(ge=0, le=100)
    total_questions: int
    correct_answers: int
    time_spent: int
    completed_at: datetime


class ReviewQuestion(BaseModel):
    question_id: str
    text: str
    options: list[QuestionOption]
    selected_option_id: str
    correct_option_id: str
    is_correct: bool
    explanation: str


class QuizReview(BaseModel):
    attempt_id: str
    questions: list[ReviewQuestion]
    score: float
    total_questions: int


class QuizGenerateRequest(BaseModel):
    document_id: str
    difficulty: str | None = "medium"
    question_count: int = Field(default=10, ge=1, le=50)


class QuizGenerateResponse(BaseModel):
    quiz_id: str
    document_id: str
    title: str
    questions: list[Question]
    total_questions: int
    difficulty: str


class QuizSubmitRequest(BaseModel):
    document_id: str
    answers: list[dict]


class QuizSubmitResponse(BaseModel):
    attempt_id: str
    score: float
    total_questions: int
    correct_answers: int


class QuizHistoryItem(BaseModel):
    attempt_id: str
    document_id: str
    score: float
    total_questions: int
    completed_at: datetime
