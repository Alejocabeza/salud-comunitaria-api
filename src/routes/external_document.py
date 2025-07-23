import os
import base64
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.dependencies import get_current_user
from ..models.external_document import ExternalDocument
from ..schemas.external_document import ExternalDocumentCreate, ExternalDocumentRead
from ..utils.action.base64_action import allowed_file
from ..core.settings import settings
from datetime import datetime

router = APIRouter(
    prefix="/external_document",
    tags=["Documentos Externos"],
    responses={404: {"description": "Not found"}},
)

UPLOAD_DIR = "public/uploads/external_documents/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CREATE (subida de archivo)
@router.post("/", response_model=ExternalDocumentRead)
def upload_external_document(
    doc: ExternalDocumentCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    # Validar extensión
    if not allowed_file(doc.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Solo se permiten: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Decodificar el archivo base64
    try:
        file_bytes = base64.b64decode(doc.file_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Archivo base64 inválido")

    # Validar tamaño
    if len(file_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el tamaño máximo permitido de {settings.MAX_FILE_SIZE_MB} MB"
        )

    # Guardar archivo en disco
    file_location = os.path.join(UPLOAD_DIR, doc.filename)
    with open(file_location, "wb") as f:
        f.write(file_bytes)

    db_doc = ExternalDocument(
        filename=doc.filename,
        description=doc.description,
        file_url=file_location,
        uploaded_by_user_id=current_user.id,
        patient_id=doc.patient_id,
        outpatient_center_id=doc.outpatient_center_id,
        uploaded_at=datetime.utcnow()
    )
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)
    return db_doc

# READ ALL (por paciente)
@router.get("/patient/{patient_id}", response_model=list[ExternalDocumentRead])
def list_documents_by_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    docs = session.exec(select(ExternalDocument).where(ExternalDocument.patient_id == patient_id)).all()
    return docs

# READ ONE
@router.get("/{doc_id}", response_model=ExternalDocumentRead)
def get_external_document(
    doc_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    doc = session.get(ExternalDocument, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

# DELETE (solo el ambulatorio o el uploader puede borrar)
@router.delete("/{doc_id}")
def delete_external_document(
    doc_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    doc = session.get(ExternalDocument, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    # Permitir solo al uploader o al ambulatorio borrar
    user_roles = {role.name for role in current_user.roles}
    if doc.uploaded_by_user_id != current_user.id and "outpatient_center" not in user_roles:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este documento")
    # Borra el archivo físico
    if os.path.exists(doc.file_url):
        os.remove(doc.file_url)
    session.delete(doc)
    session.commit()
    return {"msg": "Documento eliminado"}