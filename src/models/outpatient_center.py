from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class OutpatientCenter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[str] = None
    responsible: Optional[str] = None
    active: bool = Field(default=True)
    user_id: int = Field(foreign_key="user.id", unique=True)