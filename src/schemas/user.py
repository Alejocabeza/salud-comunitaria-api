from pydantic import BaseModel, EmailStr, ConfigDict, ConfigDict
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    roles: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class RoleRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)