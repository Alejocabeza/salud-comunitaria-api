from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from .role_permission import RolePermission

class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)
