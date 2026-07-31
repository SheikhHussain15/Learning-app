# Quickstart: Phase 6 — Production Infrastructure

**Date**: 2026-07-16  
**Feature**: 006-production-infra  
**Branch**: 006-production-infra

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or Docker)
- Git

## Setup (5 minutes)

### 1. Clone and checkout

```bash
git clone <repo-url>
cd "Learning app"
git checkout 006-production-infra
```

### 2. Backend setup

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend setup

```bash
cd app/frontend
npm install
```

### 4. Environment variables

```bash
# Backend
cp .env.example .env
# Edit .env with your configuration

# Frontend
cp .env.local.example .env.local
```

### 5. Start services

```bash
# From project root
docker compose up -d
```

## Verify Installation

### Run tests

```bash
# Backend tests
cd app/backend
pytest

# Frontend tests
cd app/frontend
npm test
```

### Check health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-07-16T21:00:00Z",
  "components": [
    {"name": "database", "status": "healthy", "latency_ms": 5},
    {"name": "chromadb", "status": "healthy", "latency_ms": 12}
  ]
}
```

### View API docs

Open http://localhost:8000/docs in your browser.

## Development Workflow

### Running locally

```bash
# Terminal 1: Backend
cd app/backend
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd app/frontend
npm run dev
```

### Running tests

```bash
# Unit tests
cd app/backend && pytest tests/unit/
cd app/frontend && npm run test:unit

# Contract tests
cd app/backend && pytest tests/contract/

# Integration tests
cd app/backend && pytest tests/integration/

# E2E tests
cd app/frontend && npm run test:e2e
```

### Code quality

```bash
# Backend
cd app/backend
ruff check src/
ruff format src/

# Frontend
cd app/frontend
npm run lint
npm run format
```

## CI/CD Pipeline

The CI/CD pipeline runs automatically on PRs and merges to main.

### Pipeline stages

1. **Code Quality** - Linting and formatting
2. **Type Checking** - TypeScript and Python type validation
3. **Unit Tests** - >90% coverage required
4. **Contract Tests** - Schema validation
5. **Integration Tests** - Database, orchestrator, retrieval
6. **Build** - Frontend and Docker images
7. **Security Scan** - Dependency and container scanning
8. **E2E Tests** - Critical user journeys
9. **Deploy to Staging** - Automatic on merge to main
10. **Deploy to Production** - Manual approval required

### Triggering deployment

```bash
# Staging (automatic on merge to main)
git push origin main

# Production (manual approval in GitHub UI)
# Go to Actions → Deploy to Production → Run workflow
```

## Monitoring

### Langfuse dashboard

Access at http://localhost:3001 (or your Langfuse URL)

- **Traces**: End-to-end request tracking
- **Costs**: AI token usage and costs
- **Latency**: Performance metrics
- **Errors**: Error rates and debugging

### Health checks

```bash
# System health
curl http://localhost:8000/api/v1/health

# Component-specific
curl http://localhost:8000/api/v1/health/database
curl http://localhost:8000/api/v1/health/chromadb
```

## Troubleshooting

### Common issues

**Database connection failed**
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Check connection
psql -h localhost -U postgres -d ai_learning
```

**Langfuse not recording traces**
```bash
# Check Langfuse is running
docker compose ps langfuse

# Check environment variables
echo $LANGFUSE_PUBLIC_KEY
echo $LANGFUSE_SECRET_KEY
```

**Tests failing**
```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_specific.py -v
```

## Next Steps

1. Read [Architecture Overview](docs/architecture.md)
2. Review [Coding Standards](docs/coding-standards.md)
3. Check [Deployment Guide](docs/deployment.md)
4. Explore [Agent Contribution Guide](docs/agents/CONTRIBUTING.md)