from sqlmodel import SQLModel, Field
from typing import Optional

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    outpatient_center_id: int = Field(foreign_key="outpatientcenter.id")
    user_id: int = Field(foreign_key="user.id", unique=True)