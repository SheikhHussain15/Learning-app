import os
import uuid

from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

ALLOWED_EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "text/plain": ".txt",
    "text/markdown": ".md",
    "application/epub+zip": ".epub",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}


def get_upload_dir() -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return UPLOAD_DIR


def sanitize_filename(filename: str) -> str:
    safe_name = os.path.basename(filename)
    name, ext = os.path.splitext(safe_name)
    unique_name = f"{uuid.uuid4()}{ext}"
    return unique_name


def validate_file(file: UploadFile) -> tuple[bool, str | None]:
    if not file.content_type or file.content_type not in ALLOWED_EXTENSIONS:
        return False, f"File type '{file.content_type}' is not supported"
    return True, None


def save_file_locally(file: UploadFile, owner_id: str) -> tuple[str, str | None]:
    is_valid, error = validate_file(file)
    if not is_valid:
        return "", error

    file_content = file.file.read()
    if len(file_content) > MAX_FILE_SIZE:
        return "", f"File size exceeds maximum of {MAX_FILE_SIZE} bytes"

    safe_filename = sanitize_filename(file.filename or "unknown")
    user_dir = os.path.join(get_upload_dir(), owner_id)
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, safe_filename)
    with open(file_path, "wb") as f:
        f.write(file_content)

    return file_path, None


def delete_file_locally(file_path: str) -> bool:
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
    except OSError:
        pass
    return False
