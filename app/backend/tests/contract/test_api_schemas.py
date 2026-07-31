import pytest
from pydantic import ValidationError
from src.schemas.production import (
    HealthCheckResponse,
    ComponentHealth,
    DeploymentStatusResponse,
    AuditLogEntry,
    TestResultResponse,
    TestRunRequest,
    TestRunResponse,
)
from datetime import datetime


class TestHealthCheckResponseContract:
    def test_valid_healthy(self):
        resp = HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now(),
            components=[],
        )
        assert resp.status == "healthy"

    def test_valid_with_components(self):
        resp = HealthCheckResponse(
            status="degraded",
            timestamp=datetime.now(),
            components=[
                ComponentHealth(name="database", status="healthy", latency_ms=5),
                ComponentHealth(name="chromadb", status="degraded", latency_ms=150, error="slow"),
            ],
        )
        assert len(resp.components) == 2

    def test_invalid_status_fails(self):
        with pytest.raises(ValidationError):
            HealthCheckResponse(status="invalid", timestamp=datetime.now(), components=[])


class TestComponentHealthContract:
    def test_valid(self):
        comp = ComponentHealth(name="backend", status="healthy", latency_ms=10)
        assert comp.latency_ms == 10

    def test_negative_latency_fails(self):
        with pytest.raises(ValidationError):
            ComponentHealth(name="backend", status="healthy", latency_ms=-1)


class TestDeploymentStatusResponseContract:
    def test_valid(self):
        resp = DeploymentStatusResponse(
            current_version="1.0.0",
            environment="production",
            deployed_at=datetime.now(),
            deployed_by="ci-bot",
            rollback_available=True,
        )
        assert resp.rollback_available is True

    def test_invalid_environment_fails(self):
        with pytest.raises(ValidationError):
            DeploymentStatusResponse(
                current_version="1.0.0",
                environment="dev",
                deployed_at=datetime.now(),
                deployed_by="ci-bot",
                rollback_available=False,
            )


class TestAuditLogEntryContract:
    def test_valid(self):
        entry = AuditLogEntry(
            id="log-1",
            event_type="login_success",
            user_id="user-1",
            ip_address="127.0.0.1",
            details={},
            created_at=datetime.now(),
        )
        assert entry.event_type == "login_success"

    def test_from_attributes(self):
        entry = AuditLogEntry(
            id="log-1",
            event_type="rate_limit",
            created_at=datetime.now(),
        )
        assert entry.user_id is None


class TestTestResultResponseContract:
    def test_valid(self):
        result = TestResultResponse(
            id="run-1",
            suite_type="unit",
            total_tests=100,
            passed=98,
            failed=2,
            duration_seconds=30,
            run_at=datetime.now(),
            commit_sha="abc123",
        )
        assert result.failed == 2

    def test_defaults(self):
        result = TestResultResponse(
            id="run-1",
            suite_type="e2e",
            total_tests=10,
            passed=10,
            failed=0,
            duration_seconds=60,
            run_at=datetime.now(),
        )
        assert result.skipped == 0


class TestTestRunRequestContract:
    def test_default_values(self):
        req = TestRunRequest()
        assert req.suite_type == "all"
        assert req.parallel is True

    def test_valid_custom(self):
        req = TestRunRequest(suite_type="unit", parallel=False)
        assert req.suite_type == "unit"
        assert req.parallel is False

    def test_invalid_suite_type_fails(self):
        with pytest.raises(ValidationError):
            TestRunRequest(suite_type="invalid")
