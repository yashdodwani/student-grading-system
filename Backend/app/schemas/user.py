from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.models.user import UserRole

# Base User Schema
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Schema for user creation
class UserCreate(UserBase):
    password: str
    role: UserRole

# Schema for user update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Schema for user response
class UserResponse(UserBase):
    id: str
    role: UserRole

    class Config:
        from_attributes = True

# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None