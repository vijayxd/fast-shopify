from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleResponse, AssignRoleSchema
from app.crud.role import create_role, get_all_roles, assign_role_to_user
from app.db.db import get_db

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# Route to create a new role
@router.post("/", response_model=RoleResponse)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)


# Route to get all roles
@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    return get_all_roles(db)


# Route to assign a role to a user
@router.post("/assign/")
def assign_role(role_data: AssignRoleSchema, db: Session = Depends(get_db)):
    try:
        return assign_role_to_user(
            db,
            user_id=role_data.user_id,
            role_id=role_data.role_id,
            additional_permissions=role_data.additional_permissions,
            account_id = role_data.account_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
