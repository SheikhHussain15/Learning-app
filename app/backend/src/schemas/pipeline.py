from typing import Any

from pydantic import BaseModel, Field

from src.models.agent_run import AgentType


class PipelineRequest(BaseModel):
    document_id: str
    user_id: str
    requested_agents: list[AgentType] = Field(default_factory=list)
    agent_params: dict[str, dict[str, Any]] = Field(default_factory=dict)
    force_reprocess: bool = False


class AgentRunResponse(BaseModel):
    id: str
    status: str
    agent_type: AgentType
    response_envelope: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    duration_ms: int | None = None


class PipelineResponse(BaseModel):
    pipeline_id: str
    status: str  # "queued", "running", "succeeded", "partial", "failed"
    agent_results: dict[str, AgentRunResponse]
    duration_ms: int | None = None
