import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.patient import Patient
from src.core.security import get_password_hash

class TestPatientRoutes:

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

    def test_create_patient_success(self, client, session, auth_headers):
        patient_data = {
            "name": "Juan Paciente",
            "birthdate": "1990-01-01",
            "phone": "123456789",
            "email": "juan.paciente@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "juan_paciente",
                "email": "juan.paciente@test.com",
                "password": "patientpass"
            }
        }
        response = client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Juan Paciente"
        assert data["user"]["username"] == "juan_paciente"

    def test_create_patient_duplicate_username(self, client, session, auth_headers):
        patient_data = {
            "name": "Duplicate User",
            "birthdate": "1990-01-01",
            "phone": "123456789",
            "email": "duplicate.user@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "duplicate_patient",
                "email": "duplicate.user@test.com",
                "password": "patientpass"
            }
        }
        client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)

        patient_data2 = {
            "name": "Another Duplicate User",
            "birthdate": "1990-01-01",
            "phone": "987654321",
            "email": "another.duplicate.user@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "duplicate_patient",
                "email": "another.duplicate.user@test.com",
                "password": "patientpass"
            }
        }
        response = client.post("/api/v1/patients/", json=patient_data2, headers=auth_headers)
        assert response.status_code == 400
        assert "El usuario ya existe" in response.json()["detail"]

    def test_create_patient_duplicate_email(self, client, session, auth_headers):
        patient_data = {
            "name": "Duplicate Email",
            "birthdate": "1990-01-01",
            "phone": "123456789",
            "email": "duplicate.email@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "duplicate_email_user",
                "email": "duplicate.email@test.com",
                "password": "patientpass"
            }
        }
        client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)

        patient_data2 = {
            "name": "Another Duplicate Email",
            "birthdate": "1990-01-01",
            "phone": "987654321",
            "email": "duplicate.email@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "another_duplicate_email_user",
                "email": "duplicate.email@test.com",
                "password": "patientpass"
            }
        }
        response = client.post("/api/v1/patients/", json=patient_data2, headers=auth_headers)
        assert response.status_code == 400
        assert "El email ya está registrado" in response.json()["detail"]

    def test_list_patients_success(self, client, session, auth_headers):
        for i in range(3):
            patient_data = {
                "name": f"Paciente {i}",
                "birthdate": "1990-01-01",
                "phone": f"11122233{i}",
                "email": f"patient{i}@test.com",
                "outpatient_center_id": 1,
                "user": {
                    "username": f"patient_user_{i}",
                    "email": f"patient{i}@test.com",
                    "password": "patientpass"
                }
            }
            client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)

        response = client.get("/api/v1/patients/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert all("name" in p for p in data)

    def test_get_patient_success(self, client, session, auth_headers):
        patient_data = {
            "name": "Paciente Get",
            "birthdate": "1990-01-01",
            "phone": "999888777",
            "email": "get.patient@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "get_patient_user",
                "email": "get.patient@test.com",
                "password": "patientpass"
            }
        }
        create_response = client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)
        patient_id = create_response.json()["id"]

        response = client.get(f"/api/v1/patients/{patient_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Paciente Get"

    def test_get_patient_not_found(self, client, auth_headers):
        response = client.get("/api/v1/patients/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Paciente no encontrado" in response.json()["detail"]

    def test_update_patient_success(self, client, session, auth_headers):
        patient_data = {
            "name": "Paciente Update",
            "birthdate": "1990-01-01",
            "phone": "555444333",
            "email": "update.patient@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "update_patient_user",
                "email": "update.patient@test.com",
                "password": "patientpass"
            }
        }
        create_response = client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)
        patient_id = create_response.json()["id"]

        update_data = {
            "name": "Paciente Actualizado",
            "phone": "111222333"
        }
        response = client.patch(f"/api/v1/patients/{patient_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Paciente Actualizado"
        assert data["phone"] == "111222333"

    def test_update_patient_not_found(self, client, auth_headers):
        update_data = {"name": "No Existe"}
        response = client.patch("/api/v1/patients/999", json=update_data, headers=auth_headers)
        assert response.status_code == 404
        assert "Paciente no encontrado" in response.json()["detail"]

    def test_delete_patient_success(self, client, session, auth_headers):
        patient_data = {
            "name": "Paciente Delete",
            "birthdate": "1990-01-01",
            "phone": "111000999",
            "email": "delete.patient@test.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "delete_patient_user",
                "email": "delete.patient@test.com",
                "password": "patientpass"
            }
        }
        create_response = client.post("/api/v1/patients/", json=patient_data, headers=auth_headers)
        patient_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/patients/{patient_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Paciente y usuario asociado eliminados" in response.json()["msg"]

        get_response = client.get(f"/api/v1/patients/{patient_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_patient_not_found(self, client, auth_headers):
        response = client.delete("/api/v1/patients/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Paciente no encontrado" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        patient_data = {"name": "Test", "birthdate": "1990-01-01", "outpatient_center_id": 1, "user": {"username": "test_user", "email": "test@test.com", "password": "testpass"}}
        response = client.post("/api/v1/patients/", json=patient_data)
        assert response.status_code == 401
        response = client.get("/api/v1/patients/")
        assert response.status_code == 401
        response = client.get("/api/v1/patients/1")
        assert response.status_code == 401
        response = client.patch("/api/v1/patients/1", json=patient_data)
        assert response.status_code == 401
        response = client.delete("/api/v1/patients/1")
        assert response.status_code == 401
