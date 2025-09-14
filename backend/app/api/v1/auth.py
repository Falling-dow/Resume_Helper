from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token
from app.schemas.user import Token
from app.schemas.auth import LoginRequest, RegisterRequest, LogoutResponse
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(body: RegisterRequest, db: Session = Depends(get_db)) -> Token:
    svc = AuthService()
    try:
        svc.register(db, email=body.email, password=body.password, username=body.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = create_access_token(body.email, expires_delta=timedelta(minutes=60))
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> Token:
    svc = AuthService()
    user = svc.verify(db, email=body.email, password=body.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(body.email, expires_delta=timedelta(minutes=60))
    return Token(access_token=token)


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    # JWT is stateless; client should drop the token.
    return LogoutResponse()
