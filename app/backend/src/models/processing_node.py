import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


def _utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


class NodeType(enum.StrEnum):
    chapter = "chapter"
    topic = "topic"
    subtopic = "subtopic"


class ProcessingNode(Base):
    __tablename__ = "processing_nodes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, nullable=False, index=True)
    parent_id = Column(String, ForeignKey("processing_nodes.id"), nullable=True, index=True)
    node_type = Column(Enum(NodeType), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    position = Column(Integer, nullable=False, default=0)
    node_metadata = Column("metadata", JSON, default=dict)
    chunk_ids = Column(JSON, default=list)
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    children = relationship("ProcessingNode", back_populates="parent", lazy="selectin")
    parent = relationship("ProcessingNode", back_populates="children", remote_side=[id], lazy="selectin")
