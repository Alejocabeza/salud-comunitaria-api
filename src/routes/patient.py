from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.patient import Patient
from ..models.user import User
from ..models.role import Role
from ..models.user_role import UserRole
from ..schemas.patient import (
    PatientCreate, PatientRead, PatientUserRead, PatientUpdate, PatientReadResource
)
from ..core.security import get_password_hash

router = APIRouter(
    prefix="/patients",
    tags=["Pacientes"],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/", response_model=PatientRead)
def create_patient(
    patient: PatientCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    role = session.exec(select(Role).where(Role.name == "patient")).first()
    if not role:
        role = Role(name="patient", description="Paciente")
        session.add(role)
        session.commit()
        session.refresh(role)

    username = patient.user.username
    if session.exec(select(User).where(User.username == username)).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    if session.exec(select(User).where(User.email == patient.user.email)).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(patient.user.password)
    user = User(
        username=username,
        email=patient.user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user_role = UserRole(user_id=user.id, role_id=role.id)
    session.add(user_role)
    session.commit()

    db_patient = Patient(
        name=patient.name,
        birthdate=patient.birthdate,
        phone=patient.phone,
        email=patient.email,
        outpatient_center_id=patient.outpatient_center_id,
        user_id=user.id
    )
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return PatientRead(
        **db_patient.dict(),
        user=PatientUserRead.model_validate(user, from_attributes=True)
    )

# READ ALL
@router.get("/", response_model=list[PatientReadResource])
def list_patients(
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    patients = session.exec(select(Patient)).all()
    return [
        PatientRead(
            **patient.model_dump(),
            user=PatientUserRead.model_validate(session.get(User, patient.user_id), from_attributes=True)
        )
        for patient in patients
    ]

# READ ONE
@router.get("/{patient_id}", response_model=PatientReadResource)
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    user = session.get(User, patient.user_id)
    return PatientRead(
        **patient.dict(),
        user=PatientUserRead.model_validate(user, from_attributes=True)
    )

# UPDATE
@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for key, value in patient_update.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    session.add(patient)
    session.commit()
    session.refresh(patient)
    user = session.get(User, patient.user_id)
    return PatientRead(
        **patient.model_dump(),
        user=PatientUserRead.model_validate(user, from_attributes=True)
    )

# DELETE
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    user = session.get(User, patient.user_id)
    session.delete(patient)
    session.commit()
    if user:
        session.delete(user)
        session.commit()
    return {"msg": "Paciente y usuario asociado eliminados"}