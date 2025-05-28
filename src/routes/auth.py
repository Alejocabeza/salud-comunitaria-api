from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..services.auth import auth_login
from ..models.auth import AuthLogin, AuthForgotPassword, AuthResetPassword
from ..config.database import get_session
from ..resource.auth.login_resource import LoginResource

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

@router.post("/login", response_model=LoginResource, status_code=status.HTTP_200_OK)
def login(auth: AuthLogin, db: Session = Depends(get_session)):
    result = auth_login(db, auth)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return result

# @router.post('forgot-password', response_model=AuthForgotPassword, status_code=status.HTTP_200_OK)
# def forgot_password(auth: AuthForgotPassword, db: Session = Depends(get_session)):
#     print(f"Processing forgot password for {auth.email}")

# @router.post('reset-password', response_model=AuthResetPassword, status_code=status.HTTP_201_CREATED)
# def reset_password(auth: AuthResetPassword, db: Session = Depends(get_session)):
#     print(f"Resetting password for {auth.email} with token {auth.token}")