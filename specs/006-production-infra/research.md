# Research: Phase 6 — Production Infrastructure

**Date**: 2026-07-16  
**Feature**: 006-production-infra  
**Branch**: 006-production-infra

## Research Tasks

### R1: Error Handling Patterns for FastAPI + Next.js

**Decision**: Implement structured exception handling with FastAPI exception handlers and Next.js error boundaries.

**Rationale**: 
- FastAPI provides `@app.exception_handler` for centralized backend error handling
- Next.js App Router provides `error.tsx` files for component-level error boundaries
- Both support structured error responses with trace IDs

**Alternatives Considered**:
- Custom middleware only: Less granular, harder to test
- Third-party error tracking (Sentry): Adds dependency, reduces control

---

### R2: Structured Logging with Langfuse Correlation

**Decision**: Use Python `structlog` for backend, custom logger for frontend, with Langfuse `trace_id` injection.

**Rationale**:
- `structlog` provides JSON-structured logs out of the box
- Langfuse SDK provides `trace_id` and `span_id` for correlation
- Correlation ID propagation via request context middleware

**Alternatives Considered**:
- Standard `logging` module: Less structured, harder to parse
- ELK stack: Overkill for initial deployment

---

### R3: Testing Framework Selection

**Decision**: pytest (backend), Jest (frontend), Playwright (E2E).

**Rationale**:
- pytest: Industry standard for Python, excellent async support
- Jest: Fast, built-in mocking, React Testing Library integration
- Playwright: Cross-browser, auto-wait, trace viewer

**Alternatives Considered**:
- unittest: More verbose, less feature-rich
- Cypress: Slower, less browser support
- Vitest: Newer, less ecosystem maturity

---

### R4: CI/CD Pipeline Implementation

**Decision**: GitHub Actions with multi-stage pipeline.

**Rationale**:
- GitHub Actions native to repository
- Supports matrix builds, caching, secrets
- Free for public repos, reasonable for private

**Alternatives Considered**:
- GitLab CI: Requires GitLab migration
- Jenkins: Self-hosted, maintenance burden
- CircleCI: External dependency

---

### R5: Rate Limiting Implementation

**Decision**: In-memory rate limiting with Redis backing for distributed scenarios.

**Rationale**:
- FastAPI middleware for request-level limiting
- Redis for cross-instance coordination
- Sliding window algorithm for accuracy

**Alternatives Considered**:
- Database-only: Too slow for rate limiting
- External service (Kong): Adds infrastructure complexity

---

### R6: Secret Management Strategy

**Decision**: Environment variables with `.env` files for development, secrets manager for production.

**Rationale**:
- Environment variables: Standard, Docker-compatible
- `.env` files: Easy local development
- Production secrets: Cloud provider secrets manager

**Alternatives Considered**:
- Vault: Overkill for current scale
- AWS Secrets Manager: Vendor lock-in

---

### R7: Documentation Generation

**Decision**: Auto-generate API docs from OpenAPI, manual guides for architecture/setup.

**Rationale**:
- FastAPI auto-generates OpenAPI spec
- Swagger UI available at `/docs`
- Architecture docs need human curation

**Alternatives Considered**:
- ReadTheDocs: External hosting, maintenance
- GitBook: Proprietary, less control

---

### R8: Circuit Breaker Pattern

**Decision**: Implement custom circuit breaker with Tenacity for AI provider calls.

**Rationale**:
- Tenacity already in stack for retry logic
- Custom implementation for full control
- State machine: closed → open → half-open

**Alternatives Considered**:
- pybreaker: Less flexible, adds dependency
- External service: Too heavy

---

### R9: E2E Test Strategy

**Decision**: Playwright with page object model, running against staging environment.

**Rationale**:
- Page objects reduce test maintenance
- Staging environment matches production
- Parallel execution for speed

**Alternatives Considered**:
- Cypress: Slower, less browser support
- Selenium: Legacy, more setup

---

### R10: Security Scanning Integration

**Decision**: Dependabot for dependency scanning, Trivy for container scanning, Bandit for Python security.

**Rationale**:
- Dependabot: Native GitHub integration
- Trivy: Fast, comprehensive container scanning
- Bandit: Python-specific security linting

**Alternatives Considered**:
- Snyk: External dependency, cost
- OWASP ZAP: More for runtime testing

---

## Summary

All research tasks resolved with clear decisions. No NEEDS CLARIFICATION items remain. All decisions align with existing tech stack and Constitution principles.