from pydantic import BaseModel, EmailStr, ConfigDict, ConfigDict
from typing import Optional

class OutpatientCenterUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class OutpatientCenterUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class OutpatientCenterCreate(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    responsible: Optional[str] = None

class OutpatientCenterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    responsible: Optional[str] = None
    active: Optional[bool] = None

class OutpatientCenterRead(BaseModel):
    id: int
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    responsible: Optional[str] = None
    active: bool
    user: Optional[OutpatientCenterUserRead] = None

    model_config = ConfigDict(from_attributes=True)


class OutpatientCenterReadOne(BaseModel):
    id: int
    name: str
    address: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    responsible: Optional[str] = None
    active: bool

    model_config = ConfigDict(from_attributes=True)