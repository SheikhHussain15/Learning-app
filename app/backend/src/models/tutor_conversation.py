from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.sql import func

from src.core.database import Base


class TutorConversation(Base):
    __tablename__ = "tutor_conversations"

    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    messages = Column(JSON, nullable=False, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = ()
