# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, project_root)

from sqlmodel import Session
from src.core.database import engine
from src.models.role import Role
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_roles(db: Session):
    roles_data = [
        {"name": "admin", "description": "Superuser role"},
        {"name": "outpatient_center", "description": "Outpatient center role"},
        {"name": "doctor", "description": "Doctor role"},
        {"name": "patient", "description": "Patient role"},
    ]

    for role in roles_data:
        existing_role = db.query(Role).filter(Role.name == role["name"]).first()
        if existing_role:
            print(f"Role '{role['name']}' already exists.")
            continue

        new_role = Role(
            name=role["name"],
            description=role["description"],
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        print(f"Role created: {new_role.name}")


def seed_data():
    print("Starting to seed data...")
    with Session(engine) as session:
        create_roles(session)
    print("Data seeding finished.")

if __name__ == "__main__":
    seed_data()