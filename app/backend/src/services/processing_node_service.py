import logging

from src.core.database import SessionLocal
from src.models.processing_node import NodeType, ProcessingNode

logger = logging.getLogger(__name__)


def create_node(
    document_id: str,
    node_type: str,
    title: str,
    content: str | None = None,
    parent_id: str | None = None,
    position: int = 0,
    metadata: dict | None = None,
    chunk_ids: list[str] | None = None,
) -> ProcessingNode:
    """Create a new ProcessingNode."""
    db = SessionLocal()
    try:
        node = ProcessingNode(
            document_id=document_id,
            node_type=NodeType(node_type),
            title=title,
            content=content,
            parent_id=parent_id,
            position=position,
            metadata=metadata or {},
            chunk_ids=chunk_ids or [],
        )
        db.add(node)
        db.commit()
        db.refresh(node)
        logger.info("Created ProcessingNode %s (type=%s, title=%s)", node.id, node_type, title)
        return node
    finally:
        db.close()


def get_node(node_id: str) -> ProcessingNode | None:
    """Get a ProcessingNode by ID."""
    db = SessionLocal()
    try:
        return db.query(ProcessingNode).filter(ProcessingNode.id == node_id).first()
    finally:
        db.close()


def get_nodes_by_document(document_id: str) -> list[ProcessingNode]:
    """Get all ProcessingNodes for a document, ordered by position."""
    db = SessionLocal()
    try:
        return (
            db.query(ProcessingNode)
            .filter(ProcessingNode.document_id == document_id)
            .order_by(ProcessingNode.position)
            .all()
        )
    finally:
        db.close()


def get_child_nodes(parent_id: str) -> list[ProcessingNode]:
    """Get child nodes of a parent node."""
    db = SessionLocal()
    try:
        return (
            db.query(ProcessingNode)
            .filter(ProcessingNode.parent_id == parent_id)
            .order_by(ProcessingNode.position)
            .all()
        )
    finally:
        db.close()


def update_node(node_id: str, **kwargs) -> ProcessingNode | None:
    """Update a ProcessingNode."""
    db = SessionLocal()
    try:
        node = db.query(ProcessingNode).filter(ProcessingNode.id == node_id).first()
        if not node:
            return None
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
        db.commit()
        db.refresh(node)
        return node
    finally:
        db.close()


def delete_node(node_id: str) -> bool:
    """Delete a ProcessingNode and its children."""
    db = SessionLocal()
    try:
        node = db.query(ProcessingNode).filter(ProcessingNode.id == node_id).first()
        if not node:
            return False
        db.delete(node)
        db.commit()
        return True
    finally:
        db.close()


def delete_nodes_by_document(document_id: str) -> int:
    """Delete all ProcessingNodes for a document."""
    db = SessionLocal()
    try:
        count = db.query(ProcessingNode).filter(ProcessingNode.document_id == document_id).delete()
        db.commit()
        logger.info("Deleted %d ProcessingNodes for document %s", count, document_id)
        return count
    finally:
        db.close()
