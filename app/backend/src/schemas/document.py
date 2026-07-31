from datetime import datetime

from pydantic import BaseModel, constr


class DocumentCreate(BaseModel):
    title: constr(min_length=1, max_length=255)
    filename: str
    format: str
    size: int
    doc_metadata: dict | None = None


class DocumentResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    filename: str
    format: str
    size: int
    status: str
    doc_metadata: dict | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int
    per_page: int
