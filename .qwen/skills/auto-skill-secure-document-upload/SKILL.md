---
name: secure-document-upload
description: Implement secure document upload workflow with validation, MIME type checking, and error handling

source: auto-skill
extracted_at: '2026-07-09T12:30:00.000Z'
---

# Secure Document Upload Skill

This skill guides the implementation of a secure document upload workflow for the AI Learning Platform, covering frontend integration, backend validation, MIME type sanitization, and comprehensive error handling for the complete upload-to-storage-to-database pipeline.

## Procedure

### 1. Implement Upload Endpoint
- Create `app/backend/src/api/v1/document/upload.py`
- Define POST `/api/v1/document/document/upload` endpoint
- Integrate FastAPI UploadFile handling with dependency injection for database sessions

### 2. Create Comprehensive Validation
- Implement `app/backend/src/middleware/validation.py` with:
  - File type validation using existing `validate_file()` function
  - MIME type checking via `validate_mime_type()` from security utils
  - File size validation (max 50MB per FR-DOC-04)
  - Ownership validation and filename sanitization
  - Request data validation for filename and file existence

### 3. Implement MIME Type Sanitization
- Create `app/backend/src/utils/security.py` with:
  - `sanitize_filename()` function to generate UUID-based filenames
  - `validate_mime_type()` function for content type verification
  - `validate_file_type()` for extension validation consistency
  - `get_safe_filename()` for storage filename generation
  - `validate_file_integrity()` for file integrity checks

### 4. Configure Storage Service
- Complete `app/backend/src/services/storage_service.py` with:
  - Enhanced `upload_to_storage()` function with detailed error handling
  - Integration with file content validation
  - Proper Supabase client configuration
  - Logging of upload attempts and errors

### 5. Implement Error Handling and Logging
- Add comprehensive error handling across all components:
  - MIME type validation errors with descriptive messages
  - File size exceeded errors with specific limit information
  - Missing file or filename errors
  - Storage upload failures with error propagation
- Implement logging for upload attempts using `log_upload_attempt()` function

### 6. Update Upload Endpoint
- Integrate validation middleware into upload endpoint
- Add logging for upload attempts and results
- Return appropriate HTTP status codes for different error types
- Ensure proper error propagation from validation to response

## File Structure

```
app/backend/
├── src/
│   ├── middleware/
│   │   └── validation.py      # NEW
│   ├── utils/
│   │   └── security.py        # NEW  
│   ├── services/
│   │   └── storage_service.py # MODIFIED
│   ├── api/v1/
│   │   └── document/
│   │       └── upload.py      # MODIFIED
│   └── main.py                # MODIFIED (import validation for logging)
├── requirements.txt            # MODIFIED (email-validator)
└── .env.example                # MODIFIED (FRONTEND_URL)
```

## Security Requirements Implemented

### FR-DOC-01: Supported File Types
- ✅ PDF, DOCX, PPTX, TXT, EPUB, JPG, PNG
- ✅ MIME type validation against whitelist
- ✅ File extension matching content type

### FR-DOC-02: Ownership Enforcement
- ✅ Owner validation and header extraction
- ✅ Document access control implementation

### FR-DOC-04: Filename Sanitization
- ✅ UUID-based unique filenames
- ✅ Path traversal prevention
- ✅ Secure storage naming conventions

### FR-DOC-05: Security Logging
- ✅ Upload attempt logging
- ✅ Error tracking and audit trails
- ✅ Successful operation recording

## Implementation Details

### Validation Functions
- `validate_document_for_upload()`: Main validation orchestrator
- `validate_upload_request_data()`: Basic request validation
- `log_upload_attempt()`: Upload attempt logging
- `sanitize_filename()`: Filename sanitization utility

### Error Handling Patterns
- MIME type errors return 400 with descriptive messages
- File size errors return 413 with limit information
- Storage errors return 400 with error messages
- Server errors return 500 with error details

### Logging Structure
```python
log_data = {
    "timestamp": datetime.now().isoformat(),
    "owner_id": owner_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "file_size": file.size,
    "success": success,
    "error_message": error
}
```

## Next Steps

After completing this skill implementation:
1. T008: Create frontend upload component (`app/frontend/src/components/document/upload-form.tsx`)
2. T012-T016: Implement library listing, search, delete functionality
3. T017-T019: Add comprehensive logging, ownership verification, quickstart updates

## Common Patterns

### Upload Endpoint Structure
```python
@router.post("/upload")
async def upload_document(file: UploadFile):
    try:
        supabase = get_supabase_client()
    except ValueError as e:
        log_upload_attempt(file, owner_id, False, str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    file_content, content_type = validate_document_for_upload(file, owner_id)
    public_url, error = upload_to_storage(supabase, file, owner_id)
    
    if error:
        log_upload_attempt(file, owner_id, False, error)
        raise HTTPException(status_code=400, detail=error)
    
    # Create document record and log success
```

### Validation Error Handling
```python
# Return clear, user-friendly error messages
raise HTTPException(status_code=400, detail=f"MIME type '{content_type}' is not supported")
raise HTTPException(status_code=413, detail=f"File size exceeds maximum of {MAX_FILE_SIZE} bytes")
raise HTTPException(status_code=400, detail="Valid owner_id is required")
```

## Dependencies

- `fastapi>=2.0.0` - Web framework for upload endpoints
- `python-multipart>=0.5.0` - File upload handling
- `email-validator>=2.0.0` - Email validation for user management

## Configuration

Required environment variables:
```bash
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
FRONTEND_URL=http://localhost:3000
DATABASE_URL=postgresql://...
```

## Testing Strategy

### Independent Test 1: Valid PDF Upload
1. Authenticate user
2. Upload valid PDF file via endpoint
3. Verify successful response with document details
4. Confirm storage upload and database record creation

### Independent Test 2: Invalid File Type
1. Authenticate user
2. Attempt upload of unsupported file type
3. Verify user-friendly error message
4. Confirm no storage or database operations

### Independent Test 3: File Size Validation
1. Authenticate user
2. Attempt upload of oversized file (>50MB)
3. Verify size limit error message
4. Confirm no storage or database operations