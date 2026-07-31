# Architecture Overview

## System Architecture

The AI Learning Platform is a monorepo web application with:

- **Backend**: Python 3.11+ with FastAPI, SQLAlchemy, Pydantic
- **Frontend**: TypeScript with Next.js 15, React 18, Tailwind CSS
- **Storage**: PostgreSQL 15 (prod), SQLite (dev), ChromaDB (vectors)
- **Observability**: Langfuse for tracing, structlog for structured logging

## Project Structure

```
app/
├── backend/           # FastAPI backend
│   ├── src/           # Application code
│   │   ├── api/v1/    # API route handlers
│   │   ├── services/  # Business logic
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── agents/    # AI agents
│   │   ├── orchestrator/ # Pipeline orchestration
│   │   ├── retrieval/ # ChromaDB retrieval
│   │   ├── tracing/   # Langfuse integration
│   │   └── core/      # Config, middleware, security
│   └── tests/         # Test suites
├── frontend/          # Next.js frontend
│   ├── src/           # Application code
│   │   ├── app/       # App Router pages
│   │   ├── components/ # React components
│   │   ├── hooks/     # React hooks
│   │   ├── services/  # API services
│   │   └── types/     # TypeScript types
│   └── tests/         # Test suites
├── docs/              # Documentation
└── .github/workflows/ # CI/CD pipelines
```

## Key Components

### API Layer (FastAPI)
- Route handlers in `src/api/v1/`
- Pydantic validation for request/response schemas
- Dependency injection for database sessions

### Service Layer
- Business logic in `src/services/`
- Agent orchestration and pipeline management
- Health checks and observability

### AI Agents
- Base agent class in `src/agents/base.py`
- Registry pattern for agent management
- Langfuse tracing for all agent executions

### Data Layer
- SQLAlchemy models in `src/models/`
- Alembic migrations in `migrations/`
- ChromaDB for vector storage

## Production Infrastructure

### Error Handling
- Structured exception handlers in `src/middleware/error_handler.py`
- Circuit breaker pattern for external dependencies
- Retry logic with exponential backoff

### Observability
- Structured JSON logging with structlog
- Langfuse trace correlation
- Health check endpoints
- Cost tracking for AI operations

### Testing
- Unit tests: `tests/unit/`
- Contract tests: `tests/contract/`
- Integration tests: `tests/integration/`
- E2E tests: `tests/e2e/` (frontend)

### CI/CD
- GitHub Actions for automated testing and deployment
- Multi-stage Docker builds
- Zero-downtime deployments
