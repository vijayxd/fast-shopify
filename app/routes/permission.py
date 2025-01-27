from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.role import PermissionCreate, PermissionResponse
from app.crud.permission import create_permission, get_all_permissions
from app.db.db import get_db

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

# Route to create a new permission
@router.post("/", response_model=PermissionResponse)
def create_new_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db, permission)


# Route to get all permissions
@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    return get_all_permissions(db)
