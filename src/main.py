# main.py
from fastapi import FastAPI
from .routes import auth, outpatient_center, doctor, patient,role,permission, resource
from .config.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    redoc_url='/'
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(outpatient_center.router, prefix="/api/v1")
app.include_router(doctor.router, prefix="/api/v1")
app.include_router(patient.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(permission.router, prefix="/api/v1")
app.include_router(resource.router, prefix="/api/v1")
