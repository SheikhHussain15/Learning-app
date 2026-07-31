---
name: document-management-foundation
description: Implement document management foundation with SQLAlchemy model, Pydantic schemas, and Supabase storage client
source: auto-skill
extracted_at: '2026-07-07T16:10:11.528Z'
---

# Document Management Foundation Skill

This skill guides the implementation of the document management foundation layer for the AI Learning Platform, covering database schema, validation schemas, and storage integration.

## Procedure

### 1. Analyze Specification Requirements
- Review `specs/<feature>/spec.md` for document entity fields
- Review `specs/<feature>/data-model.md` for field constraints
- Identify supported file formats: PDF, DOCX, PPTX, TXT, EPUB, JPG, PNG
- Note document lifecycle states: uploaded, upload_failed, queued_for_processing

### 2. Create Document Model
- Create `app/backend/src/models/document.py`
- Define SQLAlchemy model with fields:
  - id (UUID, primary key)
  - owner_id (String, indexed for queries)
  - title (String(255), required)
  - filename (String(255), required)
  - format (String(50), required)
  - size (Integer, required)
  - status (String(20), default: "uploaded")
  - doc_metadata (Text, optional JSON)
  - created_at/updated_at (DateTime, auto-managed)
- Import and register model in `main.py` for table creation

### 3. Create Pydantic Schemas
- Create `app/backend/src/schemas/document.py`
- Define schemas:
  - `DocumentCreate`: Input validation for uploads
    - title: min_length=1, max_length=255
    - filename, format, size: required
    - doc_metadata: optional dict
  - `DocumentResponse`: Output schema with all fields
  - `DocumentListResponse`: Pagination wrapper
- Enable `from_attributes = True` for ORM compatibility

### 5. Setup Storage Client
- Create `app/backend/src/core/storage.py`
- Use `supabase>=2.0.0` client library
- Read `SUPABASE_URL` and `SUPABASE_KEY` from environment
- Raise `ValueError` if credentials missing
- Export `get_supabase_client()` function

### 6. Update Dependencies
- Add `supabase>=2.0.0` to `app/backend/requirements.txt`
- Update `.env.example` with:
  - SUPABASE_URL
  - SUPABASE_KEY

### 7. Verify Implementation
- Run `python -m py_compile` on all modified files
- Confirm no syntax errors
- Update `tasks.md` with completed checkboxes

## File Structure

```
app/backend/
├── src/
│   ├── models/
│   │   └── document.py      # NEW
│   ├── schemas/
│   │   └── document.py      # NEW
│   ├── core/
│   │   └── storage.py       # NEW
│   ├── main.py              # MODIFIED (import models)
│   └── api/v1/
│       └── __init__.py      # MODIFIED (comment placeholder)
├── requirements.txt         # MODIFIED (supabase)
└── .env.example             # MODIFIED (Supabase env vars)
```

## Dependencies

- `supabase>=2.0.0` - Python client for Supabase Storage
- `sqlalchemy>=2.0.0` - ORM for database models
- `pydantic>=2.0.0` - Data validation using Python type annotations

## Configuration

Required environment variables:
```bash
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
```

## Next Steps

After completing this foundation:
1. T002: Configure Supabase Storage buckets and policies (manual dashboard step)
2. T006-T011: Implement upload endpoint and services
3. T012-T016: Implement library listing, search, delete

## Common Patterns

### Database Session Injection
```python
from src.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Storage Upload Pattern
```python
from src.core.storage import get_supabase_client

bucket = "documents"
client = get_supabase_client()
response = client.storage.from_(bucket).upload(filename, file_data)
```