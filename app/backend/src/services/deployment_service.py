from datetime import datetime

from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.models.deployment_record import DeploymentEnvironment, DeploymentRecord, DeploymentStatus

logger = get_logger("deployment_service")


class DeploymentService:
    def __init__(self, db: Session):
        self.db = db

    def create_deployment(
        self,
        version: str,
        environment: DeploymentEnvironment,
        deployed_by: str,
    ) -> DeploymentRecord:
        record = DeploymentRecord(
            version=version,
            environment=environment.value,
            status=DeploymentStatus.pending.value,
            deployed_by=deployed_by,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        logger.info("deployment_created", version=version, environment=environment.value)
        return record

    def start_deployment(self, deployment_id: str) -> DeploymentRecord:
        record = self.db.query(DeploymentRecord).filter(DeploymentRecord.id == deployment_id).first()
        if not record:
            raise ValueError(f"Deployment {deployment_id} not found")
        record.status = DeploymentStatus.in_progress.value
        self.db.commit()
        self.db.refresh(record)
        logger.info("deployment_started", deployment_id=deployment_id)
        return record

    def complete_deployment(self, deployment_id: str, success: bool = True) -> DeploymentRecord:
        record = self.db.query(DeploymentRecord).filter(DeploymentRecord.id == deployment_id).first()
        if not record:
            raise ValueError(f"Deployment {deployment_id} not found")
        record.status = DeploymentStatus.success.value if success else DeploymentStatus.failed.value
        record.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(record)
        logger.info("deployment_completed", deployment_id=deployment_id, success=success)
        return record

    def rollback(self, reason: str = "") -> DeploymentRecord | None:
        latest = (
            self.db.query(DeploymentRecord)
            .filter(DeploymentRecord.status == DeploymentStatus.success.value)
            .order_by(DeploymentRecord.deployed_at.desc())
            .first()
        )
        if not latest:
            return None

        rollback_record = DeploymentRecord(
            version=latest.version,
            environment=latest.environment,
            status=DeploymentStatus.rolled_back.value,
            deployed_by="system-rollback",
            rollback_from=latest.id,
        )
        self.db.add(rollback_record)
        self.db.commit()
        self.db.refresh(rollback_record)
        logger.info("deployment_rollback", from_deployment=latest.id, reason=reason)
        return rollback_record

    def get_current_deployment(self, environment: str | None = None) -> DeploymentRecord | None:
        query = self.db.query(DeploymentRecord).filter(
            DeploymentRecord.status == DeploymentStatus.success.value
        )
        if environment:
            query = query.filter(DeploymentRecord.environment == environment)
        return query.order_by(DeploymentRecord.deployed_at.desc()).first()

    def is_rollback_available(self) -> bool:
        return self.db.query(DeploymentRecord).filter(
            DeploymentRecord.status == DeploymentStatus.success.value
        ).count() > 1
