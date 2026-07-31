# Development Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

## Quick Start (5 minutes)

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
npm run typecheck
```
