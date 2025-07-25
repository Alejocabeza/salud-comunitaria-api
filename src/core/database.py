from sqlmodel import create_engine, SQLModel, Session
from .settings import settings

_engine = None  # Cambia a None para inicializar correctamente

def init_engine():
    global _engine
    if _engine is None or isinstance(_engine, str):
        _engine = create_engine(settings.DATABASE_URL, echo=True)

def get_engine():
    global _engine
    init_engine()
    return _engine

def set_engine(new_engine):
    global _engine
    _engine = new_engine

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    with Session(get_engine()) as session:
        yield session
