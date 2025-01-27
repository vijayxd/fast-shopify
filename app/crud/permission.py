from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.role import PermissionCreate


# Create a new permission
def create_permission(db: Session, permission_data: PermissionCreate):
    permission = Permission(name=permission_data.name, description=permission_data.description)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


# Get a permission by ID
def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()


# Get all permissions
def get_all_permissions(db: Session):
    return db.query(Permission).all()
