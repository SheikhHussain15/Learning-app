# Architecture: AI Learning Platform

## Overview

Monorepo with Next.js frontend and FastAPI backend, sharing a PostgreSQL database.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 18, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.11+, SQLAlchemy 2.x, Pydantic 2 |
| Database | PostgreSQL 15 (prod), SQLite (dev/testing) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Storage | Supabase Storage |
| AI Agents | openai-agents, Langfuse tracing |
| Vectors | ChromaDB |
| Observability | Langfuse, structlog |
| Testing | pytest + Jest + Playwright |
| CI/CD | GitHub Actions |
| Linting | Ruff (Python), ESLint + Prettier (TypeScript) |

## Project Structure

```
app/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/# React components
│   │   ├── hooks/     # React hooks
│   │   ├── services/  # API services
│   │   └── types/     # TypeScript types
│   └── tests/         # Jest + Playwright tests
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── api/v1/    # Route handlers
│   │   ├── services/  # Business logic
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── agents/    # AI agents
│   │   ├── orchestrator/ # Pipeline orchestration
│   │   ├── retrieval/ # ChromaDB retrieval
│   │   ├── tracing/   # Langfuse integration
│   │   ├── core/      # Config, logging, security
│   │   └── middleware/ # Error handling, CSRF, rate limiting
│   └── tests/         # pytest test suites
├── docs/              # Documentation
└── .github/workflows/ # CI/CD pipelines
```

## Production Infrastructure

### Error Handling
- Structured exception handlers with user-friendly messages
- Circuit breaker pattern for external dependencies
- Retry logic with exponential backoff

### Observability
- Structured JSON logging with structlog
- Langfuse trace correlation for AI operations
- Health check endpoints for all components
- Cost tracking for AI token usage

### Testing
- Unit tests (>90% coverage for agent logic)
- Contract tests for schema validation
- Integration tests for orchestrator and database
- E2E tests with Playwright

### Security
- CSRF protection on state-changing operations
- Rate limiting (100 req/min general, 5/15min auth)
- Security audit logging
- Secret rotation tracking
- Bandit security scanning

### CI/CD
- GitHub Actions for automated testing and deployment
- Multi-stage Docker builds with layer caching
- Zero-downtime deployments
- Automated dependency updates via Dependabot

## Phases

1. **Foundation** — Auth, user management, project structure
2. **Document Management** — Upload, list, search, delete documents
3. **AI Infrastructure** — Agents, orchestration, retrieval
4. **AI Agent Orchestration** — Pipeline execution, state management
5. **Learning Experience** — Quizzes, flashcards, tutor, workspace
6. **Production Infrastructure** — Error handling, testing, CI/CD, security
