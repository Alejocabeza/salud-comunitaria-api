# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, project_root)

from sqlmodel import Session
from src.core.database import get_engine
from src.models.role import Role
from src.models.role_permission import RolePermission
from src.models.permission import Permission
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_role_permissions(db: Session):
    role_permissions_data = {
        "admin": ["admin"],
        "outpatient_center": [
            'doctor.all',
            'patient.read',
        ],
        "doctor": [
        ],
        'patient': []
    }

    for role_name, permissions in role_permissions_data.items():
        role = db.query(Role).filter(Role.name == role_name).first()
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
    with Session(get_engine()) as session:
        create_role_permissions(session)
    print("Role-permission data seeding finished.")

if __name__ == "__main__":
    seed_data()