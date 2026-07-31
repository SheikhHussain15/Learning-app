import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.core.database import Base
from src.core.deps import get_db
from src.main import app
from src.models.document import Document
from src.models.user import User
from src.models.agent_run import AgentRun, AgentType, AgentStatus, Base as AgentBase
from src.models.health_check import HealthCheck
from src.models.deployment_record import DeploymentRecord
from src.models.security_audit_log import SecurityAuditLog
from src.models.test_suite_result import TestSuiteResult
from src.models.secret_rotation_log import SecretRotationLog


TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_user(db):
    user = User(
        id="test-user-1",
        email="test@example.com",
        password_hash="hashed_password",
        email_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_documents(db, sample_user):
    docs = []
    for i in range(5):
        doc = Document(
            owner_id=sample_user.id,
            title=f"Test Document {i}",
            filename=f"test-doc-{i}.pdf",
            format="application/pdf",
            size=1000 * (i + 1),
            status="uploaded",
        )
        db.add(doc)
        docs.append(doc)
    db.commit()
    for doc in docs:
        db.refresh(doc)
    return docs


@pytest.fixture
def valid_request_payload():
    return {
        "document_id": "550e8400-e29b-41d4-a716-446655440000",
        "node_ids": ["550e8400-e29b-41d4-a716-446655440001"],
        "agent_params": {"test": True},
        "context": {
            "chunks": [
                {"chunk_id": "chunk-1", "text": "Test content", "score": 0.95, "metadata": {}}
            ]
        },
    }


@pytest.fixture
def mock_langfuse(monkeypatch):
    class MockLangfuse:
        def __init__(self, *args, **kwargs):
            pass

        def trace(self, name=None):
            return MockTrace()

        def flush(self):
            pass

    class MockTrace:
        def span(self, name=None):
            return MockSpan()

        def generation(self, name=None):
            return MockSpan()

        def update(self, **kwargs):
            pass

    class MockSpan:
        def __init__(self):
            pass

        def generation(self, name=None, model=None, **kwargs):
            return MockSpan()

        def end(self):
            pass

        def update(self, **kwargs):
            pass

    monkeypatch.setattr("src.tracing.langfuse_client.Langfuse", MockLangfuse)
    return MockLangfuse


@pytest.fixture
def mock_chromadb(monkeypatch):
    class MockCollection:
        def __init__(self, name):
            self.name = name
            self._store = {}

        def get(self, **kwargs):
            ids = kwargs.get("ids", None)
            if ids:
                filtered_ids = [i for i in ids if i in self._store]
                return {"ids": filtered_ids, "metadatas": [self._store[i]["metadata"] for i in filtered_ids], "documents": [self._store[i]["document"] for i in filtered_ids]}
            return {"ids": list(self._store.keys()), "metadatas": [v["metadata"] for v in self._store.values()], "documents": [v["document"] for v in self._store.values()]}

        def add(self, **kwargs):
            ids = kwargs.get("ids", [])
            documents = kwargs.get("documents", [])
            metadatas = kwargs.get("metadatas", [])
            for i, doc_id in enumerate(ids):
                self._store[doc_id] = {
                    "document": documents[i] if i < len(documents) else "",
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                }

        def query(self, **kwargs):
            return {"ids": [[]], "distances": [[]], "metadatas": [[]], "documents": [[]]}

    class MockPersistentClient:
        def __init__(self, path=None):
            self._collections = {}

        def get_or_create_collection(self, name):
            if name not in self._collections:
                self._collections[name] = MockCollection(name)
            return self._collections[name]

        def heartbeat(self):
            return 1

    monkeypatch.setattr("chromadb.PersistentClient", MockPersistentClient)
    return MockPersistentClient
