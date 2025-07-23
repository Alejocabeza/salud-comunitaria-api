from sqlmodel import SQLModel, Field
from typing import Optional

class MedicalResource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    quantity: int = Field(default=0)
    unit: Optional[str] = None  # Ej: "cajas", "unidades", "litros"
    outpatient_center_id: int = Field(foreign_key="outpatientcenter.id")