from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: constr(min_length=8) | None = None


class UserPublic(BaseModel):
    id: str
    email: str
    name: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: str
    email_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    token: str
    access_token: str | None = None
    token_type: str = "bearer"
    user: UserPublic
