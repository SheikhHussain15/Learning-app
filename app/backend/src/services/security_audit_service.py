from datetime import datetime

from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.models.security_audit_log import SecurityAuditLog, SecurityEventType

logger = get_logger("security_audit")


class SecurityAuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        event_type: SecurityEventType,
        user_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        details: dict | None = None,
    ) -> SecurityAuditLog:
        redacted_user_id = self._redact_user_id(user_id) if user_id else None

        log_entry = SecurityAuditLog(
            event_type=event_type.value,
            user_id=redacted_user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)

        logger.info(
            "security_event",
            event_type=event_type.value,
            user_id=redacted_user_id,
            ip_address=ip_address,
        )

        return log_entry

    def log_login_success(self, user_id: str, ip_address: str, user_agent: str):
        return self.log_event(
            SecurityEventType.login_success,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def log_login_failure(self, user_id: str, ip_address: str, user_agent: str, reason: str):
        return self.log_event(
            SecurityEventType.login_failure,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"reason": reason},
        )

    def log_rate_limit(self, ip_address: str, path: str):
        return self.log_event(
            SecurityEventType.rate_limit,
            ip_address=ip_address,
            details={"path": path},
        )

    def log_permission_denied(self, user_id: str, resource: str, action: str):
        return self.log_event(
            SecurityEventType.permission_denied,
            user_id=user_id,
            details={"resource": resource, "action": action},
        )

    def get_logs(
        self,
        event_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
    ) -> list[SecurityAuditLog]:
        query = self.db.query(SecurityAuditLog)

        if event_type:
            query = query.filter(SecurityAuditLog.event_type == event_type)
        if start_date:
            query = query.filter(SecurityAuditLog.created_at >= start_date)
        if end_date:
            query = query.filter(SecurityAuditLog.created_at <= end_date)

        return query.order_by(SecurityAuditLog.created_at.desc()).limit(limit).all()

    def _redact_user_id(self, user_id: str) -> str:
        if len(user_id) > 8:
            return user_id[:4] + "***" + user_id[-4:]
        return user_id
