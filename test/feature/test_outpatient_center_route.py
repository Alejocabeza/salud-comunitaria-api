import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.outpatient_center import OutpatientCenter
from src.core.security import get_password_hash

class TestOutpatientCenterRoutes:

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

    def test_create_outpatient_center_success(self, client, session, auth_headers):
        center_data = {
            "name": "Centro Ambulatorio Test",
            "address": "Calle Falsa 123",
            "phone": "123456789",
            "email": "centro@test.com",
            "responsible": "Dr. Smith"
        }
        response = client.post("/api/v1/outpatient_center/", json=center_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Centro Ambulatorio Test"
        assert data["user"]["username"] == "centro_ambulatorio_test"

    def test_list_outpatient_centers_success(self, client, session, auth_headers):
        # Create some centers first
        for i in range(3):
            center_data = {
                "name": f"Centro {i}",
                "address": f"Dirección {i}",
                "phone": f"11122233{i}",
                "email": f"centro{i}@test.com",
                "responsible": f"Responsable {i}"
            }
            client.post("/api/v1/outpatient_center/", json=center_data, headers=auth_headers)
        
        response = client.get("/api/v1/outpatient_center/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3 # May contain centers from other tests
        assert all("name" in c for c in data)

    def test_get_outpatient_center_success(self, client, session, auth_headers):
        center_data = {
            "name": "Centro Get Test",
            "address": "Dirección Get",
            "phone": "999888777",
            "email": "get@test.com",
            "responsible": "Dr. Get"
        }
        create_response = client.post("/api/v1/outpatient_center/", json=center_data, headers=auth_headers)
        center_id = create_response.json()["id"]

        response = client.get(f"/api/v1/outpatient_center/{center_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Centro Get Test"

    def test_get_outpatient_center_not_found(self, client, auth_headers):
        response = client.get("/api/v1/outpatient_center/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Centro ambulatorio no encontrado" in response.json()["detail"]

    def test_update_outpatient_center_success(self, client, session, auth_headers):
        center_data = {
            "name": "Centro Update Test",
            "address": "Dirección Update",
            "phone": "555444333",
            "email": "update@test.com",
            "responsible": "Dr. Update"
        }
        create_response = client.post("/api/v1/outpatient_center/", json=center_data, headers=auth_headers)
        center_id = create_response.json()["id"]

        update_data = {
            "name": "Centro Actualizado",
            "address": "Nueva Dirección"
        }
        response = client.patch(f"/api/v1/outpatient_center/{center_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Centro Actualizado"
        assert data["address"] == "Nueva Dirección"

    def test_update_outpatient_center_not_found(self, client, auth_headers):
        update_data = {"name": "No Existe"}
        response = client.patch("/api/v1/outpatient_center/999", json=update_data, headers=auth_headers)
        assert response.status_code == 404
        assert "Centro ambulatorio no encontrado" in response.json()["detail"]

    def test_delete_outpatient_center_success(self, client, session, auth_headers):
        center_data = {
            "name": "Centro Delete Test",
            "address": "Dirección Delete",
            "phone": "111000999",
            "email": "delete@test.com",
            "responsible": "Dr. Delete"
        }
        create_response = client.post("/api/v1/outpatient_center/", json=center_data, headers=auth_headers)
        center_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/outpatient_center/{center_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Centro ambulatorio y usuario asociado eliminados" in response.json()["msg"]

        get_response = client.get(f"/api/v1/outpatient_center/{center_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_outpatient_center_not_found(self, client, auth_headers):
        response = client.delete("/api/v1/outpatient_center/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Centro ambulatorio no encontrado" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        center_data = {"name": "Test", "address": "Test", "email": "test@test.com"}
        response = client.post("/api/v1/outpatient_center/", json=center_data)
        assert response.status_code == 401
        response = client.get("/api/v1/outpatient_center/")
        assert response.status_code == 401
        response = client.get("/api/v1/outpatient_center/1")
        assert response.status_code == 401
        response = client.patch("/api/v1/outpatient_center/1", json=center_data)
        assert response.status_code == 401
        response = client.delete("/api/v1/outpatient_center/1")
        assert response.status_code == 401
