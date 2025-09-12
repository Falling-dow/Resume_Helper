from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me():
    # TODO: Extract user from JWT and DB
    return {"id": "demo", "email": "demo@example.com", "username": "demo"}

