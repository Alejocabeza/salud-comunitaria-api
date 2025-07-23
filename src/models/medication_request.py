from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class MedicationRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medication_name: str
    quantity: int
    reason: Optional[str] = None
    status: str = Field(default="pending")  # pending, approved, rejected, delivered, etc.
    requested_by_user_id: int = Field(foreign_key="user.id")
    outpatient_center_id: int = Field(foreign_key="outpatientcenter.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None