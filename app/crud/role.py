from sqlalchemy.orm import Session, joinedload
from app.models.role import Role, UserAccountRole
from app.models.permission import Permission, RolePermission, UserAccountRolePermission
from app.models.user import User
from app.schemas.role import RoleCreate


# Create a new role
def create_role(db: Session, role_data: RoleCreate):
    role = Role(name=role_data.name, description=role_data.description)
    db.add(role)
    db.commit()
    db.refresh(role)

    # Attach permissions if provided
    if role_data.permissions:
        permissions = db.query(Permission).filter(Permission.id.in_(role_data.permissions)).all()
        role.permissions.extend(permissions)
        db.commit()

    return role


# Get a role by ID
def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


# Get all roles
def get_all_roles(db: Session):
    return db.query(Role).options(joinedload(Role.permissions).joinedload(RolePermission.permission)).all()


# Assign a role to a user

def assign_role_to_user(
    db: Session, user_id: int, role_id: int, account_id: int, additional_permissions: list = []
):
    # Step 1: Validate user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Step 2: Validate role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise ValueError("Role not found")

    # Step 3: Validate additional permissions
    if additional_permissions:
        valid_permissions = db.query(Permission).filter(Permission.id.in_(additional_permissions)).all()
        if len(valid_permissions) != len(additional_permissions):
            raise ValueError("One or more additional permissions are invalid")

    # Step 4: Check if the user already has a role for the account
    existing_user_role = (
        db.query(UserAccountRole)
        .filter(
            UserAccountRole.user_id == user_id,
            UserAccountRole.account_id == account_id,
            UserAccountRole.role_id == role_id,
        )
        .first()
    )
    if existing_user_role:
        raise ValueError("User already has this role for the account")

    # Step 5: Assign role to user for the account
    user_account_role = UserAccountRole(
        user_id=user_id, account_id=account_id, role_id=role_id
    )
    db.add(user_account_role)
    db.commit()

    # Step 6: Assign additional permissions if provided
    if additional_permissions:
        for permission_id in additional_permissions:
            user_account_role_permission = UserAccountRolePermission(
                user_account_role_id=user_account_role.id, permission_id=permission_id
            )
            db.add(user_account_role_permission)

        db.commit()

    return {"message": "Role and permissions assigned successfully", "user_id": user_id}

