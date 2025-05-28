from typing import List
from sqlmodel import Session, select
from ..models.outpatient_center import OutpatientCenter, OutpatientCenterCreate, OutpatientCenterUpdate
from ..models.auth import Auth
from ..resource.outpatient_center_resource import ResourceOutpatientCenter
from passlib.context import CryptContext
from ..utils.jwt import encode_token 
from ..config.settings import settings
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def index(db: Session):
    results = db.exec(select(OutpatientCenter).where(OutpatientCenter.deleted_at == None)).all()
    return [ResourceOutpatientCenter.from_array(record) for record in results]

def store(db: Session, data: OutpatientCenterCreate):
    outpatient_center = OutpatientCenter.from_orm(data)
    if (db.exec(select(OutpatientCenter).where(OutpatientCenter.email == outpatient_center.email)).first()):
        raise HTTPException(status_code=400, detail="El centro de atención ambulatoria ya existe con este email")
    db.add(outpatient_center)
    db.commit()
    db.refresh(outpatient_center)
    data_auth = {
        "name": outpatient_center.name,
        "email": outpatient_center.email,
        "password": pwd_context.hash(data.password),  # Usar el password del DTO de entrada
    }
    auth = Auth.from_orm(data_auth)
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return ResourceOutpatientCenter.from_array(outpatient_center)
    

def show(db: Session, id: int):
    record = db.exec(select(OutpatientCenter).where(OutpatientCenter.id == id)).first()
    return ResourceOutpatientCenter.from_array(record)

def update(db: Session, id: int, data: OutpatientCenterUpdate):
    record = db.exec(select(OutpatientCenter).where(OutpatientCenter.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Centro de atención ambulatoria no encontrado")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceOutpatientCenter.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(OutpatientCenter).where(OutpatientCenter.id == id)).first()
    if not record:
        return None
    # Soft delete: marcar la fecha de borrado
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


