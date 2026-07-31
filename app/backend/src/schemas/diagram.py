from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class DiagramType(StrEnum):
    flowchart = "flowchart"
    mind_map = "mind_map"
    timeline = "timeline"
    concept_map = "concept_map"
    sequence = "sequence"
    class_diagram = "class"
    state = "state"
    er = "er"


class RenderFormat(StrEnum):
    mermaid = "mermaid"
    svg = "svg"
    json = "json"


class DiagramMetadata(BaseModel):
    width: int
    height: int
    node_count: int
    edge_count: int


class Diagram(BaseModel):
    id: str
    document_id: str
    title: str
    description: str
    diagram_type: DiagramType
    content: dict
    source_refs: list[str]
    created_at: datetime


class DiagramRenderData(BaseModel):
    diagram_id: str
    format: RenderFormat
    data: str
    metadata: DiagramMetadata


class DiagramGenerateRequest(BaseModel):
    document_id: str
    section_id: str | None = None
    diagram_type: DiagramType = DiagramType.flowchart
    title: str | None = None


class DiagramGenerateResponse(BaseModel):
    id: str
    document_id: str
    title: str
    description: str
    diagram_type: DiagramType
    content: dict
    source_refs: list[str] = []
