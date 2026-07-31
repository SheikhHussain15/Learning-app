from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.middleware.auth import get_current_user
from src.models.user import User
from src.schemas.user import UserResponse, UserUpdate
from src.services.auth_service import hash_password

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/profile", response_model=UserResponse)
def update_profile(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_in.email is not None:
        existing = db.query(User).filter(User.email == user_in.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_in.email

    if user_in.password is not None:
        current_user.password_hash = hash_password(user_in.password)

    db.commit()
    db.refresh(current_user)
    return current_user
