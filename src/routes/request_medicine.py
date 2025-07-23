from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.request_medicine import index, store, show, update, destroy
from ..resource.request_medicine import ResourceRequestMedicine
from ..models.request_medicines import StoreRequestMedicineRequest, UpdateRequestMedicineRequest 

router = APIRouter(
    prefix="/request_medicines",
    tags=["Solicitudes de Medicamentos"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourceRequestMedicine], status_code=status.HTTP_200_OK)
def index_permission(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourceRequestMedicine, status_code=status.HTTP_201_CREATED)
def store_request_medicine(data: StoreRequestMedicineRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourceRequestMedicine, status_code=status.HTTP_200_OK)
def get_request_medicine(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Solicitud de medicamento no encontrada")
    return result

@router.patch("/{id}", response_model=ResourceRequestMedicine, status_code=status.HTTP_200_OK)
def patch_permission(id: int, data: UpdateRequestMedicineRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Solicitud de medicamento no encontrada")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Solicitud de medicamento no encontrada")
    return {"message": "Solicitud de medicamento eliminada correctamente (soft delete)"}
