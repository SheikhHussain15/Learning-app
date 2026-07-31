import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.models.workspace_section import SectionStatus, SectionType, WorkspaceSection
from src.services.base import BaseService


class WorkspaceService(BaseService[WorkspaceSection]):
    def __init__(self, db: Session):
        super().__init__(WorkspaceSection, db)

    def get_sections_by_document(self, document_id: str) -> list[WorkspaceSection]:
        return self.db.query(WorkspaceSection).filter(
            WorkspaceSection.document_id == document_id
        ).all()

    def get_section_by_type(self, document_id: str, section_type: SectionType) -> WorkspaceSection | None:
        return self.db.query(WorkspaceSection).filter(
            WorkspaceSection.document_id == document_id,
            WorkspaceSection.section_type == section_type
        ).first()

    def request_generation(self, document_id: str, section_type: SectionType) -> WorkspaceSection:
        section = self.get_section_by_type(document_id, section_type)
        if section:
            if section.status == SectionStatus.processing:
                return section
            section.status = SectionStatus.processing
            section.requested_at = datetime.now(UTC)
            section.error_message = None
        else:
            section = WorkspaceSection(
                id=str(uuid.uuid4()),
                document_id=document_id,
                section_type=section_type,
                status=SectionStatus.processing,
                requested_at=datetime.now(UTC),
            )
            self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section

    def complete_generation(self, section_id: str, content: dict) -> WorkspaceSection | None:
        section = self.get(section_id)
        if section:
            section.status = SectionStatus.completed
            section.content = content
            section.completed_at = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(section)
        return section

    def fail_generation(self, section_id: str, error_message: str) -> WorkspaceSection | None:
        section = self.get(section_id)
        if section:
            section.status = SectionStatus.failed
            section.error_message = error_message
            self.db.commit()
            self.db.refresh(section)
        return section

    def retry_generation(self, section_id: str) -> WorkspaceSection | None:
        section = self.get(section_id)
        if section and section.status == SectionStatus.failed:
            section.status = SectionStatus.processing
            section.requested_at = datetime.now(UTC)
            section.error_message = None
            self.db.commit()
            self.db.refresh(section)
        return section
