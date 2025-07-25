import pytest
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.doctor import Doctor
from src.core.security import get_password_hash

class TestDoctorRoutes:

    @pytest.fixture
    def outpatient_center_user(self, session):
        """Crea un usuario con rol outpatient_center para los tests"""
        # Crear rol outpatient_center
        role = Role(name="outpatient_center", description="Centro ambulatorio")
        session.add(role)
        session.commit()
        session.refresh(role)
        
        # Crear usuario
        user = User(
            username="ambulatorio_test",
            email="ambulatorio@test.com",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Asignar rol
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

    def test_create_doctor_success(self, client, session, auth_headers):
        doctor_data = {
            "name": "Dr. Juan Pérez",
            "specialty": "Cardiología",
            "phone": "123456789",
            "email": "juan.perez@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_juan",
                "email": "juan.perez@hospital.com",
                "password": "doctorpass123"
            }
        }
        
        response = client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Dr. Juan Pérez"
        assert data["specialty"] == "Cardiología"
        assert data["user"]["username"] == "dr_juan"
        assert "user_id" in data

    def test_create_doctor_duplicate_username(self, client, session, auth_headers):
        # Crear primer doctor
        doctor_data = {
            "name": "Dr. Ana García",
            "specialty": "Pediatría",
            "phone": "987654321",
            "email": "ana@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_ana",
                "email": "ana@hospital.com",
                "password": "doctorpass123"
            }
        }
        client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        
        # Intentar crear segundo doctor con mismo username
        doctor_data2 = {
            "name": "Dr. Ana López",
            "specialty": "Neurología",
            "phone": "555666777",
            "email": "ana.lopez@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_ana",  # Username duplicado
                "email": "ana.lopez@hospital.com",
                "password": "doctorpass456"
            }
        }
        
        response = client.post("/api/v1/doctors/", json=doctor_data2, headers=auth_headers)
        assert response.status_code == 400
        assert "El usuario ya existe" in response.json()["detail"]

    def test_create_doctor_duplicate_email(self, client, session, auth_headers):
        # Crear primer doctor
        doctor_data = {
            "name": "Dr. Carlos Ruiz",
            "specialty": "Dermatología",
            "phone": "111222333",
            "email": "carlos@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_carlos",
                "email": "carlos@hospital.com",
                "password": "doctorpass123"
            }
        }
        client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        
        # Intentar crear segundo doctor con mismo email
        doctor_data2 = {
            "name": "Dr. Carlos Mendez",
            "specialty": "Oftalmología",
            "phone": "444555666",
            "email": "carlos.mendez@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_carlos_m",
                "email": "carlos@hospital.com",  # Email duplicado
                "password": "doctorpass456"
            }
        }
        
        response = client.post("/api/v1/doctors/", json=doctor_data2, headers=auth_headers)
        assert response.status_code == 400
        assert "El email ya está registrado" in response.json()["detail"]

    def test_list_doctors(self, client, session, auth_headers):
        # Crear algunos doctores primero
        for i in range(3):
            doctor_data = {
                "name": f"Dr. Test {i}",
                "specialty": f"Especialidad {i}",
                "phone": f"12345678{i}",
                "email": f"test{i}@hospital.com",
                "outpatient_center_id": 1,
                "user": {
                    "username": f"dr_test_{i}",
                    "email": f"test{i}@hospital.com",
                    "password": "testpass123"
                }
            }
            client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        
        response = client.get("/api/v1/doctors/", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3
        assert all("name" in doctor for doctor in data)
        assert all("user" in doctor for doctor in data)

    def test_get_doctor_success(self, client, session, auth_headers):
        # Crear un doctor
        doctor_data = {
            "name": "Dr. María González",
            "specialty": "Ginecología",
            "phone": "999888777",
            "email": "maria@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_maria",
                "email": "maria@hospital.com",
                "password": "doctorpass123"
            }
        }
        create_response = client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        doctor_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/doctors/{doctor_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Dr. María González"
        assert data["specialty"] == "Ginecología"

    def test_get_doctor_not_found(self, client, session, auth_headers):
        response = client.get("/api/v1/doctors/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Doctor no encontrado" in response.json()["detail"]

    def test_update_doctor_success(self, client, session, auth_headers):
        # Crear un doctor
        doctor_data = {
            "name": "Dr. Pedro Martínez",
            "specialty": "Traumatología",
            "phone": "777666555",
            "email": "pedro@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_pedro",
                "email": "pedro@hospital.com",
                "password": "doctorpass123"
            }
        }
        create_response = client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        doctor_id = create_response.json()["id"]
        
        # Actualizar el doctor
        update_data = {
            "name": "Dr. Pedro Martínez Actualizado",
            "specialty": "Traumatología y Ortopedia"
        }
        
        response = client.patch(f"/api/v1/doctors/{doctor_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Dr. Pedro Martínez Actualizado"
        assert data["specialty"] == "Traumatología y Ortopedia"
        assert data["phone"] == "777666555"  # No cambió

    def test_update_doctor_not_found(self, client, session, auth_headers):
        update_data = {"name": "Dr. No Existe"}
        response = client.patch("/api/v1/doctors/999", json=update_data, headers=auth_headers)
        assert response.status_code == 404
        assert "Doctor no encontrado" in response.json()["detail"]

    def test_delete_doctor_success(self, client, session, auth_headers):
        # Crear un doctor
        doctor_data = {
            "name": "Dr. Luis Fernández",
            "specialty": "Psiquiatría",
            "phone": "333444555",
            "email": "luis@hospital.com",
            "outpatient_center_id": 1,
            "user": {
                "username": "dr_luis",
                "email": "luis@hospital.com",
                "password": "doctorpass123"
            }
        }
        create_response = client.post("/api/v1/doctors/", json=doctor_data, headers=auth_headers)
        doctor_id = create_response.json()["id"]
        
        # Eliminar el doctor
        response = client.delete(f"/api/v1/doctors/{doctor_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Doctor y usuario asociado eliminados" in response.json()["msg"]
        
        # Verificar que ya no existe
        get_response = client.get(f"/api/v1/doctors/{doctor_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_doctor_not_found(self, client, session, auth_headers):
        response = client.delete("/api/v1/doctors/999", headers=auth_headers)
        assert response.status_code == 404
        assert "Doctor no encontrado" in response.json()["detail"]

    def test_unauthorized_access(self, client, session):
        """Test que verifica que sin autenticación no se puede acceder"""
        response = client.get("/api/v1/doctors/")
        assert response.status_code == 401