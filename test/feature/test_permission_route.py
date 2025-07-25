import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.permission import Permission
from src.core.security import get_password_hash

class TestPermissionRoutes:

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

    def test_create_permission_success(self, client, session, auth_headers):
        permission_data = {
            "name": "create_user",
            "description": "Permite crear usuarios"
        }
        response = client.post("/api/v1/permissions/", json=permission_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "create_user"

    def test_create_permission_duplicate(self, client, session, auth_headers):
        permission_data = {
            "name": "duplicate_permission",
            "description": "Permiso duplicado"
        }
        client.post("/api/v1/permissions/", json=permission_data, headers=auth_headers)

        response = client.post("/api/v1/permissions/", json=permission_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Permission already exists" in response.json()["detail"]

    def test_list_permissions_success(self, client, session, auth_headers):
        for i in range(3):
            permission_data = {
                "name": f"permission_{i}",
                "description": f"Descripción del permiso {i}"
            }
            client.post("/api/v1/permissions/", json=permission_data, headers=auth_headers)

        response = client.get("/api/v1/permissions/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert all("name" in p for p in data)

    def test_unauthorized_access(self, client):
        permission_data = {"name": "test_permission"}
        response = client.post("/api/v1/permissions/", json=permission_data)
        assert response.status_code == 401
        response = client.get("/api/v1/permissions/")
        assert response.status_code == 401
