
from sqlmodel import Session, select
from sqlalchemy import func
from fpdf import FPDF
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.outpatient_center import OutpatientCenter
from src.models.medical_resource import MedicalResource
from src.models.medication_request import MedicationRequest
from src.core.database import get_session
from src.schemas.reports import OccupationByOutpatientCenter

def _generate_pdf_report(title: str, headers: list, data: list) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    
    col_width = pdf.w / (len(headers) + 1)
    row_height = pdf.font_size * 1.5
    
    pdf.set_font("Arial", 'B', 10)
    for header in headers:
        pdf.cell(col_width, row_height, header, border=1)
    pdf.ln(row_height)
    
    pdf.set_font("Arial", '', 10)
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
        
    return pdf.output(dest='S').encode('latin-1')

def get_patients_report_service():
    with get_session() as session:
        statement = select(Patient)
        patients = session.exec(statement).all()
        headers = ["ID", "Name", "Birthdate", "Phone", "Email"]
        data = [[p.id, p.name, p.birthdate, p.phone, p.email] for p in patients]
        return _generate_pdf_report("Patients Report", headers, data)

def get_medical_resources_report_service():
    with get_session() as session:
        statement = select(MedicalResource)
        medical_resources = session.exec(statement).all()
        headers = ["ID", "Name", "Description", "Quantity", "Unit"]
        data = [[r.id, r.name, r.description, r.quantity, r.unit] for r in medical_resources]
        return _generate_pdf_report("Medical Resources Report", headers, data)

def get_medication_requests_report_service():
    with get_session() as session:
        statement = select(MedicationRequest)
        medication_requests = session.exec(statement).all()
        headers = ["ID", "Medication Name", "Quantity", "Status", "Created At"]
        data = [[r.id, r.medication_name, r.quantity, r.status, r.created_at] for r in medication_requests]
        return _generate_pdf_report("Medication Requests Report", headers, data)

def get_occupation_by_outpatient_center_report_service():
    with get_session() as session:
        patient_counts = session.exec(
            select(OutpatientCenter.id, func.count(Patient.id).label("patient_count"))
            .join(Patient, OutpatientCenter.id == Patient.outpatient_center_id)
            .group_by(OutpatientCenter.id)
        ).all()

        doctor_counts = session.exec(
            select(OutpatientCenter.id, func.count(Doctor.id).label("doctor_count"))
            .join(Doctor, OutpatientCenter.id == Doctor.outpatient_center_id)
            .group_by(OutpatientCenter.id)
        ).all()

        outpatient_centers = session.exec(select(OutpatientCenter)).all()

        patient_map = {row[0]: row[1] for row in patient_counts}
        doctor_map = {row[0]: row[1] for row in doctor_counts}

        headers = ["Center ID", "Center Name", "Patient Count", "Doctor Count"]
        data = [
            [center.id, center.name, patient_map.get(center.id, 0), doctor_map.get(center.id, 0)]
            for center in outpatient_centers
        ]

        return _generate_pdf_report("Occupation by Outpatient Center Report", headers, data)
