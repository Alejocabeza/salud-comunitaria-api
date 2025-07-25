import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.core.security import get_password_hash

class TestRoleRoutes:

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

    def test_create_role_success(self, client, session, auth_headers):
        role_data = {
            "name": "new_role",
            "description": "Un nuevo rol"
        }
        response = client.post("/api/v1/roles/", json=role_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "new_role"

    def test_create_role_duplicate(self, client, session, auth_headers):
        role_data = {
            "name": "duplicate_role",
            "description": "Rol duplicado"
        }
        client.post("/api/v1/roles/", json=role_data, headers=auth_headers)

        response = client.post("/api/v1/roles/", json=role_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Role already exists" in response.json()["detail"]

    def test_list_roles_success(self, client, session, auth_headers):
        for i in range(3):
            role_data = {
                "name": f"role_{i}",
                "description": f"Descripción del rol {i}"
            }
            client.post("/api/v1/roles/", json=role_data, headers=auth_headers)

        response = client.get("/api/v1/roles/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert all("name" in r for r in data)

    def test_unauthorized_access(self, client):
        role_data = {"name": "test_role"}
        response = client.post("/api/v1/roles/", json=role_data)
        assert response.status_code == 401
        response = client.get("/api/v1/roles/")
        assert response.status_code == 401
