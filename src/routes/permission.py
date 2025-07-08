from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.permission import index, store, show, update, destroy
from ..resource.permission_resource import ResourcePermission
from ..models.permission import StorePermissionRequest, UpdatePermissionRequest

router = APIRouter(
    prefix="/permissions",
    tags=["Permisos"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourcePermission], status_code=status.HTTP_200_OK)
def index_permission(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourcePermission, status_code=status.HTTP_201_CREATED)
def store_permission(data: StorePermissionRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourcePermission, status_code=status.HTTP_200_OK)
def get_permission(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return result

@router.patch("/{id}", response_model=ResourcePermission, status_code=status.HTTP_200_OK)
def patch_permission(id: int, data: UpdatePermissionRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return {"message": "Permiso eliminado correctamente (soft delete)"}
