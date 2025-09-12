from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.base import get_db as _get_db


def get_db(db: Session = Depends(_get_db)) -> Session:
    return db

