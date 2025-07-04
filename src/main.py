# main.py
from fastapi import FastAPI
from .routes import auth, outpatient_center
from .config.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url='/'
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(outpatient_center.router, prefix="/api/v1")
