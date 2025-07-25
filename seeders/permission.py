# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from sqlmodel import Session
from src.core.database import get_engine
from src.models.permission import Permission
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_roles(db: Session):
    permission_data = [
        # Admin Permission
        {"name": "admin", "description": "Permission to manage all aspects of the system"},

        # Role Permission
        {"name": "role.all", "description": "Permission to manage all roles"},
        {"name": "role.store", "description": "Permission to store role data"},
        {"name": "role.update", "description": "Permission to update role data"},
        {"name": "role.delete", "description": "Permission to delete role data"},
        {"name": "role.read", "description": "Permission to read role data"},

        # Permission Permission
        {"name": "permission.all", "description": "Permission to manage all permissions"},
        {"name": "permission.store", "description": "Permission to store permission data"},
        {"name": "permission.update", "description": "Permission to update permission data"},
        {"name": "permission.delete", "description": "Permission to delete permission data"},
        {"name": "permission.read", "description": "Permission to read permission data"},

        # Outpatient Center Permission
        {"name": "outpatient_center.all", "description": "Permission to manage outpatient center operations"},
        {"name": "outpatient_center.store", "description": "Permission to store outpatient center data"},
        {"name": "outpatient_center.update", "description": "Permission to update outpatient center data"},
        {"name": "outpatient_center.delete", "description": "Permission to delete outpatient center data"},
        {"name": "outpatient_center.read", "description": "Permission to read outpatient center data"},

        # Doctor Permission
        {"name": "doctor.all", "description": "Permission to manage all doctors"},
        {"name": "doctor.store", "description": "Permission to store doctor data"},
        {"name": "doctor.update", "description": "Permission to update doctor data"},
        {"name": "doctor.delete", "description": "Permission to delete doctor data"},
        {"name": "doctor.read", "description": "Permission to read doctor data"},

        # Patient Permission
        {"name": "patient.all", "description": "Permission to manage all patients"},
        {"name": "patient.store", "description": "Permission to store patient data"},
        {"name": "patient.update", "description": "Permission to update patient data"},
        {"name": "patient.delete", "description": "Permission to delete patient data"},
        {"name": "patient.read", "description": "Permission to read patient data"},

        # Medication Request Permission
        {"name": "medication_request.all", "description": "Permission to manage all medication requests"},
        {"name": "medication_request.store", "description": "Permission to store medication request data"},
        {"name": "medication_request.update", "description": "Permission to update medication request data"},
        {"name": "medication_request.delete", "description": "Permission to delete medication request data"},
        {"name": "medication_request.read", "description": "Permission to read medication request data"},

        # External Document Permission
        {"name": "external_document.all", "description": "Permission to manage all external documents"},
        {"name": "external_document.store", "description": "Permission to store external document data"},
        {"name": "external_document.update", "description": "Permission to update external document data"},
        {"name": "external_document.delete", "description": "Permission to delete external document data"},
        {"name": "external_document.read", "description": "Permission to read external document data"},

        # Medical Resource Permission
        {"name": "medical_resource.all", "description": "Permission to manage all medical resources"},
        {"name": "medical_resource.store", "description": "Permission to store medical resource data"},
        {"name": "medical_resource.update", "description": "Permission to update medical resource data"},
        {"name": "medical_resource.delete", "description": "Permission to delete medical resource data"},
        {"name": "medical_resource.read", "description": "Permission to read medical resource data"},

        
    ]

    for permission in permission_data:
        existing_permission = db.query(Permission).filter(Permission.name == permission["name"]).first()
        if existing_permission:
            print(f"Permission '{permission['name']}' already exists.")
            continue

        new_permission = Permission(
            name=permission["name"],
            description=permission["description"],
        )
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)
        print(f"Permission created: {new_permission.name}")


def seed_data():
    print("Starting to seed data...")
    with Session(get_engine()) as session:
        create_roles(session)
    print("Data seeding finished.")

if __name__ == "__main__":
    seed_data()