import enum
import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base


class TestSuiteType(enum.StrEnum):
    unit = "unit"
    contract = "contract"
    integration = "integration"
    e2e = "e2e"


class TestSuiteResult(Base):
    __tablename__ = "test_suite_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    suite_type = Column(String(20), nullable=False, index=True)
    total_tests = Column(Integer, nullable=False, default=0)
    passed = Column(Integer, nullable=False, default=0)
    failed = Column(Integer, nullable=False, default=0)
    skipped = Column(Integer, nullable=False, default=0)
    coverage_percent = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=False, default=0)
    run_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    commit_sha = Column(String(40), nullable=True)
