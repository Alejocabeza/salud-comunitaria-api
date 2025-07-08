from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Patients(SQLModel, table=True):
    __tablename__ = "patients"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    email: str = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, max_length=20)
    phone: Optional[str] = Field(default=None, max_length=15)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 

class StorePatientRequest(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    dni: Optional[str] = Field(default=None, max_length=20)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class UpdatePatientRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
