from ...models.auth import Auth
from pydantic import BaseModel
from typing import Optional

class LoginResource(BaseModel):
    id: int
    name: str
    email: str
    password_reset_token: Optional[str] = None
    email_reset_token: Optional[str] = None
    token: Optional[dict] = None

    @classmethod
    def from_auth(cls, auth: Auth, **kwargs) -> "LoginResource":
        return cls(
            id=auth.id,
            name=auth.name,
            email=auth.email,
            password_reset_token=auth.password_reset_token,
            email_reset_token=auth.email_reset_token,
            token={
                "access_token": kwargs.get("token"),
                "type_token": "bearer",
                "expires_in": kwargs.get('expires_in')
            }
        )
