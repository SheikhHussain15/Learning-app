import os
import uuid

from fastapi import UploadFile

# Allowed MIME types for document uploads
ALLOWED_EXTENSIONS: set[str] = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "text/plain": ".txt",
    "application/epub+zip": ".epub",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def sanitize_filename(filename: str) -> str:
    """Sanitize filename and add UUID to prevent conflicts."""
    safe_name = os.path.basename(filename)
    name, ext = os.path.splitext(safe_name)
    unique_name = f"{uuid.uuid4()}{ext}"
    return unique_name


def validate_mime_type(content_type: str) -> bool:
    """Validate that the MIME type is supported for document uploads."""
    return content_type in ALLOWED_EXTENSIONS


def validate_file_type(file: UploadFile) -> bool:
    """Check file extension matches its MIME type."""
    if not file.content_type or not file.filename:
        return False

    expected_extension = ALLOWED_EXTENSIONS.get(file.content_type)
    if not expected_extension:
        return False

    actual_extension = os.path.splitext(file.filename)[1].lower()
    return actual_extension == expected_extension


def get_safe_filename(filename: str) -> str:
    """Generate a safe filename for storage."""
    return sanitize_filename(filename)


def validate_file_integrity(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> bool:
    """Validate file size and basic integrity."""
    try:
        if file.size is None:
            return False
        return file.size <= max_size
    except (AttributeError, TypeError):
        return False


def clean_filename_for_display(filename: str) -> str:
    """Clean filename for safe display by removing potentially problematic characters."""
    # Remove path components and normalize
    filename = os.path.basename(filename)
    # Replace or remove problematic characters
    return "".join(c for c in filename if c.isalnum() or c in (".", "_", " ", "-")).strip()
