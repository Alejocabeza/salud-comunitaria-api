from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from ..schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from ..core.security import verify_password, create_access_token, create_reset_password_token, verify_reset_password_token, get_password_hash
from ..core.database import get_session
from ..models.user import User
from ..schemas.auth import Token

router = APIRouter(
    prefix="/auths",
    tags=["Autenticación"],
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Simulación de envío de correo (reemplaza por fastapi-mail en producción)
def send_reset_email(email: str, token: str):
    print(f"Enviando email a {email} con el token: {token}")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == request.email)).first()
    if not user:
        # No revelar si el email existe o no
        return {"msg": "Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña."}
    token = create_reset_password_token(user.email)
    background_tasks.add_task(send_reset_email, user.email, token)
    return {"msg": "Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, session: Session = Depends(get_session)):
    email = verify_reset_password_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.hashed_password = get_password_hash(request.new_password)
    session.add(user)
    session.commit()
    return {"msg": "Contraseña restablecida correctamente"}