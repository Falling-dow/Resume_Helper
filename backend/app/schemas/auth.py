from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LogoutResponse(BaseModel):
    detail: str = "logged out"

