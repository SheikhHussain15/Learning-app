# Quickstart: AI Agent Orchestration — Phase 4

## Prerequisites

- Python 3.11+
- PostgreSQL running (from Phase 1 foundation)
- OpenRouter API key
- Langfuse account (or self-hosted instance)
- ChromaDB (pip install)
- Phase 3 infrastructure complete (Orchestrator, Echo Agent, retrieval pipeline)

## Install Dependencies

```bash
cd app/backend
pip install pdfplumber python-docx pytesseract Pillow
```

## Database Migration

```bash
# Apply Alembic migration for new tables (ProcessingNode, AgentOutput, ProgressEvent)
alembic upgrade head
```

## Validate Agents

### 1. Start the Backend

```bash
cd app/backend
uvicorn src.main:app --reload
```

### 2. Test Document Processing Agent

```bash
$env:BODY = '{"agent_type":"document_processing","document_id":"doc-test-1","node_ids":[],"agent_params":{},"context":{"chunks":[{"chunk_id":"chunk-1","text":"Chapter 1: Introduction to Python. Python is a versatile programming language.","score":0.95,"metadata":{"page_number":1}}]}}'
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/agents/document_processing/invoke" -Method POST -ContentType "application/json" -Body $env:BODY
```

### 3. Test Knowledge Structuring Agent

```bash
$env:BODY = '{"agent_type":"knowledge_structuring","document_id":"doc-test-1","node_ids":[],"agent_params":{},"context":{"chunks":[{"chunk_id":"chunk-1","text":"Chapter 1: Introduction to Python. Python is versatile.","score":0.95,"metadata":{}},{"chunk_id":"chunk-2","text":"1.1 Variables: Python uses dynamic typing for variables.","score":0.90,"metadata":{}}]}}'
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/agents/knowledge_structuring/invoke" -Method POST -ContentType "application/json" -Body $env:BODY
```

### 4. Test Summary Agent

```bash
$env:BODY = '{"agent_type":"summary","document_id":"doc-test-1","node_ids":["node-1"],"agent_params":{"depth":"concise"},"context":{"chunks":[{"chunk_id":"chunk-1","text":"Python is a versatile language used for web, data science, and AI.","score":0.95,"metadata":{}}]}}'
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/agents/summary/invoke" -Method POST -ContentType "application/json" -Body $env:BODY
```

### 5. Test Quiz Agent

```bash
$env:BODY = '{"agent_type":"quiz","document_id":"doc-test-1","node_ids":["node-1"],"agent_params":{"difficulty":"medium","question_count":5},"context":{"chunks":[{"chunk_id":"chunk-1","text":"Python uses dynamic typing. Variables don't need type declarations.","score":0.95,"metadata":{}}]}}'
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/agents/quiz/invoke" -Method POST -ContentType "application/json" -Body $env:BODY
```

### 6. Test Pipeline Execution

```bash
$env:BODY = '{"document_id":"doc-test-1","user_id":"user-1","requested_agents":["summary","quiz"],"agent_params":{"quiz":{"difficulty":"medium","question_count":3},"summary":{"depth":"concise"}}}'
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/pipeline/invoke" -Method POST -ContentType "application/json" -Body $env:BODY
```

## Verify Responses

### Document Processing Response

```json
{
  "status": "success",
  "output": {
    "raw_text": "Chapter 1: Introduction to Python...",
    "chunks": [{"chunk_id": "chunk-1", "text": "...", "position": 0}],
    "metadata": {"format": "text", "character_count": 1234, "word_count": 200},
    "language": "en"
  },
  "source_refs": [],
  "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
}
```

### Quiz Response

```json
{
  "status": "success",
  "output": {
    "questions": [
      {
        "question": "What does Python use for variable typing?",
        "options": ["Static typing", "Dynamic typing", "No typing", "Explicit declarations"],
        "correct_index": 1,
        "explanation": "Python uses dynamic typing...",
        "difficulty": "medium",
        "source_chunk_ids": ["chunk-1"]
      }
    ],
    "metadata": {"total_questions": 5, "difficulty_distribution": {"easy": 1, "medium": 3, "hard": 1}}
  },
  "source_refs": [{"chunk_id": "chunk-1", "document_id": "doc-test-1"}]
}
```

## Run Tests

```bash
cd app/backend
pytest tests/agents/test_document_processing.py -v
pytest tests/agents/test_knowledge_structuring.py -v
pytest tests/agents/test_summary.py -v
pytest tests/agents/test_explanation.py -v
pytest tests/agents/test_translation.py -v
pytest tests/agents/test_diagram.py -v
pytest tests/agents/test_quiz.py -v
pytest tests/agents/test_revision.py -v
pytest tests/agents/test_progress.py -v
pytest tests/agents/test_recommendation.py -v
pytest tests/orchestrator/test_pipeline.py -v
pytest tests/integration/test_full_pipeline.py -v
```

## Expected Outcomes

- All 10 agents return valid ResponseEnvelopes within 5 seconds
- Document Processing produces clean chunks with metadata
- Knowledge Structuring produces hierarchical ProcessingNode tree
- Summary includes source_chunk_ids for every paragraph
- Quiz questions have correct difficulty distribution
- Diagram generates valid Mermaid/Excalidraw syntax
- Revision produces flashcards with source references
- Progress records events and returns user summary
- Recommendation identifies weak areas and suggests study actions
- Pipeline executes agents in correct dependency order
- Incremental processing skips already-completed agents
- All source_refs link back to valid chunk_ids
- Langfuse traces show complete agent hierarchy
- All tests pass
