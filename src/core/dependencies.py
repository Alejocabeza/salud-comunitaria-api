from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from ..core.database import get_session
from ..core.security import decode_access_token
from ..models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = session.exec(select(User).where(User.username == payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(role_name: str):
    def role_checker(user: User = Depends(get_current_user)):
        if not any(role.name == role_name for role in user.roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

def require_permission(permission_name: str):
    def permission_checker(user = Depends(get_current_user)):
        user_permissions = set()
        for role in user.roles:
            for perm in getattr(role, "permissions", []):
                user_permissions.add(perm.name)
        if permission_name not in user_permissions:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return permission_checker