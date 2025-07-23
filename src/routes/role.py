from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..core.security import decode_access_token
from ..models.user import Role
from ..schemas.user import RoleRead, RoleCreate

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_access_token)]
)

@router.post("/", response_model=RoleRead)
def create_role(role: RoleCreate, session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    db_role = session.exec(select(Role).where(Role.name == role.name)).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = Role(name=role.name, description=role.description)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role

@router.get("/", response_model=list[RoleRead])
def list_roles(session: Session = Depends(get_session), current_user=Depends(require_role("admin"))):
    roles = session.exec(select(Role)).all()
    return roles