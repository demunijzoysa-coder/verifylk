from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....config import get_settings
from ....db import get_db
from ....models import UserRole
from ....repositories.users import create_user, get_by_email
from ....schemas.models import Token, UserCreate, UserOut
from ....security import create_access_token, create_refresh_token, verify_password

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=UserOut, summary="Register new user")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = create_user(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
        org_id=None,
    )
    return user


@router.post("/login", response_model=Token, summary="Login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_expires = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    return Token(
        access_token=create_access_token(user.id, user.role.value, access_expires),
        refresh_token=create_refresh_token(user.id, user.role.value, refresh_expires),
    )
