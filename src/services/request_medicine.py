from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from ..models.auth import Auth
from ..models.request_medicines import RequestMedicine, StoreRequestMedicineRequest, UpdateRequestMedicineRequest
from ..resource.request_medicine import ResourceRequestMedicine
from passlib.context import CryptContext
from fastapi import HTTPException
from ..templates.email.notifications.request_medicine_notification import RequestMedicineNotification

def index(db: Session):
    results = db.exec(select(RequestMedicine).where(RequestMedicine.deleted_at == None)).all()
    return [ResourceRequestMedicine.from_array(record) for record in results]

def store(db: Session, data: StoreRequestMedicineRequest):
    requestMedicine = RequestMedicine.from_orm(data)
    if (db.exec(select(RequestMedicine).options().where(RequestMedicine.name == requestMedicine.name)).first()):
        raise HTTPException(status_code=400, detail="La solicitud ya ha sido enviada")

    db.add(requestMedicine)
    db.commit()
    db.refresh(requestMedicine)


    try:
        auth = db.exec(
            select(Auth)
            .options(selectinload(Auth.roles))
            .where(Auth.id == requestMedicine.auth_id)
        ).first()
        print(f"Auth record found: {auth}")
        if auth and hasattr(auth, "roles") and auth.roles:
            role_names = [role.name for role in auth.roles]
            user_type = "patient" if "patient" in role_names else "doctor" if "doctor" in role_names else "unknown"
            RequestMedicineNotification.send_request_medicine_email(
                email=auth.email,
                name=auth.name,
                medicine=requestMedicine.name,
                quantity=requestMedicine.quantity,
                type=user_type
            )
            print(f"Correo enviado a {auth.email} para la solicitud de medicamento {requestMedicine.name}.")
        else:
            print(f"No se encontró el usuario con ID {requestMedicine.auth_id} o no tiene roles para enviar el correo.")
    except Exception as e:
        print(f"Error sending email for request medicine {requestMedicine.name}: {str(e)}")

    return ResourceRequestMedicine.from_array(requestMedicine)

def show(db: Session, id: int):
    record = db.exec(select(RequestMedicine).where(RequestMedicine.id == id)).first()
    if not record:
        return None
    return ResourceRequestMedicine.from_array(record)

def update(db: Session, id: int, data:  UpdateRequestMedicineRequest):
    record = db.exec(select(RequestMedicine).where(RequestMedicine.id == id)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Solicitud de medicamento no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceRequestMedicine.from_array(record)

def destroy(db: Session, id: int):
    record = db.exec(select(RequestMedicine).where(RequestMedicine.id == id)).first()
    if not record:
        return None
    # Soft delete: marcar la fecha de borrado
    from datetime import datetime
    record.deleted_at = datetime.now().isoformat()
    db.add(record)
    db.commit()
    db.refresh(record)
    return ResourceRequestMedicine.from_array(record)