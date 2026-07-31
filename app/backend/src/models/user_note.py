from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func

from src.core.database import Base


class UserNote(Base):
    __tablename__ = "user_notes"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    document_id = Column(String, nullable=False, index=True)
    section_id = Column(String, nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = ()
