from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, ForeignKey
from datetime import datetime

class Roles(SQLModel, table=True):
    __tablename__ = "roles"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    description: str = Field(default=None, max_length=100)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 

class UserRole(SQLModel, table=True):
    __tablename__ = "auths_roles"

    user_id: int = Field(
        default=None,
        sa_column=Column("user_id", ForeignKey("auths.id", ondelete="CASCADE"), primary_key=True)
    )
    role_id: int = Field(
        default=None,
        sa_column=Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    )

class StoreRoleRequest(SQLModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    permissions: Optional[List[int]] = None
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class UpdateRoleRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=20)
    permissions: Optional[List[int]] = None
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
