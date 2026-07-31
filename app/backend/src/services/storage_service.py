import os
import uuid

from fastapi import UploadFile
from supabase import Client

ALLOWED_EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "text/plain": ".txt",
    "application/epub+zip": ".epub",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def validate_file(file: UploadFile) -> tuple[bool, str | None]:
    """Validate that the file has a supported content type."""
    if file.content_type not in ALLOWED_EXTENSIONS:
        return False, f"File type '{file.content_type}' is not supported"

    return True, None


def sanitize_filename(filename: str) -> str:
    """Generate a safe filename with UUID to prevent conflicts."""
    safe_name = os.path.basename(filename)
    name, ext = os.path.splitext(safe_name)
    unique_name = f"{uuid.uuid4()}{ext}"
    return unique_name


def upload_to_storage(supabase: Client, file: UploadFile, owner_id: str) -> tuple[str, str | None]:
    """Upload a file to Supabase storage after validation.

    Args:
        supabase: Supabase client
        file: The uploaded file to store
        owner_id: ID of the file owner (currently using hardcoded value)

    Returns:
        tuple: (public_url, error_message) where error_message is None if successful
    """
    is_valid, error = validate_file(file)
    if not is_valid:
        return "", error

    # Read file content from uploaded file
    # Note: file.file is already at correct position after validation
    file_content = file.file.read()

    # Check file size
    if len(file_content) > MAX_FILE_SIZE:
        return "", f"File size exceeds maximum of {MAX_FILE_SIZE} bytes"

    # Generate safe filename
    safe_filename = sanitize_filename(file.filename or "unknown")
    bucket_name = "documents"

    # Upload to Supabase storage
    response = supabase.storage.from_(bucket_name).upload(
        path=safe_filename,
        file=file_content,
        file_options={"content-type": file.content_type}
    )

    # Check for upload errors
    if response.get("error"):
        return "", response["error"].message

    # Get public URL for the uploaded file
    public_url = supabase.storage.from_(bucket_name).get_public_url(safe_filename).data.get("publicUrl")

    return public_url, None
