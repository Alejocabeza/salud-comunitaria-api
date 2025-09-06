
import base64
from fastapi import APIRouter
from src.schemas.reports import ReportResponse
from src.services.reports import (
    get_patients_report_service,
    get_medical_resources_report_service,
    get_medication_requests_report_service,
    get_occupation_by_outpatient_center_report_service
)

router = APIRouter(
    prefix="/reports",
    tags=["Reportes"],
    responses={404: {"description": "Not found"}},
)

def _get_base64_encoded_pdf(pdf_bytes: bytes) -> ReportResponse:
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return ReportResponse(pdf_base64=pdf_base64)

@router.get("/patients", response_model=ReportResponse)
def get_patients_report():
    """Get a report of all patients in PDF format."""
    pdf_bytes = get_patients_report_service()
    return _get_base64_encoded_pdf(pdf_bytes)

@router.get("/medical_resources", response_model=ReportResponse)
def get_medical_resources_report():
    """Get a report of all medical resources in PDF format."""
    pdf_bytes = get_medical_resources_report_service()
    return _get_base64_encoded_pdf(pdf_bytes)

@router.get("/medication_requests", response_model=ReportResponse)
def get_medication_requests_report():
    """Get a report of all medication requests in PDF format."""
    pdf_bytes = get_medication_requests_report_service()
    return _get_base64_encoded_pdf(pdf_bytes)

@router.get("/occupation_by_outpatient_center", response_model=ReportResponse)
def get_occupation_by_outpatient_center_report():
    """Get a report of occupation by outpatient center in PDF format."""
    pdf_bytes = get_occupation_by_outpatient_center_report_service()
    return _get_base64_encoded_pdf(pdf_bytes)
