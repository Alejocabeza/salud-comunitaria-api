from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class DoctorCreate(BaseModel):
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    outpatient_center_id: int

class DoctorUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class DoctorRead(BaseModel):
    id: int
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    outpatient_center_id: int
    user_id: int
    user: DoctorUserRead

    class Config:
        orm_mode = True


class DoctorReadResource(BaseModel):
    id: int
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True