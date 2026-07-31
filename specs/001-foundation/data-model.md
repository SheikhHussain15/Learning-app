# Data Model: AI Learning Platform Foundation

**Date**: 2026-07-01
**Phase**: Phase 1 - Data Model

## Entity: User

The User entity represents a registered user of the AI Learning Platform. This is the only entity required for Phase 1.

### Fields

| Field | Type | Nullable | Default | Constraints |
|-------|------|----------|---------|-------------|
| id | UUID | No | - | Primary Key, Indexed |
| email | String | No | - | Unique, Indexed, Not Null |
| email_verified | Boolean | No | false | Not Null |
| password_hash | String | No | - | Not Null, min 64 chars |
| created_at | DateTime | No | now() | Not Null |
| updated_at | DateTime | No | now() | Not Null |
| last_login | DateTime | Yes | null | Nullable |

### Relationships

None in Phase 1. Future phases may include:
- Documents (one-to-many)
- Sessions (one-to-many)

### Validation Rules

1. **Email**: Must be valid email format, max 255 characters
2. **Password**: Minimum 8 characters, must be hashed with bcrypt
3. **id**: Auto-generated UUID v4

### Indexes

- Primary Key: `id` (clustered)
- Unique Index: `email`
- Non-clustered Index: `created_at` (for audit queries)

### Database Constraints

- `email` must be unique
- `password_hash` cannot be empty
- `created_at` defaults to current timestamp
- `updated_at` auto-updates on row modification

### SQLAlchemy Model

```python
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)
```

## Schema Definitions

### UserCreate (Pydantic)
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
```

### UserUpdate (Pydantic)
```python
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
```

### UserResponse (Pydantic)
```python
class UserResponse(BaseModel):
    id: UUID
    email: str
    email_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
```