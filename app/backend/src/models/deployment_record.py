import enum
import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from src.core.database import Base


class DeploymentEnvironment(enum.StrEnum):
    staging = "staging"
    production = "production"


class DeploymentStatus(enum.StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    success = "success"
    failed = "failed"
    rolled_back = "rolled_back"


class DeploymentRecord(Base):
    __tablename__ = "deployment_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    version = Column(String(20), nullable=False)
    environment = Column(String(20), nullable=False, index=True)
    status = Column(String(20), nullable=False, default=DeploymentStatus.pending.value)
    deployed_by = Column(String(255), nullable=False)
    deployed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    rollback_from = Column(String, nullable=True)
