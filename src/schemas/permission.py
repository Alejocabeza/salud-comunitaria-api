from pydantic import BaseModel
from typing import Optional

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True