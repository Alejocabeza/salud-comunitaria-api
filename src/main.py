# main.py
from fastapi import FastAPI
from .routes import (
    user, 
    auth, 
    role, 
    user_roles, 
    permission, 
    role_permissions, 
    outpatient_center, 
    doctor, 
    patient, 
    medical_resource, 
    medication_request, 
    external_document
)
from .core.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url='/'
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(user_roles.router, prefix="/api/v1")
app.include_router(permission.router, prefix="/api/v1")
app.include_router(role_permissions.router, prefix="/api/v1")
app.include_router(outpatient_center.router, prefix="/api/v1")
app.include_router(doctor.router, prefix="/api/v1")
app.include_router(patient.router, prefix="/api/v1")
app.include_router(medical_resource.router, prefix="/api/v1")
app.include_router(medication_request.router, prefix="/api/v1")
app.include_router(external_document.router, prefix="/api/v1")

