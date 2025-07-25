from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.outpatient_center import OutpatientCenter
from ..models.user import User
from ..models.role import Role
from ..models.user_role import UserRole
from ..core.security import get_password_hash, generate_secure_password
from ..schemas.outpatient_center import (
    OutpatientCenterCreate,
    OutpatientCenterRead,
    OutpatientCenterUpdate,
    OutpatientCenterUserRead,
    OutpatientCenterReadOne
)

router = APIRouter(
    prefix="/outpatient_center",
    tags=["Centro de Atención Ambulatoria"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=OutpatientCenterRead)
def create_centro_ambulatorio(
    centro: OutpatientCenterCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("admin"))
):
    role = session.exec(select(Role).where(Role.name == "outpatient_center")).first()
    if not role:
        role = Role(name="outpatient_center", description="Centro ambulatorio")
        session.add(role)
        session.commit()
        session.refresh(role)

    password = get_password_hash(generate_secure_password())

    data_user = {
        'username': centro.name.lower().replace(" ", "_"),
        'email': centro.email,
        'hashed_password': password,
        'is_active': True
    }
    user = User.from_orm(data_user)
    session.add(user)
    session.commit()
    session.refresh(user)

    user_role_link = UserRole(user_id=user.id, role_id=role.id)
    session.add(user_role_link)
    session.commit()

    db_centro = OutpatientCenter(
        name=centro.name,
        address=centro.address,
        phone=centro.phone,
        email=centro.email,
        responsible=centro.responsible,
        user_id=user.id
    )
    session.add(db_centro)
    session.commit()
    session.refresh(db_centro)

    return OutpatientCenterRead(
        **db_centro.dict(),
        user=OutpatientCenterUserRead.model_validate(user, from_attributes=True)
    )

@router.get("/", response_model=list[OutpatientCenterReadOne])
def list_outpatient_centers(
    session: Session = Depends(get_session),
    current_user=Depends(require_role("admin"))
):
    return session.exec(select(OutpatientCenter)).all()

@router.get("/{centro_id}", response_model=OutpatientCenterReadOne)
def get_outpatient_center(
    centro_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("admin"))
):
    centro = session.get(OutpatientCenter, centro_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro ambulatorio no encontrado")
    return centro

@router.patch("/{centro_id}", response_model=OutpatientCenterRead)
def update_outpatient_center(
    centro_id: int,
    centro_update: OutpatientCenterUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("admin"))
):
    centro = session.get(OutpatientCenter, centro_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro ambulatorio no encontrado")
    for key, value in centro_update.model_dump(exclude_unset=True).items():
        setattr(centro, key, value)
    session.add(centro)
    session.commit()
    session.refresh(centro)
    return centro

@router.delete("/{centro_id}")
def delete_outpatient_center(
    centro_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("admin"))
):
    centro = session.get(OutpatientCenter, centro_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro ambulatorio no encontrado")
    
    user = session.exec(select(User).where(User.email == centro.email)).first()
    
    session.delete(centro)
    session.commit()
    
    if user:
        session.delete(user)
        session.commit()
    
    return {"msg": "Centro ambulatorio y usuario asociado eliminados"}