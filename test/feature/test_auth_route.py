import pytest
from src.models.user import User
from src.core.security import get_password_hash, create_reset_password_token

class TestAuthRoutes:

    def test_login_success(self, client, session):
        user = User(
            username="loginuser",
            email="loginuser@example.com",
            hashed_password=get_password_hash("loginpass")
        )
        session.add(user)
        session.commit()

        response = client.post("/api/v1/auths/login", data={
            "username": "loginuser",
            "password": "loginpass"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, session):
        user = User(
            username="wrongpass",
            email="wrong@example.com",
            hashed_password=get_password_hash("correctpass")
        )
        session.add(user)
        session.commit()

        response = client.post("/api/v1/auths/login", data={
            "username": "wrongpass",
            "password": "incorrect"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client, session):
        response = client.post("/api/v1/auths/login", data={
            "username": "noexiste",
            "password": "any"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_forgot_password_existing_email(self, client, session):
        user = User(
            username="forgotuser",
            email="forgot@example.com",
            hashed_password=get_password_hash("oldpass")
        )
        session.add(user)
        session.commit()

        response = client.post("/api/v1/auths/forgot-password", json={
            "email": "forgot@example.com"
        })
        assert response.status_code == 200
        assert "recibirás instrucciones" in response.json()["msg"]

    def test_forgot_password_nonexistent_email(self, client, session):
        response = client.post("/api/v1/auths/forgot-password", json={
            "email": "noexiste@example.com"
        })
        assert response.status_code == 200
        assert "recibirás instrucciones" in response.json()["msg"]

    def test_reset_password_valid_token(self, client, session):
        user = User(
            username="resetuser",
            email="reset@example.com",
            hashed_password=get_password_hash("oldpass")
        )
        session.add(user)
        session.commit()

        token = create_reset_password_token("reset@example.com")

        response = client.post("/api/v1/auths/reset-password", json={
            "token": token,
            "new_password": "newpass123"
        })
        assert response.status_code == 200
        assert "restablecida correctamente" in response.json()["msg"]

        # Verifica login con la nueva contraseña
        login_response = client.post("/api/v1/auths/login", data={
            "username": "resetuser",
            "password": "newpass123"
        })
        assert login_response.status_code == 200

    def test_reset_password_invalid_token(self, client, session):
        response = client.post("/api/v1/auths/reset-password", json={
            "token": "invalid_token",
            "new_password": "newpass123"
        })
        assert response.status_code == 400
        assert "Token inválido o expirado" in response.json()["detail"]

    def test_reset_password_nonexistent_user(self, client, session):
        # Token válido para un email que no existe
        token = create_reset_password_token("noexiste@example.com")
        response = client.post("/api/v1/auths/reset-password", json={
            "token": token,
            "new_password": "newpass123"
        })
        assert response.status_code == 404
        assert "Usuario no encontrado" in response.json()["detail"]