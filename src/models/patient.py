from sqlmodel import SQLModel, Field
from typing import Optional

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birthdate: Optional[str] = None  # Puedes usar date si prefieres
    phone: Optional[str] = None
    email: Optional[str] = None
    outpatient_center_id: int = Field(foreign_key="outpatientcenter.id")
    user_id: int = Field(foreign_key="user.id", unique=True)