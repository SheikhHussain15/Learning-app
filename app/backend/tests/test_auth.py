def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "new@example.com"
    assert "id" in data["user"]


def test_register_duplicate_email(client, sample_user):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_user(client, db):
    from src.services.auth_service import hash_password
    from src.models.user import User

    user = User(
        id="login-test-user",
        email="login@example.com",
        password_hash=hash_password("testpass123"),
        email_verified=True,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_get_profile_authenticated(client, sample_user):
    from src.core.auth import create_access_token

    token = create_access_token(data={"sub": sample_user.id})

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_get_profile_unauthenticated(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_profile_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_update_profile(client, sample_user):
    from src.core.auth import create_access_token

    token = create_access_token(data={"sub": sample_user.id})

    response = client.patch(
        "/api/v1/auth/profile",
        json={"email": "updated@example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"


def test_update_profile_duplicate_email(client, sample_user, db):
    from src.core.auth import create_access_token
    from src.models.user import User

    other = User(
        id="other-id",
        email="other@example.com",
        password_hash="hash",
        email_verified=True,
    )
    db.add(other)
    db.commit()

    token = create_access_token(data={"sub": sample_user.id})

    response = client.patch(
        "/api/v1/auth/profile",
        json={"email": "other@example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert "already in use" in response.json()["detail"].lower()


def test_logout(client, sample_user):
    from src.core.auth import create_access_token

    token = create_access_token(data={"sub": sample_user.id})

    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "logged out" in response.json()["message"].lower()


def test_register_then_login_flow(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "flow@example.com", "password": "password123"},
    )
    assert register_response.status_code == 200
    token = register_response.json()["token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "flow@example.com"
