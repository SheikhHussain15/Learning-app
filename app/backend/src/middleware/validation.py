
from fastapi import HTTPException, UploadFile


def validate_document_for_upload(file: UploadFile, owner_id: str) -> tuple[bytes, str]:
    """Validate document before upload and return file content and content type if validation passes."""
    # Validate basic file requirements
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    if len(file.filename.strip()) == 0:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    # Read and validate file content type
    if not file.content_type:
        raise HTTPException(status_code=400, detail="File content type is required")

    content_type = file.content_type

    # Validate file type in utils.security
    from src.utils.security import MAX_FILE_SIZE, sanitize_filename, validate_file_integrity, validate_mime_type

    # Validate MIME type is supported
    if not validate_mime_type(content_type):
        raise HTTPException(status_code=400, detail=f"MIME type '{content_type}' is not supported")

    # Read file content for size validation
    file_content = file.file.read()

    # Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File size exceeds maximum of {MAX_FILE_SIZE} bytes")

    # Validate file integrity (size check already done above)
    if not validate_file_integrity(file):
        raise HTTPException(status_code=400, detail="Invalid file or corrupted file")

    # Reset file pointer for storage service
    import io
    file.file = io.BytesIO(file_content)

    # Validate ownership requirement
    if not owner_id or not isinstance(owner_id, str):
        raise HTTPException(status_code=400, detail="Valid owner_id is required")

    # Sanitize filename
    safe_filename = sanitize_filename(file.filename or "unknown")
    if len(safe_filename) > 255:
        raise HTTPException(status_code=400, detail="Filename too long after sanitization")

    return file_content, content_type


def validate_upload_request_data(file: UploadFile) -> None:
    """Validate basic upload request data."""
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    if len(file.filename.strip()) == 0:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    if file.size and file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")


def log_upload_attempt(file: UploadFile, owner_id: str, success: bool, error: str | None = None) -> None:
    """Log upload attempt for auditing."""
    from datetime import datetime

    from src.core.logging import get_logger

    logger = get_logger("validation")

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "owner_id": owner_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": file.size,
        "success": success,
        "error_message": error
    }

    if success:
        logger.info("Upload validation successful", extra=log_data)
    else:
        logger.warning("Upload validation failed", extra=log_data)
