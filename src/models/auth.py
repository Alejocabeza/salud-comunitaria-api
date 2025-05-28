from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime  # <-- Agregado para default_factory

class Auth(SQLModel, table=True):
    __tablename__ = "auths"

    id: int = Field(default=None, primary_key=True, max_length=36)
    name: str = Field(max_length=100)
    email: str = Field(default=None, max_length=100, unique=True)
    password: str = Field(default=None)
    password_reset_token: Optional[str] = Field(default=None, max_length=100, nullable=True)
    email_reset_token: Optional[str] = Field(default=None, max_length=100, nullable=True)
    is_admin: bool = Field(default=False, nullable=False)
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat(), nullable=True)
    updated_at: Optional[str] = Field(default=None, nullable=True)

class AuthLogin(SQLModel):
    email: str = Field(max_length=100, nullable=False)
    password: str = Field(nullable=False)

class AuthForgotPassword(SQLModel):
    email: str = Field(max_length=100, nullable=False)

class AuthResetPassword(SQLModel):
    token: str = Field(max_length=100)
    email: str = Field(max_length=100, nullable=False)
    password: str = Field(nullable=False)