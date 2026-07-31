import logging

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.embeddings import resolve_embed_model
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.core import config
from src.retrieval.chroma_client import get_chroma_client
from src.schemas.agent import RetrievedChunk

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self):
        self._embed_model = None

    def _get_embed_model(self):
        if self._embed_model is None:
            self._embed_model = resolve_embed_model(config.EMBEDDING_MODEL)
            Settings.embed_model = self._embed_model
        return self._embed_model

    def retrieve(self, collection_name: str, query: str, top_k: int = None) -> list[RetrievedChunk]:
        if top_k is None:
            top_k = config.TOP_K_RETRIEVAL
        min_score = config.MIN_SIMILARITY_THRESHOLD

        try:
            chroma = get_chroma_client()
            collection = chroma.get_or_create_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=self._get_embed_model(),
            )
            query_engine = index.as_query_engine(similarity_top_k=top_k)

            results = query_engine.query(query)

            chunks = []
            for node in results.source_nodes:
                score = node.score or 0.0
                if score >= min_score:
                    chunks.append(RetrievedChunk(
                        chunk_id=node.node_id,
                        text=node.text,
                        score=score,
                        metadata=node.metadata or {},
                    ))

            logger.info(
                "Retrieved %d chunks (filtered from %d) from %s for query",
                len(chunks), len(results.source_nodes), collection_name,
            )
            return chunks

        except Exception as e:
            logger.error("Retrieval failed for collection %s: %s", collection_name, e)
            return []


_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
