def test_delete_document(client, auth_headers, sample_documents):
    doc_id = sample_documents[0].id
    response = client.delete(f"/api/v1/document/delete/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Document deleted successfully"
    assert data["id"] == doc_id


def test_delete_nonexistent_document(client, auth_headers):
    response = client.delete("/api/v1/document/delete/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_delete_requires_auth(client, sample_documents):
    doc_id = sample_documents[0].id
    response = client.delete(f"/api/v1/document/delete/{doc_id}")
    assert response.status_code == 401


def test_delete_removes_from_database(client, auth_headers, sample_documents, db):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}", headers=auth_headers)

    from src.models.document import Document

    doc = db.query(Document).filter(Document.id == doc_id).first()
    assert doc is None


def test_delete_reduces_document_count(client, auth_headers, sample_documents, db):
    from src.models.document import Document

    initial_count = db.query(Document).count()
    doc_id = sample_documents[0].id

    client.delete(f"/api/v1/document/delete/{doc_id}", headers=auth_headers)

    final_count = db.query(Document).count()
    assert final_count == initial_count - 1


def test_delete_then_list(client, auth_headers, sample_documents):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}", headers=auth_headers)

    response = client.get("/api/v1/document/list", headers=auth_headers)
    data = response.json()
    assert data["total"] == 4
    ids = [doc["id"] for doc in data["documents"]]
    assert doc_id not in ids


def test_search_after_delete(client, auth_headers, sample_documents):
    doc_id = sample_documents[0].id
    client.delete(f"/api/v1/document/delete/{doc_id}", headers=auth_headers)

    response = client.get("/api/v1/document/list?q=Document", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
