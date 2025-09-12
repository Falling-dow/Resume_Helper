from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

