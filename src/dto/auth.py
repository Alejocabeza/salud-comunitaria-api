from typing import Optional
from ..models.auth import Auth
from pydantic import BaseModel

class LoginResponse(BaseModel):
    id: int
    name: str
    email: str
    password_reset_token: Optional[str] = None
    email_reset_token: Optional[str] = None

    @classmethod
    def from_auth(cls, auth: Auth):
        return cls(
            id=auth.id,
            name=auth.name,
            email=auth.email,
            password_reset_token=auth.password_reset_token,
            email_reset_token=auth.email_reset_token,
        )

