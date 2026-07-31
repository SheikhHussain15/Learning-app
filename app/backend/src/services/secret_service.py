from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.models.secret_rotation_log import SecretRotationLog, SecretType

logger = get_logger("secret_service")


class SecretService:
    def __init__(self, db: Session):
        self.db = db

    def log_rotation(
        self,
        secret_type: SecretType,
        rotated_by: str,
    ) -> SecretRotationLog:
        previous = (
            self.db.query(SecretRotationLog)
            .filter(SecretRotationLog.secret_type == secret_type.value)
            .order_by(SecretRotationLog.rotated_at.desc())
            .first()
        )

        log_entry = SecretRotationLog(
            secret_type=secret_type.value,
            rotated_by=rotated_by,
            previous_rotation=previous.rotated_at if previous else None,
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)

        logger.info(
            "secret_rotated",
            secret_type=secret_type.value,
            rotated_by=rotated_by,
        )

        return log_entry

    def get_rotation_history(
        self,
        secret_type: SecretType | None = None,
        limit: int = 10,
    ) -> list[SecretRotationLog]:
        query = self.db.query(SecretRotationLog)
        if secret_type:
            query = query.filter(SecretRotationLog.secret_type == secret_type.value)
        return query.order_by(SecretRotationLog.rotated_at.desc()).limit(limit).all()
