from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.schemas.user import UserCreate, UserPublic
from src.services.auth_service import create_user, get_user_by_email

router = APIRouter()


@router.post("/register", response_model=UserPublic)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in.email, user_in.password)
    return UserPublic.model_validate(user)
