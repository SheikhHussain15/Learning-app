import pytest
import hashlib
from unittest.mock import patch, MagicMock
from src.services.agent_output_cache import compute_params_hash


class TestParamsHash:
    def test_compute_params_hash_deterministic(self):
        params = {"difficulty": "medium", "question_count": 5}
        hash1 = compute_params_hash(params)
        hash2 = compute_params_hash(params)
        assert hash1 == hash2

    def test_compute_params_hash_order_independent(self):
        params1 = {"difficulty": "medium", "question_count": 5}
        params2 = {"question_count": 5, "difficulty": "medium"}
        hash1 = compute_params_hash(params1)
        hash2 = compute_params_hash(params2)
        assert hash1 == hash2

    def test_compute_params_hash_different_inputs(self):
        params1 = {"difficulty": "easy"}
        params2 = {"difficulty": "hard"}
        hash1 = compute_params_hash(params1)
        hash2 = compute_params_hash(params2)
        assert hash1 != hash2

    def test_compute_params_hash_empty(self):
        hash1 = compute_params_hash({})
        hash2 = compute_params_hash({})
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex digest length


class TestCacheOperations:
    @patch("src.services.agent_output_cache.SessionLocal")
    def test_get_cached_output_miss(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        from src.services.agent_output_cache import get_cached_output
        result = get_cached_output("nonexistent-doc", "summary", {})
        assert result is None

    @patch("src.services.agent_output_cache.SessionLocal")
    def test_store_and_retrieve(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        mock_output = MagicMock()
        mock_output.output_data = {"test": True}
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()

        from src.services.agent_output_cache import store_output
        stored = store_output("test-doc", "summary", {"difficulty": "easy"}, {"test": True})
        assert stored is not None
        mock_db.add.assert_called_once()

    @patch("src.services.agent_output_cache.SessionLocal")
    def test_invalidate_cache(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_query = mock_db.query.return_value.filter.return_value
        mock_query.count.return_value = 2
        mock_query.delete.return_value = 2

        from src.services.agent_output_cache import invalidate_cache
        count = invalidate_cache("test-doc")
        assert count == 2

    @patch("src.services.agent_output_cache.SessionLocal")
    def test_invalidate_cache_by_type(self, mock_session):
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_query = mock_db.query.return_value.filter.return_value.filter.return_value
        mock_query.count.return_value = 1
        mock_query.delete.return_value = 1

        from src.services.agent_output_cache import invalidate_cache
        count = invalidate_cache("test-doc", "quiz")
        assert count == 1
