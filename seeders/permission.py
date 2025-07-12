# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from sqlmodel import Session
from src.config.database import engine
from src.models.permission import Permission
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_roles(db: Session):
    permission_data = [
        # Admin Permission
        {"name": "admin", "description": "Permission to manage all aspects of the system"},

        # Outpatient Center Permission
        {"name": "outpatient_center.all", "description": "Permission to manage outpatient center operations"},
        {"name": "outpatient_center.store", "description": "Permission to store outpatient center data"},
        {"name": "outpatient_center.update", "description": "Permission to update outpatient center data"},
        {"name": "outpatient_center.delete", "description": "Permission to delete outpatient center data"},
        {"name": "outpatient_center.read", "description": "Permission to read outpatient center data"},

        # Doctor Permission
        {"name": "doctor.all", "description": "Permission to manage all aspects of doctor operations"},
        {"name": "doctor.store", "description": "Permission to store doctor data"},
        {"name": "doctor.update", "description": "Permission to update doctor data"},
        {"name": "doctor.delete", "description": "Permission to delete doctor data"},
        {"name": "doctor.read", "description": "Permission to read doctor data"},

        # Patient Permission
        {"name": "patient.all", "description": "Permission to manage all aspects of patient operations"},
        {"name": "patient.store", "description": "Permission to store patient data"},
        {"name": "patient.update", "description": "Permission to update patient data"},
        {"name": "patient.delete", "description": "Permission to delete patient data"},
        {"name": "patient.read", "description": "Permission to read patient data"},

        # Role Permission
        {"name": "role.all", "description": "Permission to manage all aspects of role operations"},
        {"name": "role.store", "description": "Permission to store role data"},
        {"name": "role.update", "description": "Permission to update role data"},
        {"name": "role.delete", "description": "Permission to delete role data"},
        {"name": "role.read", "description": "Permission to read role data"},

        # Permission Permission
        {"name": "permission.all", "description": "Permission to manage all aspects of permission operations"},
        {"name": "permission.store", "description": "Permission to store permission data"},
        {"name": "permission.update", "description": "Permission to update permission data"},
        {"name": "permission.delete", "description": "Permission to delete permission data"},
        {"name": "permission.read", "description": "Permission to read permission data"},

        # Resource Permission
        {"name": "resource.all", "description": "Permission to manage all aspects of resource operations"},
        {"name": "resource.store", "description": "Permission to store resource data"},
        {"name": "resource.update", "description": "Permission to update resource data"},
        {"name": "resource.delete", "description": "Permission to delete resource data"},
        {"name": "resource.read", "description": "Permission to read resource data"},
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
    with Session(engine) as session:
        create_roles(session)
    print("Data seeding finished.")

if __name__ == "__main__":
    seed_data()