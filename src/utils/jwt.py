from typing import Annotated
from jose import jwt
from sqlmodel import select
from ..models.auth import Auth
from ..config.settings import settings
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..config.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def encode_token(payload: dict, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or 60)
    to_encode["exp"] = int(expire.timestamp())
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = get_session().exec(
            select(Auth).where(Auth.id == payload.get("sub"))
        ).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise credentials_exception