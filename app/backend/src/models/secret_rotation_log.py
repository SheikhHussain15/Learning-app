import enum
import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from src.core.database import Base


class SecretType(enum.StrEnum):
    ai_key = "ai_key"
    db_password = "db_password"
    jwt_secret = "jwt_secret"
    storage_key = "storage_key"


class SecretRotationLog(Base):
    __tablename__ = "secret_rotation_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    secret_type = Column(String(20), nullable=False, index=True)
    rotated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    rotated_by = Column(String(255), nullable=False)
    previous_rotation = Column(DateTime(timezone=True), nullable=True)
