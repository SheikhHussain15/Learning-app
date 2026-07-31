# Learning app Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-07-10

## Active Technologies
- Python 3.11+ (backend) + openai-agents, chromadb, llama-index, langfuse, fastapi, sqlalchemy, pydantic, tenacity (004-ai-agent-orchestration)
- SQLite dev / PostgreSQL prod (AgentRun, AgentOutput, ProcessingNode), ChromaDB (vector embeddings) (004-ai-agent-orchestration)
- Python 3.11+ (backend), TypeScript/Next.js 15 (frontend) + FastAPI, React 18, Tailwind CSS, SQLAlchemy 2.x, Pydantic 2, Mermaid.js (005-learning-experience)
- PostgreSQL (progress, quiz attempts, flashcard reviews), ChromaDB (vector retrieval for AI Tutor) (005-learning-experience)
- Python 3.11+ (backend), TypeScript 5.x (frontend) + FastAPI, Next.js 14+, SQLAlchemy 2.x, Pydantic 2, Jest, pytest, Ruff, ESLint, Prettier, Langfuse SDK, Tenacity (006-production-infra)
- PostgreSQL 15 (prod), SQLite (dev), ChromaDB (vectors) (006-production-infra)

- Python 3.11+ (backend), TypeScript (frontend) + openai-agents, chromadb, llama-index, langfuse, fastapi, sqlalchemy, pydantic (003-ai-infrastructure)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src; pytest; ruff check .
**Frontend**: `cd app/frontend; npm run dev`
**Docker**: `docker compose up --build` (from project root)

## Code Style

Python 3.11+ (backend), TypeScript (frontend): Follow standard conventions

## Recent Changes
- 006-production-infra: Added Python 3.11+ (backend), TypeScript 5.x (frontend) + FastAPI, Next.js 14+, SQLAlchemy 2.x, Pydantic 2, Jest, pytest, Ruff, ESLint, Prettier, Langfuse SDK, Tenacity
- 005-learning-experience: Added Python 3.11+ (backend), TypeScript/Next.js 15 (frontend) + FastAPI, React 18, Tailwind CSS, SQLAlchemy 2.x, Pydantic 2, Mermaid.js
- 004-ai-agent-orchestration: Added Python 3.11+ (backend) + openai-agents, chromadb, llama-index, langfuse, fastapi, sqlalchemy, pydantic, tenacity


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
