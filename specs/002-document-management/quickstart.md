# Quickstart: Document Management

1. **Prerequisites**:
   - Docker (for PostgreSQL)
   - Node.js/npm (for frontend)
   - Python/pip (for backend)
   - Supabase project for storage

2. **Setup**:
   - Ensure `docker-compose.yml` is running to start PostgreSQL.
   - Configure `.env` with Supabase project credentials.
   - Install backend dependencies (`pip install -r backend/requirements.txt`).
   - Install frontend dependencies (`cd app/frontend && npm install`).

3. **Supabase Storage Setup**:
   - Run `supabase/storage/documents-bucket.sql` in the Supabase SQL Editor.
   - This creates the `documents` bucket with:
     - Private access (non-public bucket)
     - 50MB file size limit
     - Allowed MIME types: PDF, DOCX, PPTX, TXT, EPUB, JPG, PNG
     - Row Level Security policies enforcing user ownership

4. **Running**:
   - `npm run dev` to start concurrent frontend and backend services.

5. **API Endpoints**:
   - `POST /api/v1/document/upload` — Upload a document (multipart form)
   - `GET /api/v1/document/list?owner_id={id}&page=1&per_page=20` — List documents with pagination
   - `GET /api/v1/document/list?owner_id={id}&q={search}` — Search documents by title/filename
   - `DELETE /api/v1/document/delete/{id}` — Delete a document

6. **Document Lifecycle States**:
   - `uploaded` — File stored and record created
   - `upload_failed` — Error during storage or record creation
   - `queued_for_processing` — Awaiting future AI tasks

7. **Supported File Types**: PDF, DOCX, PPTX, TXT, EPUB, JPG, PNG (max 50MB)
