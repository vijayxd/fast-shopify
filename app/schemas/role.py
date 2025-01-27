# app/schemas/role.py
from pydantic import BaseModel
from typing import List, Optional


# Base schema for Role
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Schema for creating a new role
class RoleCreate(RoleBase):
    permissions: Optional[List[int]] = []  # List of permission IDs


# Schema for returning role details
class RoleResponse(RoleBase):
    id: int
    permissions: List["PermissionResponse"]
    
    class Config:
        from_attributes = True


# Base schema for Permission
class PermissionBase(BaseModel):
    name: str = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Schema for creating a new permission
class PermissionCreate(PermissionBase):
    pass


# Schema for returning permission details
class PermissionResponse(PermissionBase):
    id: int
    
    class Config:
        from_attributes = True


# Schema for assigning a role to a user
class AssignRoleSchema(BaseModel):
    user_id: int
    role_id: int
    account_id:int
    additional_permissions: Optional[List[int]] = []  # List of additional permission IDs to assign

    class Config:
        from_attributes = True


# To handle recursive relationships
RoleResponse.model_rebuild()
