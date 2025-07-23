# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from sqlmodel import Session
from src.core.database import engine
from src.models.user import Role, UserRoleLink as UserRole
from passlib.context import CryptContext

def create_auth_roles(db: Session):
    auth_roles_data = {
        1: ["admin"], 
    }

    for auth_id, roles in auth_roles_data.items():
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                print(f"Role '{role_name}' does not exist.")
                continue

            existing_auth_role = db.query(UserRole).filter(
                UserRole.user_id == auth_id,
                UserRole.role_id == role.id
            ).first()

            if existing_auth_role:
                print(f"Role '{role_name}' is already assigned to auth ID '{auth_id}'.")
                continue

            auth_role = UserRole(user_id=auth_id, role_id=role.id)
            db.add(auth_role)
        db.commit()
        print(f"Roles assigned to auth ID: {auth_id}")


def seed_data():
    print("Starting to seed auth-role data...")
    with Session(engine) as session:
        create_auth_roles(session)
    print("Auth-role data seeding finished.")

if __name__ == "__main__":
    seed_data()