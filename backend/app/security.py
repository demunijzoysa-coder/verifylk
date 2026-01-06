from datetime import datetime, timedelta
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: dict[str, Any] = {"sub": str(subject), "role": role}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: dict[str, Any] = {"sub": str(subject), "role": role, "type": "refresh"}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.refresh_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
