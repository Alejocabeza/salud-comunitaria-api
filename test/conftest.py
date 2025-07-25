import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
import subprocess
import tempfile
from alembic.config import Config
from alembic import command

# Agrega la carpeta src al sys.path para importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all models to ensure they are registered with SQLModel before creating tables.
from src.models.user import User
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.medication_request import MedicationRequest
from src.models.medical_resource import MedicalResource
from src.models.outpatient_center import OutpatientCenter
from src.models.external_document import ExternalDocument
from src.models.role import Role
from src.models.permission import Permission
from src.models.user_role import UserRole
from src.models.role_permission import RolePermission

import src.core.database as database_module
from src.core.database import get_session

@pytest.fixture(name="engine")
def engine_fixture():
    # Create a temporary file for the SQLite database
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        test_database_url = f"sqlite:///{tmp_file.name}"

    os.environ["DATABASE_URL"] = test_database_url

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    test_database_url = f"sqlite:///{tmp_file.name}"
    tmp_file.close()

    os.environ["DATABASE_URL"] = test_database_url

    temp_engine = create_engine(
        test_database_url,
        connect_args={"check_same_thread": False}
    )
    # Create tables directly for testing
    SQLModel.metadata.create_all(temp_engine)

    temp_engine = create_engine(
        test_database_url,
        connect_args={"check_same_thread": False}
    )
    yield temp_engine

    # Clean up after tests
    temp_engine.dispose()
    os.remove(tmp_file.name)
    del os.environ["DATABASE_URL"]

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session, engine):
    from src.main import app
    app.dependency_overrides[get_session] = lambda: session
    # Set the global engine for the app to the test engine
    database_module.set_engine(engine)
    client = TestClient(app)
    yield client
    # Clear overrides and reset the global engine after tests
    app.dependency_overrides.clear()
    database_module.set_engine(None)
