import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.patient import Patient
from src.models.external_document import ExternalDocument
from src.core.security import get_password_hash
import base64
import os

class TestExternalDocumentRoutes:

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

        patient = Patient(
            name="Test Patient",
            birthdate="2000-01-01",
            phone="123456789",
            email="patient@test.com",
            outpatient_center_id=1,
            user_id=user.id
        )
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return patient

    @pytest.fixture
    def patient_auth_headers(self, client, patient_user):
        """Obtiene headers de autenticación para el usuario paciente"""
        response = client.post("/api/v1/auths/login", data={
            "username": "patient_test",
            "password": "testpass"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_upload_external_document_success(self, client, session, auth_headers, patient_user):
        file_content = "This is a test document."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        
        doc_data = {
            "filename": "test_document.txt",
            "file_base64": encoded_content,
            "description": "A test document",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        
        response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test_document.txt"
        assert "file_url" in data
        assert os.path.exists(data["file_url"])
        
        # Clean up the created file
        os.remove(data["file_url"])

    def test_upload_external_document_invalid_file_type(self, client, auth_headers, patient_user):
        file_content = "This is a test document."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        
        doc_data = {
            "filename": "test_document.exe",
            "file_base64": encoded_content,
            "description": "An executable file",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        
        response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Tipo de archivo no permitido" in response.json()["detail"]

    def test_upload_external_document_file_too_large(self, client, auth_headers, patient_user):
        # Create a large file (e.g., 6MB, exceeding default 5MB limit)
        large_content = "A" * (6 * 1024 * 1024)  # 6MB of 'A's
        encoded_content = base64.b64encode(large_content.encode()).decode()
        
        doc_data = {
            "filename": "large_document.txt",
            "file_base64": encoded_content,
            "description": "A large document",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        
        response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        assert response.status_code == 400
        assert "El archivo excede el tamaño máximo permitido" in response.json()["detail"]

    def test_list_documents_by_patient_success(self, client, session, auth_headers, patient_user):
        # Upload a document for the patient
        file_content = "Patient document."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        doc_data = {
            "filename": "patient_doc.txt",
            "file_base64": encoded_content,
            "description": "Patient's document",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)

        response = client.get(f"/api/v1/external_document/patient/{patient_user.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["filename"] == "patient_doc.txt"
        
        # Clean up the created file
        os.remove(data[0]["file_url"])

    def test_get_external_document_success(self, client, session, auth_headers, patient_user):
        file_content = "Document to retrieve."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        doc_data = {
            "filename": "retrieve_doc.txt",
            "file_base64": encoded_content,
            "description": "Document to retrieve",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        doc_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/external_document/{doc_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "retrieve_doc.txt"
        
        # Clean up the created file
        os.remove(data["file_url"])

    def test_get_external_document_not_found(self, client, auth_headers):
        response = client.get("/api/v1/external_document/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Documento no encontrado" in response.json()["detail"]

    def test_delete_external_document_success_by_uploader(self, client, session, patient_auth_headers, patient_user):
        file_content = "Document to delete."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        doc_data = {
            "filename": "delete_doc_uploader.txt",
            "file_base64": encoded_content,
            "description": "Document to delete by uploader",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/external_document/", json=doc_data, headers=patient_auth_headers)
        doc_id = create_response.json()["id"]
        file_url = create_response.json()["file_url"]
        
        response = client.delete(f"/api/v1/external_document/{doc_id}", headers=patient_auth_headers)
        assert response.status_code == 200
        assert "Documento eliminado" in response.json()["msg"]
        assert not os.path.exists(file_url)

    def test_delete_external_document_success_by_outpatient_center(self, client, session, auth_headers, patient_user):
        file_content = "Document to delete by outpatient center."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        doc_data = {
            "filename": "delete_doc_outpatient.txt",
            "file_base64": encoded_content,
            "description": "Document to delete by outpatient center",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        doc_id = create_response.json()["id"]
        file_url = create_response.json()["file_url"]
        
        response = client.delete(f"/api/v1/external_document/{doc_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Documento eliminado" in response.json()["msg"]
        assert not os.path.exists(file_url)

    def test_delete_external_document_not_found(self, client, auth_headers):
        response = client.delete("/api/v1/external_document/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Documento no encontrado" in response.json()["detail"]

    def test_delete_external_document_unauthorized(self, client, session, auth_headers, patient_auth_headers, patient_user):
        # Create a document by outpatient_center_user
        file_content = "Document to delete by unauthorized user."
        encoded_content = base64.b64encode(file_content.encode()).decode()
        doc_data = {
            "filename": "unauthorized_delete.txt",
            "file_base64": encoded_content,
            "description": "Document to delete by unauthorized user",
            "patient_id": patient_user.id,
            "outpatient_center_id": 1
        }
        create_response = client.post("/api/v1/external_document/", json=doc_data, headers=auth_headers)
        doc_id = create_response.json()["id"]
        file_url = create_response.json()["file_url"]

        # Attempt to delete with patient_auth_headers (who is not the uploader and not outpatient_center)
        response = client.delete(f"/api/v1/external_document/{doc_id}", headers=patient_auth_headers)
        assert response.status_code == 403
        assert "No tienes permiso para borrar este documento" in response.json()["detail"]
        
        # Clean up the created file
        os.remove(file_url)

    def test_unauthorized_access(self, client):
        response = client.post("/api/v1/external_document/", json={})
        assert response.status_code == 401
        response = client.get("/api/v1/external_document/patient/1")
        assert response.status_code == 401
        response = client.get("/api/v1/external_document/1")
        assert response.status_code == 401
        response = client.delete("/api/v1/external_document/1")
        assert response.status_code == 401
