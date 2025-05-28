from typing import List
from sqlmodel import Session, select
from ..models.auth import Auth, AuthLogin
from passlib.context import CryptContext
from ..resource.auth.login_resource import LoginResource

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth_login(db: Session, auth_login: AuthLogin):
    user = db.exec(select(Auth).where(Auth.email == auth_login.email)).first()
    if not user:
        return None 
    if not pwd_context.verify(auth_login.password, user.password):
        return None 
    return LoginResource.from_auth(user)
    