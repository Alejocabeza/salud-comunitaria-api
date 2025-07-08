from sqlmodel import Session, select
from ..models.role import Roles, StoreRoleRequest, UpdateRoleRequest 
from ..models.auth import Auth
from ..resource.role_resource import ResourceRole
from passlib.context import CryptContext
from fastapi import HTTPException
from ..utils.password_generator import generate_secure_password
from ..services.email.patient_email_service import PatientEmailService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def index(db: Session):
    results = db.exec(select(Roles).where(Roles.deleted_at == None)).all()
    return [ResourceRole.from_array(record) for record in results]

def store(db: Session, data: StoreRoleRequest):
    role = Roles.from_orm(data)
    if (db.exec(select(Roles).where(Roles.name == role.name)).first()):
        raise HTTPException(status_code=400, detail="El rol ya existe con este nombre")

    db.add(role)
    db.commit()
    db.refresh(role)


def show(db: Session, id: int):
    record = db.exec(select(Roles).where(Roles.id == id)).first()
    if not record:
        return None
    return ResourceRole.from_array(record)

def update(db: Session, id: int, data:  UpdateRoleRequest):
    record = db.exec(select(Roles).where(Roles.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceRole.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(Roles).where(Roles.id == id)).first()
    if not record:
        return None
    # Soft delete: marcar la fecha de borrado
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceRole.from_array(record)