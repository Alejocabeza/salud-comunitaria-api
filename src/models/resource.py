from typing import Optional
from sqlmodel import Field, SQLModel, Column, ForeignKey
from datetime import datetime

class Resource(SQLModel, table=True):
    __tablename__ = "resources"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    dose: Optional[str] = Field(default=None, max_length=100)
    quantity: Optional[int] = Field(default=None, ge=0)
    in_stock: Optional[bool] = Field(default=True)
    outpatient_center_id: int = Field(default=None, sa_column=Column('outpatient_center_id', ForeignKey('outpatient_centers.id', ondelete='CASCADE')))
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 


class StoreResourceRequest(SQLModel):
    name: str = Field(max_length=100)
    dose: Optional[str] = Field(default=None, max_length=100)
    quantity: Optional[int] = Field(default=None, ge=0)
    in_stock: Optional[bool] = Field(default=True)
    outpatient_center_id: int = Field(default=None, sa_column=Column('outpatient_center_id', ForeignKey('outpatient_centers.id', ondelete='CASCADE')))
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class UpdateResourceRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    dose: Optional[str] = Field(default=None, max_length=100)
    quantity: Optional[int] = Field(default=None, ge=0)
    in_stock: Optional[bool] = Field(default=True)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
