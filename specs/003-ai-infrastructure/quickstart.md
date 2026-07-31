# Quickstart: AI Infrastructure — Phase 3

## Prerequisites

- Python 3.11+
- PostgreSQL running (from Phase 1 foundation)
- OpenRouter API key
- Langfuse account (or self-hosted instance)
- ChromaDB (pip install)

## Environment Setup

Add to `app/backend/.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
CHROMA_DB_PATH=./data/chromadb
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
TOP_K_RETRIEVAL=10
MIN_SIMILARITY_THRESHOLD=0.5
AGENT_MAX_RETRIES=3
AGENT_TIMEOUT_SECONDS=60
ORCHESTRATOR_TIMEOUT_SECONDS=300
LOG_LEVEL=INFO
```

## Install Dependencies

```bash
cd app/backend
pip install openai-agents chromadb llama-index langfuse tenacity
```

## Database Migration

Run the AgentRun table migration:

```bash
# Apply Alembic migration for agent_runs table
alembic upgrade head
```

## Validate Infrastructure

### 1. Start the Backend

```bash
cd app/backend
uvicorn src.main:app --reload
```

### 2. Invoke the Echo Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents/echo/invoke \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <session_token>" \
  -d '{
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "node_ids": ["550e8400-e29b-41d4-a716-446655440001"],
    "agent_params": {"test": true},
    "context": {
      "chunks": [
        {"chunk_id": "chunk-1", "text": "Test content", "score": 0.95, "metadata": {}}
      ]
    }
  }'
```

### 3. Verify Response

Expected response:

```json
{
  "status": "success",
  "run_id": "...",
  "response": {
    "status": "success",
    "output": {
      "echoed_document_id": "550e8400-e29b-41d4-a716-446655440000",
      "echoed_node_ids": ["550e8400-e29b-41d4-a716-446655440001"],
      "echoed_trace_id": "...",
      "received_agent_params": {"test": true}
    },
    "source_refs": [],
    "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
    "error": null
  },
  "duration_ms": ...
}
```

### 4. Verify Langfuse Trace

Check Langfuse dashboard for a trace with:
- Name: `agent.echo.invoke`
- Status: `success`
- Model: `gpt-4o-mini`
- Token usage: 50/20/70

### 5. Verify AgentRun in Database

```bash
# Connect to PostgreSQL and query:
SELECT id, status, retry_count, duration_ms, model_used
FROM agent_runs
WHERE agent_type = 'echo'
ORDER BY created_at DESC
LIMIT 1;
```

## Run Tests

```bash
cd app/backend
pytest tests/agents/ -v           # Contract + Echo Agent tests
pytest tests/orchestrator/ -v     # Orchestrator lifecycle tests
pytest tests/retrieval/ -v        # Indexing + retrieval tests
pytest tests/tracing/ -v          # Langfuse integration tests
```

## Expected Outcomes

- Echo Agent returns valid ResponseEnvelope within 5 seconds
- AgentRun transitions: queued → running → succeeded
- Langfuse trace created with complete hierarchy
- All tests pass
