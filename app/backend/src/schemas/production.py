from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    timestamp: datetime
    components: list["ComponentHealth"]


class ComponentHealth(BaseModel):
    name: str
    status: Literal["healthy", "degraded", "unhealthy"]
    latency_ms: int = Field(ge=0)
    error: str | None = None


class DeploymentStatusResponse(BaseModel):
    current_version: str
    environment: Literal["staging", "production"]
    deployed_at: datetime
    deployed_by: str
    rollback_available: bool


class RollbackRequest(BaseModel):
    reason: str = ""


class AuditLogEntry(BaseModel):
    id: str
    event_type: str
    user_id: str | None = None
    ip_address: str | None = None
    details: dict = Field(default_factory=dict)
    created_at: datetime

    class Config:
        from_attributes = True


class TestResultResponse(BaseModel):
    id: str
    suite_type: str
    total_tests: int
    passed: int
    failed: int
    skipped: int = 0
    coverage_percent: float | None = None
    duration_seconds: int
    run_at: datetime
    commit_sha: str | None = None

    class Config:
        from_attributes = True


class TestRunRequest(BaseModel):
    suite_type: Literal["unit", "contract", "integration", "e2e", "all"] = "all"
    parallel: bool = True


class TestRunResponse(BaseModel):
    run_id: str
    status: Literal["queued", "running", "completed", "failed"]
    estimated_duration_seconds: int


HealthCheckResponse.model_rebuild()
