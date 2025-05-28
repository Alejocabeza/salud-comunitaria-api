# main.py
from fastapi import FastAPI
from .config.database import create_db_and_tables, engine
from .routes import auth
from .config.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    redoc_url='/'
)

app.include_router(auth.router, prefix="/api/v1")