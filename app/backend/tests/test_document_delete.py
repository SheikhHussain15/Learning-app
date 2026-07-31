def test_delete_document(client, sample_documents):
    doc_id = sample_documents[0].id
    response = client.delete(f"/api/v1/document/delete/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Document deleted successfully"
    assert data["id"] == doc_id


def test_delete_nonexistent_document(client):
    response = client.delete("/api/v1/document/delete/nonexistent-id")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_delete_removes_from_database(client, sample_documents, db):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}")

    from src.models.document import Document

    doc = db.query(Document).filter(Document.id == doc_id).first()
    assert doc is None


def test_delete_reduces_document_count(client, sample_documents, db):
    from src.models.document import Document

    initial_count = db.query(Document).count()
    doc_id = sample_documents[0].id

    client.delete(f"/api/v1/document/delete/{doc_id}")

    final_count = db.query(Document).count()
    assert final_count == initial_count - 1


def test_delete_then_list(client, sample_documents):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}")

    response = client.get("/api/v1/document/list?owner_id=test-user-1")
    data = response.json()
    assert data["total"] == 4
    ids = [doc["id"] for doc in data["documents"]]
    assert doc_id not in ids


def test_search_after_delete(client, sample_documents):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}")

    response = client.get("/api/v1/document/list?owner_id=test-user-1&q=Document")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
