import pytest
from datetime import datetime
from src.models.test_suite_result import TestSuiteResult, TestSuiteType
from src.services.test_result_service import TestResultService


class TestTestResultService:
    def test_create_result(self, db):
        service = TestResultService(db)
        result = service.create_result(
            suite_type=TestSuiteType.unit,
            total_tests=100,
            passed=98,
            failed=2,
            skipped=0,
            coverage_percent=92.5,
            duration_seconds=45,
            commit_sha="abc123",
        )
        assert result.id is not None
        assert result.suite_type == TestSuiteType.unit.value
        assert result.total_tests == 100
        assert result.passed == 98
        assert result.failed == 2
        assert result.coverage_percent == 92.5

    def test_get_results(self, db):
        service = TestResultService(db)
        service.create_result(
            suite_type=TestSuiteType.unit,
            total_tests=50,
            passed=50,
            failed=0,
            duration_seconds=20,
        )
        service.create_result(
            suite_type=TestSuiteType.contract,
            total_tests=30,
            passed=29,
            failed=1,
            duration_seconds=15,
        )
        results = service.get_results()
        assert len(results) == 2

    def test_get_results_by_type(self, db):
        service = TestResultService(db)
        service.create_result(suite_type=TestSuiteType.unit, total_tests=10, passed=10, failed=0, duration_seconds=5)
        service.create_result(suite_type=TestSuiteType.e2e, total_tests=5, passed=4, failed=1, duration_seconds=30)
        results = service.get_results(suite_type=TestSuiteType.unit)
        assert len(results) == 1
        assert results[0].suite_type == TestSuiteType.unit.value

    def test_get_results_with_limit(self, db):
        service = TestResultService(db)
        for i in range(5):
            service.create_result(suite_type=TestSuiteType.unit, total_tests=10, passed=10, failed=0, duration_seconds=5)
        results = service.get_results(limit=3)
        assert len(results) == 3
