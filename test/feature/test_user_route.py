import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.core.security import get_password_hash

class TestUserRoutes:

    @pytest.fixture
    def regular_user(self, session):
        """Crea un usuario regular para los tests"""
        user = User(
            username="regular_test",
            email="regular@test.com",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @pytest.fixture
    def auth_headers(self, client, regular_user):
        """Obtiene headers de autenticación para el usuario regular"""
        response = client.post("/api/v1/auths/login", data={
            "username": "regular_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_read_own_profile_success(self, client, auth_headers, regular_user):
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == regular_user.username
        assert data["email"] == regular_user.email

    def test_read_own_profile_unauthorized(self, client):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
