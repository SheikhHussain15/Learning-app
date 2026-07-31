import logging

import chromadb
from chromadb import PersistentClient

from src.core import config

logger = logging.getLogger(__name__)


class ChromaClientWrapper:
    def __init__(self, path: str | None = None):
        self._path = path or config.CHROMA_DB_PATH
        self._client: PersistentClient | None = None

    def get_client(self) -> PersistentClient:
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self._path)
        return self._client

    def get_or_create_collection(self, name: str):
        return self.get_client().get_or_create_collection(name=name)

    def heartbeat(self) -> bool:
        try:
            self.get_client().heartbeat()
            return True
        except Exception as e:
            logger.error("ChromaDB heartbeat failed: %s", e)
            return False


_chroma_wrapper: ChromaClientWrapper | None = None


def get_chroma_client() -> ChromaClientWrapper:
    global _chroma_wrapper
    if _chroma_wrapper is None:
        _chroma_wrapper = ChromaClientWrapper()
    return _chroma_wrapper
