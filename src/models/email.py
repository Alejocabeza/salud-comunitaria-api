from pydantic import BaseModel, EmailStr

class Auth(BaseModel):
    email: EmailStr
    subject: str
    body: str
