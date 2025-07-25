from pydantic import BaseModel, ConfigDict, ConfigDict
from typing import Optional

class MedicalResourceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 0
    unit: Optional[str] = None
    outpatient_center_id: int

class MedicalResourceRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    unit: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MedicalResourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None