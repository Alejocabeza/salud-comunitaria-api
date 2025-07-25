import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, project_root)

from sqlmodel import Session
from src.core.database import get_engine
from seeders.user import seed_data as seed_user
from seeders.role import seed_data as seed_role
from seeders.permission import seed_data as seed_permission
from seeders.role_permission import seed_data as seed_role_permission
from seeders.auth_role import seed_data as seed_auth_role

def seed_all():
    print("Starting to seed all data...")
    with Session(get_engine()) as session:
        print('seeding Users...')
        seed_user()
        print('seeding Roles...')
        seed_role()
        print('seeding Permissions...')
        seed_permission()
        print('seeding Role-Permissions...')
        seed_role_permission()
        print('seeding Auth-Roles...')
        seed_auth_role()
    print("All data seeding finished.")

if __name__ == "__main__":
    seed_all()