import enum
import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class HealthStatus(enum.StrEnum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"


class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    component = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default=HealthStatus.healthy.value)
    latency_ms = Column(Integer, nullable=False, default=0)
    error_message = Column(String(500), nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
