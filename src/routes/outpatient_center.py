from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.outpatient_center import index, store, show, update, destroy
from ..resource.outpatient_center_resource import ResourceOutpatientCenter
from ..models.outpatient_center import OutpatientCenterCreate, OutpatientCenterUpdate

router = APIRouter(
    prefix="/outpatient_center",
    tags=["Centro de Atención Ambulatoria"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)
 
@router.get("/", response_model=List[ResourceOutpatientCenter], status_code=status.HTTP_200_OK)
def index_outpatient_center(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourceOutpatientCenter, status_code=status.HTTP_201_CREATED)
def store_outpatient_center(data: OutpatientCenterCreate, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourceOutpatientCenter, status_code=status.HTTP_200_OK)
def get_outpatient_center(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Centro de atención ambulatoria no encontrado")
    return result

@router.patch("/{id}", response_model=ResourceOutpatientCenter, status_code=status.HTTP_200_OK)
def patch_outpatient_center(id: int, data: OutpatientCenterUpdate, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Centro de atención ambulatoria no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_outpatient_center(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Centro de atención ambulatoria no encontrado")
    return {"message": "Centro de atención ambulatoria eliminado correctamente (soft delete)"}
