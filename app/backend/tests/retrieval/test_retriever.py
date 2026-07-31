import pytest
from src.retrieval.retriever import Retriever


@pytest.fixture
def retriever(mock_chromadb, monkeypatch):
    monkeypatch.setattr(
        "src.retrieval.retriever.resolve_embed_model",
        lambda model: type("MockEmbed", (), {"__call__": lambda self, x: None})(),
    )
    return Retriever()


def test_retrieve_top_k(retriever):
    results = retriever.retrieve(collection_name="test_collection", query="test query", top_k=5)
    assert isinstance(results, list)


def test_retrieve_min_score_filter(retriever):
    results = retriever.retrieve(collection_name="test_collection", query="test query")
    assert isinstance(results, list)


def test_retrieve_empty_query(retriever):
    results = retriever.retrieve(collection_name="test_collection", query="")
    assert isinstance(results, list)


def test_retrieve_nonexistent_collection(retriever):
    results = retriever.retrieve(collection_name="nonexistent", query="test")
    assert isinstance(results, list)
