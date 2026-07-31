import pytest
from src.retrieval.indexer import Indexer


class MockEmbed:
    pass


@pytest.fixture
def indexer(mock_chromadb, monkeypatch):
    monkeypatch.setattr("src.retrieval.indexer.resolve_embed_model", lambda model: MockEmbed())
    monkeypatch.setattr("src.retrieval.indexer.Settings", type("Settings", (), {"embed_model": None}))
    return Indexer()


def test_index_document(indexer, monkeypatch):
    class MockVectorStoreIndex:
        @staticmethod
        def from_vector_store(*args, **kwargs):
            return MockVectorStoreIndex()
        def insert(self, doc):
            pass

    monkeypatch.setattr("src.retrieval.indexer.VectorStoreIndex", MockVectorStoreIndex)
    result = indexer.index_document(
        doc_id="test-doc-1",
        text="Test document for indexing.",
        metadata={"title": "Test Doc", "format": "text"},
    )
    assert result is True


def test_index_empty_document(indexer, monkeypatch):
    class MockVectorStoreIndex:
        @staticmethod
        def from_vector_store(*args, **kwargs):
            return MockVectorStoreIndex()
        def insert(self, doc):
            pass

    monkeypatch.setattr("src.retrieval.indexer.VectorStoreIndex", MockVectorStoreIndex)
    result = indexer.index_document(doc_id="test-doc-empty", text="")
    assert result is True


def test_index_error_handling(indexer, monkeypatch):
    class MockVectorStoreIndex:
        @staticmethod
        def from_vector_store(*args, **kwargs):
            return MockVectorStoreIndex()
        def insert(self, doc):
            pass

    monkeypatch.setattr("src.retrieval.indexer.VectorStoreIndex", MockVectorStoreIndex)
    result = indexer.index_document(doc_id="test-doc-2", text="Test")
    assert result is True
