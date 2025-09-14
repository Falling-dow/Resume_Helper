from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User


class AuthService:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # ---------- public (DB-backed) ----------
    def register(self, db: Session, *, email: str, password: str, username: Optional[str] = None) -> User:
        exists = db.scalar(select(User).where(User.email == email))
        if exists:
            raise ValueError("Email already registered")
        now = datetime.utcnow()
        user = User(
            email=email,
            username=username,
            password_hash=self.pwd_context.hash(password),
            is_active=True,
            is_verified=False,
            created_at=now,
            updated_at=now,
        )
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Email already registered")
        db.refresh(user)
        return user

    def verify(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user: Optional[User] = db.scalar(select(User).where(User.email == email))
        if not user:
            return None
        if not self.pwd_context.verify(password, user.password_hash or ""):
            return None
        return user

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.scalar(select(User).where(User.email == email))
