from pydantic import BaseModel, EmailStr, ConfigDict, ConfigDict
from typing import Optional

class PatientUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class PatientCreate(BaseModel):
    name: str
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    outpatient_center_id: int
    user: PatientUserCreate

class PatientUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class PatientRead(BaseModel):
    id: int
    name: str
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    outpatient_center_id: int
    user_id: int
    user: PatientUserRead

    class Config:
        orm_mode = True

class PatientReadResource(BaseModel):
    id: int
    name: str
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    outpatient_center_id: int
    user_id: int
    user: PatientUserRead

    model_config = ConfigDict(from_attributes=True)

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None