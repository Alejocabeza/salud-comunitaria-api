from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.resource import index, store, show, update, destroy
from ..resource.resources_resource import ResourceResources
from ..models.resource import StoreResourceRequest, UpdateResourceRequest

router = APIRouter(
    prefix="/resources",
    tags=["Recursos Medicos"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourceResources], status_code=status.HTTP_200_OK)
def index_resource(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourceResources, status_code=status.HTTP_201_CREATED)
def store_resource(data: StoreResourceRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourceResources, status_code=status.HTTP_200_OK)
def get_resource(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return result

@router.patch("/{id}", response_model=ResourceResources, status_code=status.HTTP_200_OK)
def patch_resource(id: int, data: UpdateResourceRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return {"message": "Recurso eliminado correctamente (soft delete)"}
