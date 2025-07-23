from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.user import User, Role, UserRoleLink

router = APIRouter(
    prefix="/user_roles",
    tags=["Usuario Roles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/assign")
def assign_role_to_user(user_id: int, role_id: int, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    user = session.get(User, user_id)
    role = session.get(Role, role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    link = session.exec(select(UserRoleLink).where(
        (UserRoleLink.user_id == user_id) & (UserRoleLink.role_id == role_id)
    )).first()
    if link:
        raise HTTPException(status_code=400, detail="Role already assigned to user")
    new_link = UserRoleLink(user_id=user_id, role_id=role_id)
    session.add(new_link)
    session.commit()
    return {"msg": f"Role '{role.name}' assigned to user '{user.username}'"}

@router.post("/remove")
def remove_role_from_user(user_id: int, role_id: int, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    link = session.exec(select(UserRoleLink).where(
        (UserRoleLink.user_id == user_id) & (UserRoleLink.role_id == role_id)
    )).first()
    if not link:
        raise HTTPException(status_code=404, detail="Role not assigned to user")
    session.delete(link)
    session.commit()
    return {"msg": "Role removed from user"}