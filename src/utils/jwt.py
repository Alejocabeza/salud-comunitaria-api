from jose import jwt
from ..config.settings import settings

def create_access_token(payload: dict, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return True
    except jwt.JWTError:
        return None