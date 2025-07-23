from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import require_role
from ..models.medical_resource import MedicalResource
from ..schemas.medical_resource import (
    MedicalResourceCreate, MedicalResourceRead, MedicalResourceUpdate
)

router = APIRouter(
    prefix="/medical_resource",
    tags=["Recursos Médicos"],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/", response_model=MedicalResourceRead)
def create_medical_resource(
    resource: MedicalResourceCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    db_resource = MedicalResource.from_orm(resource)
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource

# READ ALL
@router.get("/", response_model=list[MedicalResourceRead])
def list_medical_resources(
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    resources = session.exec(select(MedicalResource)).all()
    return resources

# READ ONE
@router.get("/{resource_id}", response_model=MedicalResourceRead)
def get_medical_resource(
    resource_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    resource = session.get(MedicalResource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso médico no encontrado")
    return resource

# UPDATE
@router.patch("/{resource_id}", response_model=MedicalResourceRead)
def update_medical_resource(
    resource_id: int,
    resource_update: MedicalResourceUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    resource = session.get(MedicalResource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso médico no encontrado")
    for key, value in resource_update.dict(exclude_unset=True).items():
        setattr(resource, key, value)
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource

# DELETE
@router.delete("/{resource_id}")
def delete_medical_resource(
    resource_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(require_role("outpatient_center"))
):
    resource = session.get(MedicalResource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso médico no encontrado")
    session.delete(resource)
    session.commit()
    return {"msg": "Recurso médico eliminado"}