
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.models.document import Document


def search_documents(
    db: Session,
    query: str,
    owner_id: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Document], int]:
    db_query = db.query(Document)

    if owner_id:
        db_query = db_query.filter(Document.owner_id == owner_id)

    if query:
        search_term = f"%{query}%"
        db_query = db_query.filter(
            or_(
                Document.title.ilike(search_term),
                Document.filename.ilike(search_term),
                Document.format.ilike(search_term),
            )
        )

    total = db_query.count()
    offset = (page - 1) * per_page
    documents = (
        db_query.order_by(Document.created_at.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    return documents, total
