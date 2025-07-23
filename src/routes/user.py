from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..core.database import get_session
from ..models.user import User, Role
from ..schemas.user import UserCreate, UserRead
from ..core.security import decode_access_token
from ..core.dependencies import get_current_user, require_role
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(decode_access_token)]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.get("/me")
def read_own_profile(current_user = Depends(get_current_user)):
    return current_user