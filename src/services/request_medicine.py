from sqlmodel import Session, select
from ..models.request_medicines import RequestMedicine, StoreRequestMedicineRequest, UpdateRequestMedicineRequest
from ..resource.request_medicine import ResourceRequestMedicine
from passlib.context import CryptContext
from fastapi import HTTPException

def store(db: Session, data: StoreRequestMedicineRequest):
    requestMedicine = RequestMedicine.from_orm(data)
    if (db.exec(select(RequestMedicine).where(RequestMedicine.name == requestMedicine.name)).first()):
        raise HTTPException(status_code=400, detail="La solicitud ya ha sido enviada")

    db.add(requestMedicine)
    db.commit()
    db.refresh(requestMedicine)

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