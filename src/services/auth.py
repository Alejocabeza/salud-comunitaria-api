from typing import List
from sqlmodel import Session, select
from ..models.auth import Auth, AuthLogin
from passlib.context import CryptContext
from ..resource.login_resource import LoginResource
from ..utils.jwt import encode_token 
from ..config.settings import settings
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth_login(db: Session, auth_login: AuthLogin):
    user = db.exec(select(Auth).where(Auth.email == auth_login.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not pwd_context.verify(auth_login.password, user.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    token = encode_token({"email": user.email, "id": user.id})
    return LoginResource.from_auth(user, token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

