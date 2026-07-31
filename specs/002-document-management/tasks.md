# Tasks: Document Management Foundation

**Input**: Design documents from `/specs/002-document-management/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

## Task Summary

| User Story | Priority | Independent Test | Tasks Count |
|------------|----------|------------------|-------------|
| US1: Secure Document Upload | P1 | Upload and verify appearance | 6 |
| US2: Discovery & Management | P1 | Search, filter, delete | 5 |

**Total Tasks**: 16 (includes setup/foundation)
**Parallel Opportunities**: 7 tasks marked [P]

---

## Phase 1: Setup (Infrastructure)

**Goal**: Prepare the project for document management

- [x] T001 Initialize database schema for Document entity in backend
- [x] T002 [P] Configure Supabase Storage buckets and policies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create infrastructure required for document operations

- [x] T003 Create Document SQLAlchemy model in app/backend/src/models/document.py
- [x] T004 [P] Create Pydantic schemas in app/backend/src/schemas/document.py
- [x] T005 [P] Setup storage client in app/backend/src/core/storage.py

---

## Phase 3: US1 - Secure Document Upload

**Goal**: Enable users to upload documents securely

**Independent Test**: Upload a valid PDF file and verify its appearance in the library.

- [x] T006 [P] [US1] Implement upload endpoint in app/backend/src/api/v1/document/upload.py
- [x] T007 [P] [US1] Implement storage upload service in app/backend/src/services/storage_service.py
- [x] T009 [US1] Implement server-side validation in app/backend/src/middleware/validation.py
- [x] T010 [US1] Add MIME type sanitization in app/backend/src/utils/security.py
- [x] T011 [US1] Test full upload → storage → record creation flow

---

## Phase 4: US2 - Discovery & Management

**Goal**: Allow users to manage their documents

**Independent Test**: Upload documents, search for them, and delete one.

- [x] T012 [P] [US2] Implement library list endpoint in app/backend/src/api/v1/document/list.py
- [x] T013 [P] [US2] Implement document search service in app/backend/src/services/search_service.py
- [x] T014 [P] [US2] Create library list page in app/frontend/src/app/library/page.tsx
- [x] T015 [US2] Implement delete endpoint in app/backend/src/api/v1/document/delete.py
- [x] T016 [US2] Test search and deletion persistence

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Finalize quality and logging

- [x] T017 Add request logging for upload/delete events
- [x] T018 Verify all documents are private to the owner
- [x] T019 Update quickstart.md with document usage steps

---

## Implementation Strategy

**MVP Scope**:
1. Document Model & Schema setup
2. Secure Upload workflow
3. Basic Library listing and deletion

**Incremental Delivery**:
- Phase 1 & 2: Infrastructure ready
- Phase 3: Upload capability
- Phase 4: Library management & Search
- Phase 5: Logging & Security
