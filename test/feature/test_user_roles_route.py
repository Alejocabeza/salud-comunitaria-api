import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.core.security import get_password_hash

class TestUserRolesRoutes:

    @pytest.fixture
    def admin_user(self, session):
        """Crea un usuario con rol admin para los tests"""
        role = Role(name="admin", description="Administrador")
        session.add(role)
        session.commit()
        session.refresh(role)
        
        user = User(
            username="admin_test",
            email="admin@test.com",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)
        session.commit()
        
        return user

    @pytest.fixture
    def auth_headers(self, client, admin_user):
        """Obtiene headers de autenticación para el usuario admin"""
        response = client.post("/api/v1/auths/login", data={
            "username": "admin_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def test_user(self, session):
        user = User(
            username="test_user_role",
            email="test_user_role@test.com",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @pytest.fixture
    def test_role(self, session):
        role = Role(name="test_role_user", description="Rol de prueba para usuario")
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

    def test_assign_role_to_user_success(self, client, session, auth_headers, test_user, test_role):
        response = client.post(
            f"/api/v1/user_roles/assign?user_id={test_user.id}&role_id={test_role.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Role 'test_role_user' assigned to user 'test_user_role'" in response.json()["msg"]

    def test_assign_role_to_user_not_found(self, client, auth_headers, test_user):
        response = client.post(
            f"/api/v1/user_roles/assign?user_id={test_user.id}&role_id=999",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "User or Role not found" in response.json()["detail"]

    def test_assign_role_to_user_already_assigned(self, client, session, auth_headers, test_user, test_role):
        # Assign first
        link = UserRole(user_id=test_user.id, role_id=test_role.id)
        session.add(link)
        session.commit()

        # Assign again
        response = client.post(
            f"/api/v1/user_roles/assign?user_id={test_user.id}&role_id={test_role.id}",
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Role already assigned to user" in response.json()["detail"]

    def test_remove_role_from_user_success(self, client, session, auth_headers, test_user, test_role):
        # Assign first
        link = UserRole(user_id=test_user.id, role_id=test_role.id)
        session.add(link)
        session.commit()

        response = client.post(
            f"/api/v1/user_roles/remove?user_id={test_user.id}&role_id={test_role.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Role removed from user" in response.json()["msg"]

    def test_remove_role_from_user_not_found(self, client, auth_headers, test_user):
        response = client.post(
            f"/api/v1/user_roles/remove?user_id={test_user.id}&role_id=999",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "Role not assigned to user" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        response = client.post("/api/v1/user_roles/assign?user_id=1&role_id=1")
        assert response.status_code == 401
        response = client.post("/api/v1/user_roles/remove?user_id=1&role_id=1")
        assert response.status_code == 401
