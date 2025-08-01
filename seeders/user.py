# seeders/seed_auth.py
import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from sqlmodel import Session
from src.core.database import get_engine
from src.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user(db: Session):
    existing_user = db.query(User).filter(User.email == "admin@example.com").first()
    if existing_user:
        print("Admin user already exists.")
        return

    hashed_password = pwd_context.hash('12345678')

    admin_user = User(
        username="Admin",
        email="admin@example.com",
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"Admin user created: {admin_user.email}")

def seed_data():
    print("Starting to seed data...")
    with Session(get_engine()) as session:
        create_admin_user(session)
    print("Data seeding finished.")

if __name__ == "__main__":
    seed_data()