from fastapi import APIRouter, Depends

from src.middleware.auth import get_current_user
from src.models.user import User

router = APIRouter()


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully"}
