import sys
import os

# Añade el directorio raíz al sys.path para poder importar módulos de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(1, project_root)

from sqlmodel import Session
from src.config.database import engine
from seeders.role import seed_data as seed_roles
from seeders.permission import seed_data as seed_permissions
from seeders.auth_role import seed_data as seed_auth_roles
from seeders.role_permission import seed_data as seed_role_permissions
from seeders.auth import seed_data as seed_auth

def seed_all():
    print("Starting to seed all data...")
    with Session(engine) as session:
        print('seeding Auths...')
        seed_auth()
        print("Seeding roles...")
        seed_roles()
        print("Seeding permissions...")
        seed_permissions()
        print("Seeding role-permission relationships...")
        seed_role_permissions()
        print("Seeding auth-role relationships...")
        seed_auth_roles()
    print("All data seeding finished.")

if __name__ == "__main__":
    seed_all()