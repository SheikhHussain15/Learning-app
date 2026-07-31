---

description: "Task list for Phase 6 — Production Infrastructure"
---

# Tasks: Phase 6 — Production Infrastructure

**Input**: Design documents from `/specs/006-production-infra/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as US1 (Automated Testing) explicitly requires test infrastructure and coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `app/backend/src/`, `app/backend/tests/`
- **Frontend**: `app/frontend/src/`, `app/frontend/tests/`
- **Docs**: `app/docs/`
- **CI/CD**: `.github/workflows/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency installation, and tool configuration

- [x] T001 Install production Python dependencies (structlog, ruff, bandit, pytest-asyncio, pytest-cov) in app/backend/requirements.txt
- [x] T002 [P] Install frontend testing dependencies (jest, @testing-library/react, @testing-library/jest-dom, jest-environment-jsdom) in app/frontend/package.json
- [x] T003 [P] Install Playwright for E2E testing (npm install -D @playwright/test) in app/frontend/package.json
- [x] T004 [P] Configure Ruff linting and formatting in app/backend/pyproject.toml
- [x] T005 [P] Configure pytest with coverage settings in app/backend/pyproject.toml
- [x] T006 [P] Configure Jest for frontend unit tests in app/frontend/jest.config.js
- [x] T007 [P] Configure Playwright for E2E tests in app/frontend/playwright.config.ts
- [x] T008 [P] Add test scripts to frontend package.json (test:unit, test:e2e, test:coverage)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create HealthCheck model in app/backend/src/models/health_check.py
- [x] T010 [P] Create DeploymentRecord model in app/backend/src/models/deployment_record.py
- [x] T011 [P] Create SecurityAuditLog model in app/backend/src/models/security_audit_log.py
- [x] T012 [P] Create TestSuiteResult model in app/backend/src/models/test_suite_result.py
- [x] T013 [P] Create SecretRotationLog model in app/backend/src/models/secret_rotation_log.py
- [x] T014 Create Alembic migration for all new entities in app/backend/migrations/versions/
- [x] T015 Setup structured logging with structlog in app/backend/src/core/logging.py (replace existing logging setup)
- [x] T016 Create base error handler middleware in app/backend/src/middleware/error_handler.py
- [x] T017 [P] Create Pydantic schemas for production entities in app/backend/src/schemas/production.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Automated Testing (Priority: P1) 🎯 MVP

**Goal**: Automated tests run on every code change, catching regressions before production with >90% agent logic coverage.

**Independent Test**: Run full test suite locally (`pytest` + `npm test`) and confirm all tests pass with expected coverage thresholds.

### Implementation for User Story 1

- [x] T018 [P] [US1] Create backend unit tests for agent logic in app/backend/tests/unit/test_agent_logic.py
- [x] T019 [P] [US1] Create backend unit tests for services in app/backend/tests/unit/test_services.py
- [x] T020 [P] [US1] Create backend unit tests for utilities and validators in app/backend/tests/unit/test_utils.py
- [x] T021 [P] [US1] Create contract tests for agent schemas (RequestEnvelope/ResponseEnvelope validation) in app/backend/tests/contract/test_agent_schemas.py
- [x] T022 [P] [US1] Create contract tests for API response schemas in app/backend/tests/contract/test_api_schemas.py
- [x] T023 [US1] Create integration tests for orchestrator pipeline execution in app/backend/tests/integration/test_orchestrator_integration.py
- [x] T024 [P] [US1] Create integration tests for ChromaDB retrieval in app/backend/tests/integration/test_retrieval_integration.py
- [x] T025 [P] [US1] Create integration tests for database CRUD operations in app/backend/tests/integration/test_database_integration.py
- [x] T026 [P] [US1] Create frontend unit test setup with Jest in app/frontend/tests/unit/ (basic component render tests)
- [x] T027 [US1] Create TestSuiteResult service for storing test execution results in app/backend/src/services/test_result_service.py
- [x] T028 [US1] Create test results API endpoint (GET /api/v1/testing/results, POST /api/v1/testing/run) in app/backend/src/api/v1/testing/routes.py
- [x] T029 [US1] Add test data fixtures and synthetic data management in app/backend/tests/conftest.py
- [x] T030 [US1] Verify all tests pass and coverage thresholds met (run pytest --cov and npm test)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Error Handling (Priority: P1)

**Goal**: Users receive clear, actionable error messages when something goes wrong, with internal logging providing full diagnostic context.

**Independent Test**: Trigger various error conditions (network failure, AI provider outage, invalid input) and confirm appropriate user-friendly messages appear with trace IDs logged.

### Implementation for User Story 2

- [x] T031 [US2] Implement backend structured exception handlers (validation, auth, not-found, database, AI provider, unexpected) in app/backend/src/middleware/error_handler.py
- [x] T032 [P] [US2] Create frontend ErrorBoundary component with retry option in app/frontend/src/components/ui/ErrorBoundary.tsx
- [x] T033 [P] [US2] Create frontend error state components (network, auth, AI, upload, retrieval errors) in app/frontend/src/components/ui/ErrorState.tsx
- [x] T034 [US2] Implement retry logic with exponential backoff using Tenacity in app/backend/src/core/retry.py
- [x] T035 [US2] Implement circuit breaker pattern for external dependencies (AI providers, storage, MCP) in app/backend/src/core/circuit_breaker.py
- [x] T036 [US2] Add graceful degradation for AI provider failures (cached responses, fallback models) in app/backend/src/services/agent_service.py
- [x] T037 [US2] Add structured error response format with trace_id, request_id, and user-friendly messages to all API endpoints
- [x] T038 [US2] Add frontend error handling hooks (useErrorHandler) in app/frontend/src/hooks/useErrorHandler.ts
- [x] T039 [US2] Implement sensitive information protection (never log passwords, keys, tokens; redact user IDs) in app/backend/src/core/logging.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Observability (Priority: P1)

**Goal**: Complete visibility into system behavior through structured logging with Langfuse correlation, enabling effective debugging and performance optimization.

**Independent Test**: Make API requests and verify Langfuse traces exist with full context (trace_id, span_id, token usage, latency, cost).

### Implementation for User Story 3

- [x] T040 [US3] Implement Langfuse trace correlation middleware (inject trace_id/span_id into all log entries) in app/backend/src/middleware/logging.py
- [x] T041 [P] [US3] Add structured JSON log formatting with all required fields (timestamp, level, message, service, trace_id, span_id, user_id, request_id, metadata) in app/backend/src/core/logging.py
- [x] T042 [US3] Create health check service (check database, ChromaDB, Langfuse, storage) in app/backend/src/services/health_service.py
- [x] T043 [US3] Implement health check API endpoints (GET /api/v1/health, GET /api/v1/health/{component}) in app/backend/src/api/v1/health/routes.py
- [x] T044 [P] [US3] Add trace_id propagation to all existing API route handlers across app/backend/src/api/v1/
- [x] T045 [US3] Create cost tracking service (AI token usage, latency, cost attribution) in app/backend/src/services/cost_tracking_service.py
- [x] T046 [US3] Implement alerting threshold monitoring (error rate >5%/>10%, latency >5s/>10s) in app/backend/src/core/alerting.py
- [x] T047 [US3] Add observability metadata to agent execution spans (token counts, model, latency) in app/backend/src/agents/base.py
- [x] T048 [US3] Create dashboard data endpoint for real-time system health in app/backend/src/api/v1/dashboard/routes.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 — CI/CD Pipeline (Priority: P2)

**Goal**: Automated deployments so code changes reach production safely and quickly with zero-downtime.

**Independent Test**: Push a change and observe automated deployment to staging; verify health checks pass post-deployment.

### Implementation for User Story 4

- [x] T049 [US4] Create GitHub Actions CI workflow (lint, typecheck, unit tests, contract tests, integration tests, build, security scan) in .github/workflows/ci.yml
- [x] T050 [US4] Create GitHub Actions deployment workflow (staging auto-deploy on main merge, production with manual approval) in .github/workflows/deploy.yml
- [x] T051 [P] [US4] Optimize backend Dockerfile for layer caching and smaller image size in app/backend/Dockerfile
- [x] T052 [P] [US4] Optimize frontend Dockerfile for build caching in app/frontend/Dockerfile
- [x] T053 [US4] Create deployment record service (track deployments, enable rollback) in app/backend/src/services/deployment_service.py
- [x] T054 [US4] Implement deployment API endpoints (GET /api/v1/deploy/status, POST /api/v1/deploy/rollback) in app/backend/src/api/v1/deploy/routes.py
- [x] T055 [US4] Add post-deployment health check verification to deployment workflow
- [x] T056 [US4] Add database migration step to deployment pipeline (backward-compatible migrations before code deploy)
- [x] T057 [US4] Configure Dependabot for automated dependency updates in .github/dependabot.yml

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 — Documentation (Priority: P2)

**Goal**: Comprehensive documentation enabling new contributors to understand the codebase and contribute effectively within 30 minutes of setup.

**Independent Test**: Have a new contributor follow the setup guide from scratch and verify they have a working development environment.

### Implementation for User Story 5

- [x] T058 [P] [US5] Create developer setup guide in app/docs/setup.md
- [x] T059 [P] [US5] Create architecture overview document in app/docs/architecture.md
- [x] T060 [P] [US5] Create coding standards guide (Python Ruff rules, TypeScript ESLint config, commit conventions) in app/docs/coding-standards.md
- [x] T061 [P] [US5] Create deployment guide (environments, zero-downtime process, rollback) in app/docs/deployment.md
- [x] T062 [P] [US5] Create troubleshooting guide (common issues, database, Langfuse, tests) in app/docs/troubleshooting.md
- [x] T063 [US5] Create agent contribution guide (define contract, implement, register, test, document) in app/docs/agents/contributing.md
- [x] T064 [US5] Create CONTRIBUTING.md at project root (PR process, branch strategy, commit conventions, quality gates)

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 — Security (Priority: P2)

**Goal**: User data and AI interactions are secure with defense-in-depth: CSRF protection, rate limiting, audit logging, and dependency scanning.

**Independent Test**: Verify CSRF tokens on state-changing operations, confirm rate limiting returns 429 responses, and security scanning finds zero critical vulnerabilities.

### Implementation for User Story 6

- [x] T065 [US6] Implement CSRF protection middleware (token generation, validation on state-changing operations) in app/backend/src/middleware/csrf.py
- [x] T066 [US6] Implement rate limiting middleware (sliding window: 100 req/min general, 5 attempts/15min auth, 10 req/min AI) in app/backend/src/middleware/rate_limiter.py
- [x] T067 [P] [US6] Create security audit logging service (login events, rate limiting, permission denied, secret access) in app/backend/src/services/security_audit_service.py
- [x] T068 [P] [US6] Create secret rotation logging service in app/backend/src/services/secret_service.py
- [x] T069 [US6] Implement security audit log API endpoint (GET /api/v1/security/audit-log with filtering) in app/backend/src/api/v1/security/routes.py
- [x] T070 [US6] Add Bandit security scanning configuration in app/backend/.bandit
- [x] T071 [US6] Configure CORS restrictions for production origins in app/backend/src/main.py
- [x] T072 [US6] Add document ownership validation to all data access endpoints
- [x] T073 [US6] Add secure logging practices (redact PII, never log secrets) enforced across all logging call sites

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T074 [P] Performance optimization: add database query indexing for hot paths in app/backend/src/models/
- [x] T075 [P] Code cleanup: run Ruff auto-fix and ESLint --fix across codebase
- [x] T076 [P] Create E2E tests for critical user journeys (login, upload, AI processing, quiz, flashcards) in app/frontend/tests/e2e/
- [x] T077 Run quickstart.md validation (verify setup, tests, health check, API docs all work end-to-end)
- [x] T078 [P] Update existing ARCHITECTURE.md at project root with production infrastructure additions
- [x] T079 Security hardening: verify all endpoints have proper auth, rate limiting, and input validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (Testing), US2 (Error Handling), US3 (Observability) are P1 and can proceed in parallel
  - US4 (CI/CD) can start after US1 (needs test infrastructure) and US3 (needs observability)
  - US5 (Documentation) can start after US2-US4 are largely complete
  - US6 (Security) can start after US2 (needs error handling framework)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Testing)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - Error Handling)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1 - Observability)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2 - CI/CD)**: Depends on US1 (test infrastructure needed for CI) and US3 (observability needed for deployment monitoring)
- **User Story 5 (P2 - Documentation)**: Depends on US2-US4 being substantially complete (documents existing behavior)
- **User Story 6 (P2 - Security)**: Depends on US2 (error handling framework for security events)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004, T005, T006, T007, T008)
- All Foundational model tasks marked [P] can run in parallel (T010, T011, T012, T013)
- US1, US2, US3 can all start in parallel after Phase 2 completes
- Within US1: all unit and contract test tasks marked [P] can run in parallel (T018-T022, T024-T026)
- Within US2: frontend error components can run in parallel (T032, T033)
- Within US3: logging tasks can run in parallel (T040, T041, T044)
- Within US5: all documentation tasks marked [P] can run in parallel (T058-T062)
- Within US6: audit and secret services can run in parallel (T067, T068)
- Different user stories can be worked on simultaneously by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all unit and contract tests together:
Task: "Create backend unit tests for agent logic in app/backend/tests/unit/test_agent_logic.py"
Task: "Create backend unit tests for services in app/backend/tests/unit/test_services.py"
Task: "Create backend unit tests for utilities and validators in app/backend/tests/unit/test_utils.py"
Task: "Create contract tests for agent schemas in app/backend/tests/contract/test_agent_schemas.py"
Task: "Create contract tests for API response schemas in app/backend/tests/contract/test_api_schemas.py"
Task: "Create frontend unit test setup in app/frontend/tests/unit/"
```

---

## Parallel Example: User Story 3

```bash
# Launch observability tasks together:
Task: "Implement Langfuse trace correlation middleware in app/backend/src/middleware/logging.py"
Task: "Add structured JSON log formatting in app/backend/src/core/logging.py"
Task: "Add trace_id propagation to all existing API route handlers"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Automated Testing)
4. **STOP and VALIDATE**: Run full test suite, verify coverage thresholds
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Testing) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Error Handling) → Test independently → Deploy/Demo
4. Add User Story 3 (Observability) → Test independently → Deploy/Demo
5. Add User Story 4 (CI/CD) → Test independently → Deploy/Demo
6. Add User Story 5 (Documentation) → Test independently → Deploy/Demo
7. Add User Story 6 (Security) → Test independently → Deploy/Demo
8. Polish → Final validation → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Testing)
   - Developer B: User Story 2 (Error Handling)
   - Developer C: User Story 3 (Observability)
3. After P1 stories:
   - Developer A: User Story 4 (CI/CD)
   - Developer B: User Story 5 (Documentation)
   - Developer C: User Story 6 (Security)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests pass before implementing (for US1: write tests first, ensure they fail)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
