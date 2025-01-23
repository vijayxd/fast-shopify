# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Pydantic schema for creating a new user

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

# Pydantic schema for updating user data (partial update)
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True

# Pydantic schema for the user response (to be used in GET requests)
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
