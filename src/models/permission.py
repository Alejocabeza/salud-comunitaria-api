from typing import Optional
from sqlmodel import Field, SQLModel, Column, ForeignKey
from datetime import datetime

class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    description: str = Field(default=None, max_length=100)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default=None)
    deleted_at: Optional[str] = Field(default=None) 

class UserPermission(SQLModel, table=True):
    __tablename__ = "users_permissions"

    user_id: int = Field(
        default=None,
        sa_column=Column("user_id", ForeignKey("auths.id", ondelete="CASCADE"), primary_key=True)
    )
    permission_id: int = Field(
        default=None,
        sa_column=Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
    )

class RolePermission(SQLModel, table=True):
    __tablename__ = "roles_permissions"

    role_id: int = Field(
        default=None,
        sa_column=Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    )
    permission_id: int = Field(
        default=None,
        sa_column=Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
    )

class StorePermissionRequest(SQLModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

class UpdatePermissionRequest(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=20)
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
