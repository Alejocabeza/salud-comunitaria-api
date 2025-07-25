from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionRead

router = APIRouter(
    prefix="/permissions",
    tags=["Permisos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=PermissionRead)
def create_permission(permission: PermissionCreate, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    db_permission = session.exec(select(Permission).where(Permission.name == permission.name)).first()
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")
    new_permission = Permission(name=permission.name, description=permission.description)
    session.add(new_permission)
    session.commit()
    session.refresh(new_permission)
    return new_permission

@router.get("/", response_model=list[PermissionRead])
def list_permissions(session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    return session.exec(select(Permission)).all()