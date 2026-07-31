import logging

from llama_index.core import Document as LIDocument
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.embeddings import resolve_embed_model
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.core import config
from src.retrieval.chroma_client import get_chroma_client

logger = logging.getLogger(__name__)


class Indexer:
    def __init__(self):
        self._embed_model = None

    def _get_embed_model(self):
        if self._embed_model is None:
            self._embed_model = resolve_embed_model(config.EMBEDDING_MODEL)
            Settings.embed_model = self._embed_model
        return self._embed_model

    def index_document(self, doc_id: str, text: str, metadata: dict | None = None) -> bool:
        try:
            chroma = get_chroma_client()
            collection = chroma.get_or_create_collection(f"doc_{doc_id}")
            vector_store = ChromaVectorStore(chroma_collection=collection)

            doc = LIDocument(text=text, metadata=metadata or {})
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=self._get_embed_model(),
            )
            index.insert(doc)

            logger.info("Indexed document %s with %d chars", doc_id, len(text))
            return True
        except Exception as e:
            logger.error("Indexing failed for document %s: %s", doc_id, e)
            return False


_indexer: Indexer | None = None


def get_indexer() -> Indexer:
    global _indexer
    if _indexer is None:
        _indexer = Indexer()
    return _indexer
