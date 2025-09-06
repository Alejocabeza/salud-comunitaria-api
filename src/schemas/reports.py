
from pydantic import BaseModel
from typing import List

class OccupationByOutpatientCenter(BaseModel):
    outpatient_center_id: int
    outpatient_center_name: str
    patient_count: int
    doctor_count: int

class OccupationReport(BaseModel):
    data: List[OccupationByOutpatientCenter]

class ReportResponse(BaseModel):
    pdf_base64: str
