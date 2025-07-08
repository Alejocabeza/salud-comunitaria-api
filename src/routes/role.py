from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..utils.jwt import decode_token
from ..config.database import get_session
from ..services.role import index, store, show, update, destroy
from ..resource.role_resource import ResourceRole
from ..models.role import StoreRoleRequest, UpdateRoleRequest

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_token)]
)

@router.get("/", response_model=List[ResourceRole], status_code=status.HTTP_200_OK)
def index_role(db: Session = Depends(get_session)):
    return index(db)

@router.post("/", response_model=ResourceRole, status_code=status.HTTP_201_CREATED)
def store_role(data: StoreRoleRequest, db: Session = Depends(get_session)):
    return store(db, data)

@router.get("/{id}", response_model=ResourceRole, status_code=status.HTTP_200_OK)
def get_role(id: int, db: Session = Depends(get_session)):
    result = show(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return result

@router.patch("/{id}", response_model=ResourceRole, status_code=status.HTTP_200_OK)
def patch_role(id: int, data: UpdateRoleRequest, db: Session = Depends(get_session)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id: int, db: Session = Depends(get_session)):
    result = destroy(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado correctamente (soft delete)"}
