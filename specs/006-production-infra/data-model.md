# Data Model: Phase 6 — Production Infrastructure

**Date**: 2026-07-16  
**Feature**: 006-production-infra  
**Branch**: 006-production-infra

## Overview

Phase 6 adds production infrastructure entities that support observability, testing, and deployment. These entities extend the existing data model without modifying core business entities.

## Entities

### HealthCheck

Represents automated health check results for system components.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| component | string | Component name (frontend, backend, database, chromadb) |
| status | enum | healthy, degraded, unhealthy |
| latency_ms | integer | Response time in milliseconds |
| error_message | string | Error details if unhealthy |
| checked_at | timestamp | When check was performed |

**Relationships**: None (standalone monitoring entity)

**State Transitions**: healthy ↔ degraded ↔ unhealthy

---

### DeploymentRecord

Tracks deployment history for rollback and audit purposes.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| version | string | Semantic version (MAJOR.MINOR.PATCH) |
| environment | enum | staging, production |
| status | enum | pending, in_progress, success, failed, rolled_back |
| deployed_by | string | User or system that initiated deploy |
| deployed_at | timestamp | When deployment started |
| completed_at | timestamp | When deployment finished |
| rollback_from | UUID | Reference to previous version if rolled back |

**Relationships**: Self-referential for rollback tracking

**State Transitions**: pending → in_progress → success | failed → rolled_back

---

### SecurityAuditLog

Records security-relevant events for compliance and investigation.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| event_type | enum | login_success, login_failure, rate_limit, permission_denied, secret_access |
| user_id | string | Redacted user identifier |
| ip_address | string | Client IP (anonymized in logs) |
| user_agent | string | Client user agent |
| details | jsonb | Event-specific metadata |
| created_at | timestamp | When event occurred |

**Relationships**: References User (existing entity)

**State Transitions**: None (append-only log)

---

### TestSuiteResult

Stores automated test execution results for trend analysis.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| suite_type | enum | unit, contract, integration, e2e |
| total_tests | integer | Total tests executed |
| passed | integer | Tests passed |
| failed | integer | Tests failed |
| skipped | integer | Tests skipped |
| coverage_percent | decimal | Code coverage percentage |
| duration_seconds | integer | Total execution time |
| run_at | timestamp | When tests were executed |
| commit_sha | string | Git commit being tested |

**Relationships**: References DeploymentRecord

**State Transitions**: None (append-only record)

---

### SecretRotationLog

Tracks secret rotation events for security compliance.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| secret_type | enum | ai_key, db_password, jwt_secret, storage_key |
| rotated_at | timestamp | When rotation occurred |
| rotated_by | string | User or system that performed rotation |
| previous_rotation | timestamp | When previous rotation occurred |

**Relationships**: None (audit log)

**State Transitions**: None (append-only log)

---

## Existing Entity Extensions

### ProgressEvent (existing)

No schema changes. Phase 6 adds observability correlation:

- All ProgressEvent records now include `trace_id` field for Langfuse correlation
- Existing `metadata` JSON field captures additional context

### PipelineRun (existing)

No schema changes. Phase 6 adds:

- Enhanced error tracking with structured error objects
- Retry count and backoff state tracking

---

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| HealthCheck | status | Must be one of: healthy, degraded, unhealthy |
| HealthCheck | latency_ms | Must be >= 0 |
| DeploymentRecord | version | Must follow semantic versioning |
| DeploymentRecord | status | Must follow state transition rules |
| SecurityAuditLog | event_type | Must be one of defined enum values |
| TestSuiteResult | coverage_percent | Must be between 0 and 100 |
| TestSuiteResult | failed | Must be 0 for production deployments |

---

## Migration Strategy

Phase 6 entities are additive — no existing tables are modified.

1. Create new tables: health_check, deployment_record, security_audit_log, test_suite_result, secret_rotation_log
2. Add `trace_id` column to existing ProgressEvent table (nullable for backward compatibility)
3. All migrations are backward compatible and reversible

---

## Indexes

| Entity | Index | Purpose |
|--------|-------|---------|
| HealthCheck | component, checked_at | Dashboard queries |
| DeploymentRecord | environment, deployed_at | Rollback queries |
| SecurityAuditLog | event_type, created_at | Audit queries |
| TestSuiteResult | suite_type, run_at | Trend analysis |
| SecretRotationLog | secret_type, rotated_at | Compliance queries |