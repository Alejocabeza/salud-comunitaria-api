from ..models.patient import Patients
from pydantic import BaseModel
from typing import Optional

class ResourcePatient(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    dni: Optional[str] = None
    phone: Optional[str] = None
    specialty: Optional[str] = None
    address: Optional[str] = None

    @classmethod
    def from_array(cls, patient: Patients, **kwargs) -> "ResourcePatient":
        return cls(
            id=patient.id,
            name=patient.name,
            email=patient.email,
            dni=patient.dni,
            phone=patient.phone,
        )
