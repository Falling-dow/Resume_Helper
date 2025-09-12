from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext

from app.core.security import create_access_token
from app.schemas.user import Token, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=Token)
def register(user: UserCreate) -> Token:
    # TODO: implement real DB logic, email verification, etc.
    hashed = pwd_context.hash(user.password)
    if not hashed:
        raise HTTPException(status_code=400, detail="Registration failed")
    token = create_access_token(user.email, expires_delta=timedelta(minutes=60))
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(user: UserCreate) -> Token:
    # TODO: validate user credentials from DB
    token = create_access_token(user.email, expires_delta=timedelta(minutes=60))
    return Token(access_token=token)

