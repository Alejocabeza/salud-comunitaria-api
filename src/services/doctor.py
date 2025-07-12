from sqlmodel import Session, select
from ..models.doctors import Doctors, StoreDoctorRequest, UpdateDoctorRequest
from ..models.auth import Auth
from ..models.role import Roles, UserRole
from ..resource.doctor_resource import ResourceDoctor
from passlib.context import CryptContext
from fastapi import HTTPException
from ..utils.password_generator import generate_secure_password
from ..services.email.doctor_email_service import DoctoreEmailService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def index(db: Session):
    results = db.exec(select(Doctors).where(Doctors.deleted_at == None)).all()
    return [ResourceDoctor.from_array(record) for record in results]

def store(db: Session, data: StoreDoctorRequest):
    outpatient_center = Doctors.from_orm(data)
    if (db.exec(select(Doctors).where(Doctors.email == outpatient_center.email)).first()):
        raise HTTPException(status_code=400, detail="El doctor ya existe con este email")
    
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

    doctor_role = db.query(Roles).filter(Roles.name == "doctor").first()
    if doctor_role:
        user_role = UserRole(user_id=auth.id, role_id=doctor_role.id)
        db.add(user_role)
        db.commit()
    else:
        raise Exception("Rol 'doctor' no encontrado")

    # Send welcome email with credentials
    try:
        DoctoreEmailService.send_welcome_email(
            email=outpatient_center.email,
            name=outpatient_center.name,
            password=password
        )
    except Exception as e:
        print(f"Error sending email to {outpatient_center.email}: {str(e)}")
    
    return ResourceDoctor.from_array(outpatient_center)
    

def show(db: Session, id: int):
    record = db.exec(select(Doctors).where(Doctors.id == id)).first()
    if not record:
        return None
    return ResourceDoctor.from_array(record)

def update(db: Session, id: int, data: UpdateDoctorRequest):
    record = db.exec(select(Doctors).where(Doctors.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceDoctor.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(Doctors).where(Doctors.id == id)).first()
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

    db.commit() 

    return record