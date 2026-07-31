from sqlalchemy.orm import Session

from src.models.test_suite_result import TestSuiteResult, TestSuiteType


class TestResultService:
    def __init__(self, db: Session):
        self.db = db

    def create_result(
        self,
        suite_type: TestSuiteType,
        total_tests: int,
        passed: int,
        failed: int,
        skipped: int = 0,
        coverage_percent: float | None = None,
        duration_seconds: int = 0,
        commit_sha: str | None = None,
    ) -> TestSuiteResult:
        result = TestSuiteResult(
            suite_type=suite_type.value,
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            coverage_percent=coverage_percent,
            duration_seconds=duration_seconds,
            commit_sha=commit_sha,
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def get_results(
        self,
        suite_type: TestSuiteType | None = None,
        limit: int = 10,
    ) -> list[TestSuiteResult]:
        query = self.db.query(TestSuiteResult)
        if suite_type:
            query = query.filter(TestSuiteResult.suite_type == suite_type.value)
        return query.order_by(TestSuiteResult.run_at.desc()).limit(limit).all()
