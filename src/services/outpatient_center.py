from typing import List
from sqlmodel import Session, select
from ..models.outpatient_center import OutpatientCenter, OutpatientCenterCreate, OutpatientCenterUpdate
from ..models.auth import Auth
from ..models.role import Roles, UserRole
from ..resource.outpatient_center_resource import ResourceOutpatientCenter
from passlib.context import CryptContext
from ..utils.jwt import encode_token 
from ..config.settings import settings
from fastapi import HTTPException
from ..utils.password_generator import generate_secure_password
from ..services.email.outpatient_center_email_service import OutpatientCenterEmailService

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
    
    # Generate automatic password if not provided
    password = data.password if data.password else generate_secure_password()
    
    data_auth = {
        "name": outpatient_center.name,
        "email": outpatient_center.email,
        "password": pwd_context.hash(password),
    }
    auth = Auth.from_orm(data_auth)
    db.add(auth)
    db.commit()
    db.refresh(auth)

    outpatient_center_role = db.query(Roles).filter(Roles.name == "outpatient_center").first()
    if outpatient_center_role:
        user_role = UserRole(user_id=auth.id, role_id=outpatient_center_role.id)
        db.add(user_role)
        db.commit()
    else:
        raise Exception("Rol 'outpatient_center' no encontrado")

    # Send welcome email with credentials
    try:
        OutpatientCenterEmailService.send_welcome_email(
            email=outpatient_center.email,
            name=outpatient_center.name,
            password=password
        )
    except Exception as e:
        print(f"Error sending email to {outpatient_center.email}: {str(e)}")
    
    return ResourceOutpatientCenter.from_array(outpatient_center)
    

def show(db: Session, id: int):
    record = db.exec(select(OutpatientCenter).where(OutpatientCenter.id == id)).first()
    if not record:
        return None
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
    
    # Soft delete para OutpatientCenter
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)

    # Hard delete para Auth
    auth_record = db.exec(select(Auth).where(Auth.email == record.email)).first()
    if auth_record:
        db.delete(auth_record)

    db.commit() # Un solo commit para todas las operaciones

    return record


