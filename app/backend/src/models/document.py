import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from src.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    format = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="uploaded")
    doc_metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
