from typing import Optional
from sqlmodel import Field, SQLModel, Column, ForeignKey
from datetime import datetime

class RequestMedicine(SQLModel, table=True):
    __tablename__ = "request_medicines"

    id: int = Field(default=None, primary_key=True, max_length=36)
    auth_id: int = Field(default=None, sa_column=Column('auth_id', ForeignKey('auths.id', ondelete='CASCADE')))
    name: str = Field(max_length=100)
    quantity: int = Field(ge=0)
    reason: Optional[str] = Field(default=None, max_length=255)
    send_email_at: Optional[str] = Field(default=None, nullable=True)
    is_sent_email: bool = Field(default=False)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    deleted_at: Optional[str] = Field(default=None, nullable=True)


class StoreRequestMedicineRequest(SQLModel):
    name: str = Field(max_length=100)
    auth_id: int = Field(default=None, sa_column=Column('auth_id', ForeignKey('auths.id', ondelete='CASCADE')))
    reason: Optional[str] = Field(default=None, max_length=255)
    quantity: int = Field(ge=0)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class UpdateRequestMedicineRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    auth_id: Optional[int] = Field(default=None, sa_column=Column('auth_id', ForeignKey('auths.id', ondelete='CASCADE')))
    reason: Optional[str] = Field(default=None, max_length=255)
    quantity: Optional[int] = Field(default=None, ge=0)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
