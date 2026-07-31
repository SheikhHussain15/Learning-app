from datetime import datetime

from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    chunk_id: str
    document_id: str
    chapter_title: str
    topic_title: str
    content_preview: str
    relevance_score: float = Field(ge=0, le=1)


class TutorMessage(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    sources: list[SourceReference]
    created_at: datetime


class TutorConversation(BaseModel):
    id: str
    document_id: str
    user_id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime


class TutorMessageInput(BaseModel):
    content: str


class TutorResponse(BaseModel):
    message_id: str
    role: str = "assistant"
    content: str
    sources: list[SourceReference]
    is_grounded: bool
    confidence: float = Field(ge=0, le=1)
    created_at: datetime


class TutorMessageRequest(BaseModel):
    document_id: str
    content: str


class TutorMessageResponse(BaseModel):
    message_id: str
    role: str
    content: str
    sources: list[SourceReference] = []
    is_grounded: bool = False
    confidence: float = 0.0


class TutorConversationResponse(BaseModel):
    id: str
    document_id: str
    user_id: str
    title: str
    message_count: int
    messages: list[TutorMessageResponse] = []
