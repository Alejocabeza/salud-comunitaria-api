from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.doctor import Doctor
from ..models.user import User, Role, UserRoleLink
from ..schemas.doctor import (
    DoctorCreate, DoctorRead, DoctorUserRead, DoctorUpdate, DoctorReadResource
)
from ..core.security import get_password_hash

router = APIRouter(
    prefix="/doctors",
    tags=["Medicos y Doctores"],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/", response_model=DoctorRead)
def create_doctor(
    doctor: DoctorCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    role = session.exec(select(Role).where(Role.name == "doctor")).first()
    if not role:
        role = Role(name="doctor", description="Doctor")
        session.add(role)
        session.commit()
        session.refresh(role)

    username = doctor.user.username
    if session.exec(select(User).where(User.username == username)).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    if session.exec(select(User).where(User.email == doctor.user.email)).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(doctor.user.password)
    user = User(
        username=username,
        email=doctor.user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user_role_link = UserRoleLink(user_id=user.id, role_id=role.id)
    session.add(user_role_link)
    session.commit()

    db_doctor = Doctor(
        name=doctor.name,
        specialty=doctor.specialty,
        phone=doctor.phone,
        email=doctor.email,
        outpatient_center_id=doctor.outpatient_center_id,
        user_id=user.id
    )
    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)

    return DoctorRead(
        **db_doctor.dict(),
        user=DoctorUserRead.model_validate(user, from_attributes=True)
    )

# READ ALL
@router.get("/", response_model=list[DoctorReadResource])
def list_doctors(
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    doctors = session.exec(select(Doctor)).all()
    result = []
    for doctor in doctors:
        user = session.get(User, doctor.user_id)
        result.append(
            DoctorRead(
                **doctor.dict(),
                user=DoctorUserRead.model_validate(user, from_attributes=True)
            )
        )
    return result

# READ ONE
@router.get("/{doctor_id}", response_model=DoctorReadResource)
def get_doctor(
    doctor_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    user = session.get(User, doctor.user_id)
    return DoctorRead(
        **doctor.dict(),
        user=DoctorUserRead.model_validate(user, from_attributes=True)
    )

# UPDATE
@router.patch("/{doctor_id}", response_model=DoctorReadResource)
def update_doctor(
    doctor_id: int,
    doctor_update: DoctorUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    for key, value in doctor_update.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    user = session.get(User, doctor.user_id)
    return DoctorRead(
        **doctor.dict(),
        user=DoctorUserRead.model_validate(user, from_attributes=True)
    )

# DELETE
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    user = session.get(User, doctor.user_id)
    session.delete(doctor)
    session.commit()
    if user:
        session.delete(user)
        session.commit()
    return {"msg": "Doctor y usuario asociado eliminados"}