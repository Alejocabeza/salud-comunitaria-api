from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.patient import index, store, show, update, destroy
from ..resource.patient_resource import ResourcePatient
from ..models.patient import StorePatientRequest, UpdatePatientRequest

router = APIRouter(
    prefix="/patients",
    tags=["Pacientes"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourcePatient], status_code=status.HTTP_200_OK)
def index_patient(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourcePatient, status_code=status.HTTP_201_CREATED)
def store_patient(data: StorePatientRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourcePatient, status_code=status.HTTP_200_OK)
def get_patient(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return result

@router.patch("/{id}", response_model=ResourcePatient, status_code=status.HTTP_200_OK)
def patch_patient(id: int, data: UpdatePatientRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado correctamente (soft delete)"}
