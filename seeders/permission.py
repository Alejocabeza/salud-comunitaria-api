# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from sqlmodel import Session
from src.core.database import engine
from src.models.user import Permission
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
        {"name": "doctor.all", "description": "Permission to manage all doctors"},
        {"name": "doctor.store", "description": "Permission to store doctor data"},
        {"name": "doctor.update", "description": "Permission to update doctor data"},
        {"name": "doctor.delete", "description": "Permission to delete doctor data"},
        {"name": "doctor.read", "description": "Permission to read doctor data"},
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