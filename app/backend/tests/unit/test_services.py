import pytest
from src.services.auth_service import hash_password, verify_password, create_user, get_user_by_email
from unittest.mock import patch, MagicMock


class TestAuthService:
    def test_hash_password(self):
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_verify_password_correct(self):
        password = "my_secret"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "my_secret"
        hashed = hash_password(password)
        assert verify_password("wrong_password", hashed) is False

    def test_create_user(self, db):
        user = create_user(db, "new@example.com", "password123")
        assert user is not None
        assert user.email == "new@example.com"
        assert user.password_hash != "password123"

    def test_get_user_by_email_exists(self, db, sample_user):
        found = get_user_by_email(db, "test@example.com")
        assert found is not None
        assert found.id == sample_user.id

    def test_get_user_by_email_not_found(self, db):
        found = get_user_by_email(db, "nonexistent@example.com")
        assert found is None
