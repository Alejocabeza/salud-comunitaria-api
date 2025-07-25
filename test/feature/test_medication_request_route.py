import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.medication_request import MedicationRequest
from src.models.outpatient_center import OutpatientCenter
from src.models.outpatient_center import OutpatientCenter
from src.models.outpatient_center import OutpatientCenter
from src.models.outpatient_center import OutpatientCenter
from src.models.outpatient_center import OutpatientCenter
from src.models.outpatient_center import OutpatientCenter
from src.core.security import get_password_hash

class TestMedicationRequestRoutes:

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

        outpatient_center = OutpatientCenter(
            name="Test Outpatient Center",
            address="123 Test St",
            phone="123-456-7890",
            email="test@example.com",
            responsible="Test Admin",
            user_id=user.id
        )
        session.add(outpatient_center)
        session.commit()
        session.refresh(outpatient_center)
        
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

    @pytest.fixture
    def doctor_user(self, session):
        """Crea un usuario con rol doctor para los tests"""
        role = Role(name="doctor", description="Doctor")
        session.add(role)
        session.commit()
        session.refresh(role)

        user = User(
            username="doctor_test",
            email="doctor@test.com",
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
    def doctor_auth_headers(self, client, doctor_user):
        """Obtiene headers de autenticación para el usuario doctor"""
        response = client.post("/api/v1/auths/login", data={
            "username": "doctor_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.fixture
    def patient_user(self, session):
        """Crea un usuario con rol patient para los tests"""
        role = Role(name="patient", description="Paciente")
        session.add(role)
        session.commit()
        session.refresh(role)

        user = User(
            username="patient_test",
            email="patient@test.com",
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
    def patient_auth_headers(self, client, patient_user):
        """Obtiene headers de autenticación para el usuario paciente"""
        response = client.post("/api/v1/auths/login", data={
            "username": "patient_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_medication_request_success_doctor(self, client, session, doctor_auth_headers):
        request_data = {
            "medication_name": "Paracetamol",
            "quantity": 10,
            "reason": "Dolor de cabeza",
            "outpatient_center_id": 1
        }
        response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["medication_name"] == "Paracetamol"
        assert data["status"] == "pending"

    def test_create_medication_request_success_patient(self, client, session, patient_auth_headers):
        request_data = {
            "medication_name": "Ibuprofeno",
            "quantity": 5,
            "reason": "Fiebre",
            "outpatient_center_id": 1
        }
        response = client.post("/api/v1/medication_request/", json=request_data, headers=patient_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["medication_name"] == "Ibuprofeno"
        assert data["status"] == "pending"

    def test_create_medication_request_unauthorized_role(self, client, session, auth_headers):
        request_data = {
            "medication_name": "Aspirina",
            "quantity": 20,
            "reason": "Dolor muscular",
            "outpatient_center_id": 1
        }
        response = client.post("/api/v1/medication_request/", json=request_data, headers=auth_headers)
        assert response.status_code == 403
        assert "No tienes permiso para solicitar medicamentos." in response.json()["detail"]

    def test_list_medication_requests_outpatient_center(self, client, session, auth_headers, doctor_auth_headers):
        # Create a request by doctor
        request_data = {
            "medication_name": "Amoxicilina",
            "quantity": 1,
            "reason": "Infección",
            "outpatient_center_id": 1
        }
        client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)

        response = client.get("/api/v1/medication_request/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(r["medication_name"] == "Amoxicilina" for r in data)

    def test_list_medication_requests_doctor(self, client, session, doctor_auth_headers):
        # Create a request by doctor
        request_data = {
            "medication_name": "Cefalexina",
            "quantity": 2,
            "reason": "Infección de garganta",
            "outpatient_center_id": 1
        }
        client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)

        response = client.get("/api/v1/medication_request/", headers=doctor_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(r["medication_name"] == "Cefalexina" for r in data)

    def test_get_medication_request_success(self, client, session, auth_headers, doctor_auth_headers):
        request_data = {
            "medication_name": "Omeprazol",
            "quantity": 30,
            "reason": "Acidez",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        response = client.get(f"/api/v1/medication_request/{request_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["medication_name"] == "Omeprazol"

    def test_get_medication_request_not_found(self, client, auth_headers):
        response = client.get("/api/v1/medication_request/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Solicitud no encontrada" in response.json()["detail"]

    def test_get_medication_request_unauthorized(self, client, session, doctor_auth_headers, patient_auth_headers):
        # Create a request by doctor
        request_data = {
            "medication_name": "TestMed",
            "quantity": 1,
            "reason": "Test",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        # Patient tries to access doctor's request
        response = client.get(f"/api/v1/medication_request/{request_id}", headers=patient_auth_headers)
        assert response.status_code == 403
        assert "No tienes acceso a esta solicitud" in response.json()["detail"]

    def test_update_medication_request_success(self, client, session, auth_headers, doctor_auth_headers):
        request_data = {
            "medication_name": "Vitamina C",
            "quantity": 60,
            "reason": "Deficiencia",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        update_data = {"status": "approved"}
        response = client.patch(f"/api/v1/medication_request/{request_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"

    def test_update_medication_request_not_found(self, client, auth_headers):
        update_data = {"status": "approved"}
        response = client.patch("/api/v1/medication_request/999", json=update_data, headers=auth_headers)
        assert response.status_code == 404
        assert "Solicitud no encontrada" in response.json()["detail"]

    def test_update_medication_request_unauthorized(self, client, session, doctor_auth_headers):
        request_data = {
            "medication_name": "TestMed2",
            "quantity": 1,
            "reason": "Test",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        update_data = {"status": "approved"}
        response = client.patch(f"/api/v1/medication_request/{request_id}", json=update_data, headers=doctor_auth_headers)
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]

    def test_delete_medication_request_success(self, client, session, auth_headers, doctor_auth_headers):
        request_data = {
            "medication_name": "Antibiótico",
            "quantity": 14,
            "reason": "Infección",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/medication_request/{request_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Solicitud de medicamento eliminada" in response.json()["msg"]

        get_response = client.get(f"/api/v1/medication_request/{request_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_medication_request_not_found(self, client, auth_headers):
        response = client.delete("/api/v1/medication_request/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Solicitud no encontrada" in response.json()["detail"]

    def test_delete_medication_request_unauthorized(self, client, session, doctor_auth_headers):
        request_data = {
            "medication_name": "TestMed3",
            "quantity": 1,
            "reason": "Test",
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/medication_request/", json=request_data, headers=doctor_auth_headers)
        request_id = create_response.json()["id"]

        response = client.delete(f"/api/v1/medication_request/{request_id}", headers=doctor_auth_headers)
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]

    def test_unauthorized_access(self, client):
        request_data = {"medication_name": "Test", "quantity": 1, "outpatient_center_id": 1}
        response = client.post("/api/v1/medication_request/", json=request_data)
        assert response.status_code == 401
        response = client.get("/api/v1/medication_request/")
        assert response.status_code == 401
        response = client.get("/api/v1/medication_request/1")
        assert response.status_code == 401
        response = client.patch("/api/v1/medication_request/1", json=request_data)
        assert response.status_code == 401
        response = client.delete("/api/v1/medication_request/1")
        assert response.status_code == 401
