from ..models.doctors import Doctors
from pydantic import BaseModel
from typing import Optional

class ResourceDoctor(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    dni: Optional[str] = None
    phone: Optional[str] = None
    specialty: Optional[str] = None
    address: Optional[str] = None

    @classmethod
    def from_array(cls, doctor: Doctors, **kwargs) -> "ResourceDoctor":
        return cls(
            id=doctor.id,
            name=doctor.name,
            email=doctor.email,
            dni=doctor.dni,
            phone=doctor.phone,
            specialty=doctor.specialty,
        )
