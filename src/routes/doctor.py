from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.doctor import index, store, show, update, destroy
from ..resource.doctor_resource import ResourceDoctor
from ..models.doctors import StoreDoctorRequest, UpdateDoctorRequest

router = APIRouter(
    prefix="/doctors",
    tags=["Doctores / Medicos"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourceDoctor], status_code=status.HTTP_200_OK)
def index_doctor(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourceDoctor, status_code=status.HTTP_201_CREATED)
def store_doctor(data: StoreDoctorRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourceDoctor, status_code=status.HTTP_200_OK)
def get_doctor(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Centro de atención ambulatoria no encontrado")
    return result

@router.patch("/{id}", response_model=ResourceDoctor, status_code=status.HTTP_200_OK)
def patch_doctor(id: int, data: UpdateDoctorRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return {"message": "Doctor eliminado correctamente (soft delete)"}
