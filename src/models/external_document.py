from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ExternalDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    description: Optional[str] = None
    file_url: str
    uploaded_by_user_id: int = Field(foreign_key="user.id")
    patient_id: int = Field(foreign_key="patient.id")
    outpatient_center_id: int = Field(foreign_key="outpatientcenter.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)