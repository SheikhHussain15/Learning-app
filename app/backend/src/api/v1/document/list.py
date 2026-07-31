
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.core.logging import get_logger
from src.middleware.auth import get_current_user
from src.models.document import Document
from src.models.user import User
from src.schemas.document import DocumentListResponse
from src.services.search_service import search_documents

router = APIRouter()
logger = get_logger("document.list")


@router.get("/list", response_model=DocumentListResponse)
def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    q: str | None = Query(None, description="Search query string"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owner_id = current_user.id

    if q:
        documents, total = search_documents(
            db=db,
            query=q,
            owner_id=owner_id,
            page=page,
            per_page=per_page,
        )
    else:
        query = db.query(Document).filter(Document.owner_id == owner_id)
        total = query.count()
        offset = (page - 1) * per_page
        documents = (
            query.order_by(Document.created_at.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )

    return DocumentListResponse(
        documents=documents,
        total=total,
        page=page,
        per_page=per_page,
    )
