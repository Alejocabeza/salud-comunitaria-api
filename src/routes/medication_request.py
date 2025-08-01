from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import get_current_user, require_role
from ..models.outpatient_center import OutpatientCenter
from ..models.medication_request import MedicationRequest
from ..models.doctor import Doctor
from ..models.patient import Patient
from ..schemas.medication_request import (
    MedicationRequestCreate, MedicationRequestRead, MedicationRequestUpdate
)
from src.templates.notifications.medication_request import medication_request
from datetime import datetime

router = APIRouter(
    prefix="/medication_request",
    tags=["Solicitudes de Medicamentos"],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/", response_model=MedicationRequestRead)
async def create_medication_request(
    request: MedicationRequestCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    # Solo pueden crear solicitudes los roles doctor y patient
    allowed_roles = {"doctor", "patient"}
    user_roles = {role.name for role in current_user.roles}
    if not user_roles.intersection(allowed_roles):
        raise HTTPException(status_code=403, detail="No tienes permiso para solicitar medicamentos.")

    db_request = MedicationRequest(
        medication_name=request.medication_name,
        quantity=request.quantity,
        reason=request.reason,
        status="pending",
        requested_by_user_id=current_user.id,
        outpatient_center_id=request.outpatient_center_id,
        created_at=datetime.utcnow()
    )
    session.add(db_request)
    session.commit()
    session.refresh(db_request)

    # Obtener información del centro ambulatorio
    outpatient_center = session.get(OutpatientCenter, request.outpatient_center_id)
    if not outpatient_center:
        print(f"Error: Centro ambulatorio con ID {request.outpatient_center_id} no encontrado")
        return db_request

    if not outpatient_center.email:
        print(f"Advertencia: Centro ambulatorio '{outpatient_center.name}' no tiene email configurado")
        return db_request

    # Determinar el tipo de solicitante y obtener su nombre
    requester_name = current_user.username
    requester_type = "Usuario"

    if "doctor" in user_roles:
        doctor = session.exec(select(Doctor).where(Doctor.user_id == current_user.id)).first()
        if doctor:
            requester_name = doctor.name
            requester_type = "Doctor"
    elif "patient" in user_roles:
        patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
        if patient:
            requester_name = patient.name
            requester_type = "Paciente"

    # Enviar notificación por correo al centro ambulatorio
    try:
        print(f"Intentando enviar correo a: {outpatient_center.email}")
        print(f"Solicitante: {requester_name} ({requester_type})")
        print(f"Medicamento: {request.medication_name}")

        await medication_request(
            email_to=outpatient_center.email,
            center_name=outpatient_center.name,
            requester_name=requester_name,
            requester_type=requester_type,
            medication_name=request.medication_name,
            quantity=request.quantity,
            reason=request.reason
        )
        print("Correo enviado exitosamente")
    except Exception as e:
        # Log del error pero no fallar la creación de la solicitud
        print(f"Error enviando notificación de solicitud de medicamento: {e}")
        import traceback
        traceback.print_exc()

    return db_request

# READ ALL (solo para el ambulatorio)
@router.get("/", response_model=list[MedicationRequestRead])
def list_medication_requests(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    # El ambulatorio ve todas, el doctor/paciente solo las suyas
    user_roles = {role.name for role in current_user.roles}
    if "outpatient_center" in user_roles:
        outpatient_center = session.exec(select(OutpatientCenter).where(OutpatientCenter.user_id == current_user.id)).first()
        if not outpatient_center:
            raise HTTPException(status_code=404, detail="Centro ambulatorio no encontrado para el usuario actual")
        requests = session.exec(select(MedicationRequest).where(
            MedicationRequest.outpatient_center_id == outpatient_center.id
        )).all()
    else:
        requests = session.exec(select(MedicationRequest).where(
            MedicationRequest.requested_by_user_id == current_user.id
        )).all()
    return requests

# READ ONE
@router.get("/{request_id}", response_model=MedicationRequestRead)
def get_medication_request(
    request_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    req = session.get(MedicationRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    user_roles = {role.name for role in current_user.roles}
    if "outpatient_center" in user_roles:
        outpatient_center = session.exec(select(OutpatientCenter).where(OutpatientCenter.user_id == current_user.id)).first()
        if not outpatient_center or req.outpatient_center_id != outpatient_center.id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta solicitud")
    elif req.requested_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta solicitud")
    return req

# UPDATE (solo el ambulatorio puede cambiar el estado)
@router.patch("/{request_id}", response_model=MedicationRequestRead)
def update_medication_request(
    request_id: int,
    update: MedicationRequestUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    req = session.get(MedicationRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(req, key, value)
    req.updated_at = datetime.utcnow()
    session.add(req)
    session.commit()
    session.refresh(req)
    return req

# DELETE (opcional, solo el ambulatorio puede borrar)
@router.delete("/{request_id}")
def delete_medication_request(
    request_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    req = session.get(MedicationRequest, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    session.delete(req)
    session.commit()
    return {"msg": "Solicitud de medicamento eliminada"}