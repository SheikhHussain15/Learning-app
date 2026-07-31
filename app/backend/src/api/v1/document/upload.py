import io
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.core.local_storage import sanitize_filename, save_file_locally, validate_file
from src.core.logging import get_logger
from src.middleware.auth import get_current_user
from src.middleware.validation import log_upload_attempt
from src.models.document import Document
from src.models.user import User
from src.schemas.document import DocumentResponse

router = APIRouter()
logger = get_logger("document.upload")


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: Annotated[UploadFile, File(...)],
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owner_id = current_user.id
    logger.info(f"Upload attempt for user: {owner_id}, file: {file.filename}, content_type: {file.content_type}")

    is_valid, error = validate_file(file)
    logger.info(f"Validation result: is_valid={is_valid}, error={error}")
    if not is_valid:
        log_upload_attempt(file, owner_id, False, error)
        raise HTTPException(status_code=400, detail=error)

    file_content = file.file.read()
    logger.info(f"File read, size: {len(file_content)} bytes")
    file_size = len(file_content)

    file.file = io.BytesIO(file_content)

    file_path, error = save_file_locally(file, owner_id)
    logger.info(f"Save file result: path={file_path}, error={error}")
    if error:
        log_upload_attempt(file, owner_id, False, error)
        raise HTTPException(status_code=400, detail=error)

    document = Document(
        owner_id=owner_id,
        title=title.strip() or file.filename or "Untitled",
        filename=sanitize_filename(file.filename or "unknown"),
        format=file.content_type or "unknown",
        size=file_size,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    log_upload_attempt(file, owner_id, True)
    logger.info("Document uploaded: id=%s, title=%s, size=%d", document.id, document.title, document.size)

    return document
