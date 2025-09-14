from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user
