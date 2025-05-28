from jose import jwt
from ..config.settings import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

def encode_token(payload: dict, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or 60)
    to_encode["exp"] = int(expire.timestamp())
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )