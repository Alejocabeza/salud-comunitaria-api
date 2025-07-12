from sqlmodel import Session, select
from ..models.resource import Resource, StoreResourceRequest, UpdateResourceRequest
from ..models.auth import Auth
from ..resource.resources_resource import ResourceResources
from passlib.context import CryptContext
from fastapi import HTTPException
from ..utils.password_generator import generate_secure_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def index(db: Session):
    results = db.exec(select(Resource).where(Resource.deleted_at == None)).all()
    return [ResourceResources.from_array(record) for record in results]

def store(db: Session, data: StoreResourceRequest):
    resource = Resource.from_orm(data)
    if (db.exec(select(Resource).where(Resource.name == resource.name)).first()):
        raise HTTPException(status_code=400, detail="El recurso ya existe con este nombre")

    db.add(resource)
    db.commit()
    db.refresh(resource)

def show(db: Session, id: int):
    record = db.exec(select(Resource).where(Resource.id == id)).first()
    if not record:
        return None
    return ResourceResources.from_array(record)

def update(db: Session, id: int, data:  UpdateResourceRequest):
    record = db.exec(select(Resource).where(Resource.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceResources.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(Resource).where(Resource.id == id)).first()
    if not record:
        return None
    # Soft delete: marcar la fecha de borrado
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceResources.from_array(record)