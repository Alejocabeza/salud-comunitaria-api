import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.permission import Permission
from src.models.role_permission import RolePermission
from src.core.security import get_password_hash

class TestRolePermissionsRoutes:

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
    def test_role(self, session):
        role = Role(name="test_role", description="Rol de prueba")
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

    @pytest.fixture
    def test_permission(self, session):
        permission = Permission(name="test_permission", description="Permiso de prueba")
        session.add(permission)
        session.commit()
        session.refresh(permission)
        return permission

    def test_assign_permission_to_role_success(self, client, session, auth_headers, test_role, test_permission):
        response = client.post(
            f"/api/v1/role_permissions/assign?role_id={test_role.id}&permission_id={test_permission.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Permission 'test_permission' assigned to role 'test_role'" in response.json()["msg"]

    def test_assign_permission_to_role_not_found(self, client, auth_headers, test_role):
        response = client.post(
            f"/api/v1/role_permissions/assign?role_id={test_role.id}&permission_id=999",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "Role or Permission not found" in response.json()["detail"]

    def test_assign_permission_to_role_already_assigned(self, client, session, auth_headers, test_role, test_permission):
        # Assign first
        client.post(
            f"/api/v1/role_permissions/assign?role_id={test_role.id}&permission_id={test_permission.id}",
            headers=auth_headers
        )
        # Assign again
        response = client.post(
            f"/api/v1/role_permissions/assign?role_id={test_role.id}&permission_id={test_permission.id}",
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Permission already assigned to role" in response.json()["detail"]

    def test_remove_permission_from_role_success(self, client, session, auth_headers, test_role, test_permission):
        # Assign first
        link = RolePermission(role_id=test_role.id, permission_id=test_permission.id)
        session.add(link)
        session.commit()

        response = client.post(
            f"/api/v1/role_permissions/remove?role_id={test_role.id}&permission_id={test_permission.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Permission removed from role" in response.json()["msg"]

    def test_remove_permission_from_role_not_found(self, client, auth_headers, test_role):
        response = client.post(
            f"/api/v1/role_permissions/remove?role_id={test_role.id}&permission_id=999",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "Permission not assigned to role" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        response = client.post("/api/v1/role_permissions/assign?role_id=1&permission_id=1")
        assert response.status_code == 401
        response = client.post("/api/v1/role_permissions/remove?role_id=1&permission_id=1")
        assert response.status_code == 401
