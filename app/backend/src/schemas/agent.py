from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from src.models.agent_run import AgentStatus, AgentType


class TokenUsage(BaseModel):
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)


class ErrorInfo(BaseModel):
    code: str
    message: str
    retryable: bool


class SourceRef(BaseModel):
    chunk_id: str
    document_id: str
    node_id: str | None = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    score: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RequestContext(BaseModel):
    chunks: list[RetrievedChunk] = Field(default_factory=list)
    source_doc_id: str | None = None
    previous_agent_output: dict[str, Any] | None = None


class RequestEnvelope(BaseModel):
    document_id: str
    node_ids: list[str]
    agent_params: dict[str, Any] = Field(default_factory=dict)
    context: RequestContext | None = None
    trace_id: str


class ResponseEnvelope(BaseModel):
    status: Literal["success", "error", "partial"]
    output: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[SourceRef] = Field(default_factory=list)
    usage: TokenUsage
    error: ErrorInfo | None = None


class ModelConfig(BaseModel):
    agent_type: AgentType
    primary_model_id: str
    fallback_model_id: str
    capabilities: list[str] = Field(default_factory=list)
    cost_tier: Literal["low", "medium", "high"]


class AgentRunCreate(BaseModel):
    agent_type: AgentType
    document_id: str | None = None
    node_ids: list[str] = Field(default_factory=list)
    agent_params: dict[str, Any] = Field(default_factory=dict)
    context: RequestContext | None = None


class AgentRunResponse(BaseModel):
    id: str
    status: AgentStatus
    agent_type: AgentType
    response_envelope: ResponseEnvelope | None = None
    error: ErrorInfo | None = None
    duration_ms: int | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True
