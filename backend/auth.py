from datetime import timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from . import crud, schemas, security, models
from .database import get_db

# This constant was missing, causing the login to crash the server.
# It defines the token's lifespan in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Token Creation & Verification ---

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return security.create_access_token(data, expires_delta)

def create_password_reset_token(phone_number: str):
    return security.create_access_token(
        data={"sub": phone_number, "scope": "password-reset"},
        expires_delta=timedelta(minutes=15)
    )

def verify_password_reset_token(token: str):
    return security.decode_password_reset_token(token)

# --- Authentication Logic ---

def authenticate_user(db: Session, phone_number: str, password: str) -> Optional[models.User]:
    """
    Authenticates a user by phone number and password.

    Args:
        db: The database session.
        phone_number: The user's phone number.
        password: The user's password.

    Returns:
        The authenticated user object, or None if authentication fails.
    """
    user = crud.get_user_by_phone_number(db, phone_number=phone_number)
    if not user or not security.verify_password(password, user.hashed_password):
        return None
    return user

# --- Dependency for Protected Routes ---

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    phone_number = security.decode_access_token(token)
    if phone_number is None:
        raise credentials_exception
    
    user = crud.get_user_by_phone_number(db, phone_number=phone_number)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    # In the future, you could add a `disabled` flag to the user model
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user