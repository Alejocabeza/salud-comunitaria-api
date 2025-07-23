from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.user import Role
from ..models.user import Permission, RolePermissionLink

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
    link = session.exec(select(RolePermissionLink).where(
        (RolePermissionLink.role_id == role_id) & (RolePermissionLink.permission_id == permission_id)
    )).first()
    if link:
        raise HTTPException(status_code=400, detail="Permission already assigned to role")
    new_link = RolePermissionLink(role_id=role_id, permission_id=permission_id)
    session.add(new_link)
    session.commit()
    return {"msg": f"Permission '{permission.name}' assigned to role '{role.name}'"}

@router.post("/remove")
def remove_permission_from_role(role_id: int, permission_id: int, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    link = session.exec(select(RolePermissionLink).where(
        (RolePermissionLink.role_id == role_id) & (RolePermissionLink.permission_id == permission_id)
    )).first()
    if not link:
        raise HTTPException(status_code=404, detail="Permission not assigned to role")
    session.delete(link)
    session.commit()
    return {"msg": "Permission removed from role"}