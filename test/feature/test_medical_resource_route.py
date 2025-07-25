import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.medical_resource import MedicalResource
from src.core.security import get_password_hash

class TestMedicalResourceRoutes:

    @pytest.fixture
    def outpatient_center_user(self, session):
        """Crea un usuario con rol outpatient_center para los tests"""
        role = Role(name="outpatient_center", description="Centro ambulatorio")
        session.add(role)
        session.commit()
        session.refresh(role)
        
        user = User(
            username="ambulatorio_test",
            email="ambulatorio@test.com",
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
    def auth_headers(self, client, outpatient_center_user):
        """Obtiene headers de autenticación para el usuario ambulatorio"""
        response = client.post("/api/v1/auths/login", data={
            "username": "ambulatorio_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_medical_resource_success(self, client, session, auth_headers):
        resource_data = {
            "name": "Jeringas",
            "description": "Jeringas de 5ml",
            "quantity": 100,
            "unit": "unidades",
            "outpatient_center_id": 1
        }
        response = client.post("/api/v1/medical_resource/", json=resource_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jeringas"
        assert data["quantity"] == 100

    def test_list_medical_resources_success(self, client, session, auth_headers):
        # Create some resources first
        for i in range(3):
            resource_data = {
                "name": f"Recurso {i}",
                "description": f"Descripción {i}",
                "quantity": i * 10,
                "unit": "unidades",
                "outpatient_center_id": 1
            }
            client.post("/api/v1/medical_resource/", json=resource_data, headers=auth_headers)
        
        response = client.get("/api/v1/medical_resource/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3 # May contain resources from other tests
        assert all("name" in r for r in data)

    def test_get_medical_resource_success(self, client, session, auth_headers):
        resource_data = {
            "name": "Vendas",
            "description": "Vendas elásticas",
            "quantity": 50,
            "unit": "rollos",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medical_resource/", json=resource_data, headers=auth_headers)
        resource_id = create_response.json()["id"]

        response = client.get(f"/api/v1/medical_resource/{resource_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Vendas"
        assert data["quantity"] == 50

    def test_get_medical_resource_not_found(self, client, auth_headers):
        response = client.get("/api/v1/medical_resource/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Recurso médico no encontrado" in response.json()["detail"]

    def test_update_medical_resource_success(self, client, session, auth_headers):
        resource_data = {
            "name": "Alcohol",
            "description": "Alcohol etílico",
            "quantity": 20,
            "unit": "litros",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medical_resource/", json=resource_data, headers=auth_headers)
        resource_id = create_response.json()["id"]

        update_data = {
            "quantity": 30,
            "unit": "ml"
        }
        response = client.patch(f"/api/v1/medical_resource/{resource_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 30
        assert data["unit"] == "ml"

    def test_update_medical_resource_not_found(self, client, auth_headers):
        update_data = {"quantity": 10}
        response = client.patch("/api/v1/medical_resource/999", json=update_data, headers=auth_headers)
        assert response.status_code == 404
        assert "Recurso médico no encontrado" in response.json()["detail"]

    def test_delete_medical_resource_success(self, client, session, auth_headers):
        resource_data = {
            "name": "Guantes",
            "description": "Guantes de látex",
            "quantity": 500,
            "unit": "pares",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medical_resource/", json=resource_data, headers=auth_headers)
        resource_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/medical_resource/{resource_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Recurso médico eliminado" in response.json()["msg"]

        get_response = client.get(f"/api/v1/medical_resource/{resource_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_medical_resource_not_found(self, client, auth_headers):
        response = client.delete("/api/v1/medical_resource/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Recurso médico no encontrado" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        resource_data = {"name": "Test", "quantity": 10, "outpatient_center_id": 1}
        response = client.post("/api/v1/medical_resource/", json=resource_data)
        assert response.status_code == 401
        response = client.get("/api/v1/medical_resource/")
        assert response.status_code == 401
        response = client.get("/api/v1/medical_resource/1")
        assert response.status_code == 401
        response = client.patch("/api/v1/medical_resource/1", json=resource_data)
        assert response.status_code == 401
        response = client.delete("/api/v1/medical_resource/1")
        assert response.status_code == 401
