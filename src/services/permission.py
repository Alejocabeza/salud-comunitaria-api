from sqlmodel import Session, select
from ..models.permission import Permission, StorePermissionRequest, UpdatePermissionRequest 
from ..models.auth import Auth
from ..resource.permission_resource import ResourcePermission
from passlib.context import CryptContext
from fastapi import HTTPException
from ..utils.password_generator import generate_secure_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def index(db: Session):
    results = db.exec(select(Permission).where(Permission.deleted_at == None)).all()
    return [ResourcePermission.from_array(record) for record in results]

def store(db: Session, data: StorePermissionRequest):
    permission = Permission.from_orm(data)
    if (db.exec(select(Permission).where(Permission.name == permission.name)).first()):
        raise HTTPException(status_code=400, detail="El permiso ya existe con este nombre")

    db.add(permission)
    db.commit()
    db.refresh(permission)

def show(db: Session, id: int):
    record = db.exec(select(Permission).where(Permission.id == id)).first()
    if not record:
        return None
    return ResourcePermission.from_array(record)

def update(db: Session, id: int, data:  UpdatePermissionRequest):
    record = db.exec(select(Permission).where(Permission.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourcePermission.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(Permission).where(Permission.id == id)).first()
    if not record:
        return None
    # Soft delete: marcar la fecha de borrado
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourcePermission.from_array(record)