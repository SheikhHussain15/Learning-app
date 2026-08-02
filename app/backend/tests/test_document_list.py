OWNER_ID = "test-user-1"


def test_list_documents_requires_auth(client, sample_documents):
    response = client.get("/api/v1/document/list")
    assert response.status_code == 401


def test_list_documents_with_owner(client, auth_headers, sample_documents):
    response = client.get("/api/v1/document/list", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["documents"]) == 5


def test_list_documents_pagination(client, auth_headers, sample_documents):
    response = client.get("/api/v1/document/list?page=1&per_page=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["documents"]) == 2
    assert data["page"] == 1
    assert data["per_page"] == 2


def test_list_documents_second_page(client, auth_headers, sample_documents):
    response = client.get("/api/v1/document/list?page=3&per_page=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 1
    assert data["page"] == 3


def test_list_documents_filter_by_owner(client, db):
    from src.core.auth import create_access_token
    from src.models.document import Document
    from src.models.user import User

    other = User(
        id="other-user",
        email="other@example.com",
        password_hash="hashed_password",
        email_verified=True,
    )
    db.add(other)
    db.flush()
    doc = Document(
        owner_id="other-user",
        title="Other doc",
        filename="other.pdf",
        format="application/pdf",
        size=500,
        status="uploaded",
    )
    db.add(doc)
    db.commit()

    token = create_access_token(data={"sub": "other-user"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/document/list", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["documents"][0]["owner_id"] == "other-user"


def test_list_documents_ordered_by_date(client, auth_headers, sample_documents):
    response = client.get("/api/v1/document/list", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    dates = [doc["created_at"] for doc in data["documents"]]
    assert dates == sorted(dates, reverse=True)
