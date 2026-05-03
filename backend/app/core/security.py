"""
Security helpers: password hashing and JWT handling.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """Hash a plain password."""
#     return pwd_context.hash(password)

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    bcrypt has a strict limit of 72 bytes.
    We enforce validation instead of silent truncation.
    """

    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long (max 72 bytes allowed)")

    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(password, hashed)


def create_access_token(payload: dict) -> str:
    """Create signed JWT with expiry."""
    data = payload.copy()
    data["exp"] = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode JWT and return payload."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return {}