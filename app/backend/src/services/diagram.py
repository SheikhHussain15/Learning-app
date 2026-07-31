import uuid

from sqlalchemy.orm import Session

from src.models.progress_event import ProgressEvent, ProgressEventType
from src.schemas.diagram import DiagramGenerateRequest, DiagramGenerateResponse


class DiagramService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_diagram(self, request: DiagramGenerateRequest) -> DiagramGenerateResponse:
        return DiagramGenerateResponse(
            id=str(uuid.uuid4()),
            document_id=request.document_id,
            title=request.title or "Diagram",
            description="Generated diagram",
            diagram_type=request.diagram_type,
            content={"mermaid": "graph TD\n    A-->B"},
            source_refs=[],
        )

    async def get_diagrams(self, document_id: str) -> list:
        return []

    async def get_diagram(self, diagram_id: str) -> dict | None:
        return None

    async def interact_with_diagram(
        self, user_id: str, diagram_id: str, document_id: str
    ) -> None:
        event = ProgressEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            event_type=ProgressEventType.diagram_interacted,
            document_id=document_id,
            event_data={"diagram_id": diagram_id},
        )
        self.db.add(event)
        self.db.commit()
