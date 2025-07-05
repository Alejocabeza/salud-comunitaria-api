from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Doctors(SQLModel, table=True):
    __tablename__ = "doctors"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    email: str = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, max_length=20)
    phone: Optional[str] = Field(default=None, max_length=15)
    specialty: Optional[str] = Field(default=None, max_length=100)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 

class StoreDoctorRequest(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    dni: Optional[str] = Field(default=None, max_length=20)
    specialty: Optional[str] = Field(default=None, max_length=100)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class UpdateDoctorRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, max_length=20)
    specialty: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
