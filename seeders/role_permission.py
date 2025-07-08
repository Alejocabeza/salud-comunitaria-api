# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, project_root)

from sqlmodel import Session
from src.config.database import engine
from src.models.permission import RolePermission, Permission
from src.models.role import Roles
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_role_permissions(db: Session):
    role_permissions_data = {
        "admin": ["admin"],
        "outpatient_center": ["outpatient_center.store", "outpatient_center.update", "outpatient_center.delete", "outpatient_center.read", 'doctor.store', 'doctor.delete', 'doctor.read', 'patient.read'],
        "doctor": ["doctor.store", "doctor.update", "doctor.delete", "doctor.read", 'patient.store', 'patient.update', 'patient.delete', 'patient.read'],
        "patient": ["patient.store", "patient.update", "patient.delete", "patient.read"],
    }

    for role_name, permissions in role_permissions_data.items():
        role = db.query(Roles).filter(Roles.name == role_name).first()
        if not role:
            print(f"Role '{role_name}' does not exist.")
            continue

        for permission_name in permissions:
            permission = db.query(Permission).filter(Permission.name == permission_name).first()
            if not permission:
                print(f"Permission '{permission_name}' does not exist.")
                continue

            existing_role_permission = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            ).first()

            if existing_role_permission:
                print(f"Permission '{permission_name}' is already assigned to role '{role_name}'.")
                continue

            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            db.add(role_permission)
        db.commit()
        print(f"Permissions assigned to role: {role_name}")


def seed_data():
    print("Starting to seed role-permission data...")
    with Session(engine) as session:
        create_role_permissions(session)
    print("Role-permission data seeding finished.")

if __name__ == "__main__":
    seed_data()