import enum
import uuid

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.sql import func

from src.core.database import Base


class SecurityEventType(enum.StrEnum):
    login_success = "login_success"
    login_failure = "login_failure"
    rate_limit = "rate_limit"
    permission_denied = "permission_denied"
    secret_access = "secret_access"


class SecurityAuditLog(Base):
    __tablename__ = "security_audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String(30), nullable=False, index=True)
    user_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
