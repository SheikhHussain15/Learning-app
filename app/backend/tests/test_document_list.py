OWNER_ID = "test-user-1"


def test_list_documents_requires_owner(client, sample_documents):
    response = client.get("/api/v1/document/list")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["documents"] == []


def test_list_documents_with_owner(client, sample_documents):
    response = client.get(f"/api/v1/document/list?owner_id={OWNER_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["documents"]) == 5


def test_list_documents_pagination(client, sample_documents):
    response = client.get(f"/api/v1/document/list?owner_id={OWNER_ID}&page=1&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["documents"]) == 2
    assert data["page"] == 1
    assert data["per_page"] == 2


def test_list_documents_second_page(client, sample_documents):
    response = client.get(f"/api/v1/document/list?owner_id={OWNER_ID}&page=3&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 1
    assert data["page"] == 3


def test_list_documents_filter_by_owner(client, sample_documents, db):
    from src.models.document import Document

    other = Document(
        owner_id="other-user",
        title="Other doc",
        filename="other.pdf",
        format="application/pdf",
        size=500,
        status="uploaded",
    )
    db.add(other)
    db.commit()

    response = client.get("/api/v1/document/list?owner_id=other-user")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["documents"][0]["owner_id"] == "other-user"


def test_list_documents_ordered_by_date(client, sample_documents):
    response = client.get(f"/api/v1/document/list?owner_id={OWNER_ID}")
    assert response.status_code == 200
    data = response.json()
    dates = [doc["created_at"] for doc in data["documents"]]
    assert dates == sorted(dates, reverse=True)
