from src.services.search_service import search_documents


def test_search_by_title(db, sample_documents):
    results, total = search_documents(db=db, query="Document 1")
    assert total == 1
    assert results[0].title == "Test Document 1"


def test_search_partial_title(db, sample_documents):
    results, total = search_documents(db=db, query="Document")
    assert total == 5


def test_search_no_results(db, sample_documents):
    results, total = search_documents(db=db, query="Nonexistent")
    assert total == 0
    assert results == []


def test_search_empty_query(db, sample_documents):
    results, total = search_documents(db=db, query="")
    assert total == 5
    assert len(results) == 5


def test_search_with_owner_filter(db, sample_documents):
    results, total = search_documents(db=db, query="Document", owner_id="test-user-1")
    assert total == 5


def test_search_wrong_owner(db, sample_documents):
    results, total = search_documents(db=db, query="Document", owner_id="wrong-user")
    assert total == 0


def test_search_pagination(db, sample_documents):
    results, total = search_documents(db=db, query="Document", page=1, per_page=2)
    assert total == 5
    assert len(results) == 2


def test_search_case_insensitive(db, sample_documents):
    results, total = search_documents(db=db, query="document 3")
    assert total == 1
    assert results[0].title == "Test Document 3"


def test_search_via_api_endpoint(client, sample_documents):
    response = client.get("/api/v1/document/list?owner_id=test-user-1&q=Document+2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["documents"][0]["title"] == "Test Document 2"
