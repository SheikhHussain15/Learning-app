from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.core.logging import get_logger
from src.middleware.auth import get_current_user
from src.models.document import Document
from src.models.user import User

router = APIRouter()
logger = get_logger("document.delete")


@router.delete("/delete/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")

    db.delete(document)
    db.commit()

    logger.info("Document deleted: id=%s, owner=%s", document_id, current_user.id)

    return {"message": "Document deleted successfully", "id": document_id}
