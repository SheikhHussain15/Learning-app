from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import create_access_token
from src.core.deps import get_db
from src.schemas.user import AuthResponse, UserCreate, UserPublic
from src.services.auth_service import create_user, get_user_by_email

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in.email, user_in.password)
    token = create_access_token(data={"sub": user.id, "user_id": user.id, "email": user.email})
    return AuthResponse(
        token=token,
        access_token=token,
        user=UserPublic.model_validate(user),
    )
