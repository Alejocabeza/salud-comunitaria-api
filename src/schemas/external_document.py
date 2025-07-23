from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalDocumentCreate(BaseModel):
    filename: str
    file_base64: str
    description: Optional[str] = None
    patient_id: int
    outpatient_center_id: int

class ExternalDocumentRead(BaseModel):
    id: int
    filename: str
    description: Optional[str] = None
    file_url: str
    uploaded_by_user_id: int
    patient_id: int
    outpatient_center_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True