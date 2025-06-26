from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class OutpatientCenter(SQLModel, table=True):
    __tablename__ = "outpatient_centers"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    email: str = Field(default=None, max_length=100)
    rif: Optional[str] = Field(default=None, max_length=20)
    phone: Optional[str] = Field(default=None, max_length=15)
    address: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 

class OutpatientCenterCreate(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    rif: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class OutpatientCenterUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    rif: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())