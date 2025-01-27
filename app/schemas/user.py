# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.schemas.role import PermissionResponse
# Pydantic schema for creating a new user



class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

# Pydantic schema for updating user data (partial update)
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

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
        from_attributes = True

class UserAccountRoleResponse(BaseModel):
    account_id: int
    account_name: str
    role: str
    permissions: List["PermissionResponse"] = []

    class Config:
        from_attributes = True
        
class UserDetailsResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    user_account_roles: List[UserAccountRoleResponse]

    class Config:
        from_attributes = True

