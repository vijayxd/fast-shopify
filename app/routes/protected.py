# app/api/v1/endpoints/protected.py
from fastapi import APIRouter, Depends
from app.security.dependency import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/auth/", response_model=UserResponse)
async def protected_route(current_user: User = Depends(get_current_user)):
    return current_user
