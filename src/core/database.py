from sqlmodel import create_engine, SQLModel, Session
from .settings import settings

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(settings.DATABASE_URL, echo=True)
    return _engine

def set_engine(new_engine):
    global _engine
    _engine = new_engine

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    with Session(get_engine()) as session:
        yield session
