import pytest
from src.models.user import User
from src.models.document import Document
from src.services.auth_service import create_user, get_user_by_email


class TestUserCRUD:
    def test_create_user(self, db):
        user = create_user(db, "crud@example.com", "password123")
        assert user.id is not None
        assert user.email == "crud@example.com"
        assert user.created_at is not None

    def test_get_user_by_email(self, db, sample_user):
        found = get_user_by_email(db, "test@example.com")
        assert found is not None
        assert found.id == sample_user.id

    def test_user_email_unique(self, db):
        create_user(db, "unique@example.com", "pass1")
        with pytest.raises(Exception):
            create_user(db, "unique@example.com", "pass2")

    def test_user_timestamps(self, db):
        user = create_user(db, "timestamps@example.com", "pass")
        assert user.created_at is not None
        assert user.updated_at is not None


class TestDocumentCRUD:
    def test_create_document(self, db, sample_user):
        doc = Document(
            owner_id=sample_user.id,
            title="Test Doc",
            filename="test.pdf",
            format="application/pdf",
            size=1024,
            status="uploaded",
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        assert doc.id is not None
        assert doc.title == "Test Doc"

    def test_query_documents_by_owner(self, db, sample_documents, sample_user):
        docs = db.query(Document).filter(Document.owner_id == sample_user.id).all()
        assert len(docs) == 5

    def test_document_status_update(self, db, sample_documents):
        doc = sample_documents[0]
        doc.status = "processed"
        db.commit()
        db.refresh(doc)
        assert doc.status == "processed"
