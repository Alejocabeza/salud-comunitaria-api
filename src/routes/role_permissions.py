from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.role import Role
from ..models.permission import Permission
from ..models.role_permission import RolePermission

router = APIRouter(
    prefix="/role_permissions",
    tags=["Role Permisos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/assign")
def assign_permission_to_role(role_id: int, permission_id: int, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    role = session.get(Role, role_id)
    permission = session.get(Permission, permission_id)
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    link = session.exec(select(RolePermission).where(
        (RolePermission.role_id == role_id) & (RolePermission.permission_id == permission_id)
    )).first()
    if link:
        raise HTTPException(status_code=400, detail="Permission already assigned to role")
    new_link = RolePermission(role_id=role_id, permission_id=permission_id)
    session.add(new_link)
    session.commit()
    return {"msg": f"Permission '{permission.name}' assigned to role '{role.name}'"}

@router.post("/remove")
def remove_permission_from_role(role_id: int, permission_id: int, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    link = session.exec(select(RolePermission).where(
        (RolePermission.role_id == role_id) & (RolePermission.permission_id == permission_id)
    )).first()
    if not link:
        raise HTTPException(status_code=404, detail="Permission not assigned to role")
    session.delete(link)
    session.commit()
    return {"msg": "Permission removed from role"}