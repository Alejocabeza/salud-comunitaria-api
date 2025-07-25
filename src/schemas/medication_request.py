from pydantic import BaseModel, ConfigDict, ConfigDict
from typing import Optional
from datetime import datetime

class MedicationRequestCreate(BaseModel):
    medication_name: str
    quantity: int
    reason: Optional[str] = None
    outpatient_center_id: int

class MedicationRequestRead(BaseModel):
    id: int
    medication_name: str
    quantity: int
    reason: Optional[str] = None
    status: str
    requested_by_user_id: int
    outpatient_center_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MedicationRequestUpdate(BaseModel):
    status: Optional[str] = None
    updated_at: Optional[datetime] = None