from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission
from app.models.permission import RolePermission

def seed_role_permissions(db:Session):
    # Define role-permission mapping
    role_permissions = {
        "Owner": [
            "view_orders", "add_orders", "edit_orders", "delete_orders",
            "view_products", "add_products", "edit_products", "delete_products",
            "view_users", "add_users", "edit_users", "delete_users",
            "view_roles", "edit_roles", "assign_roles"
        ],
        "Admin": [
            "view_orders", "add_orders", "edit_orders", "delete_orders",
            "view_products", "add_products", "edit_products", "delete_products",
            "view_users", "add_users", "edit_users", "delete_users",
            "view_roles", "edit_roles", "assign_roles"
        ],
        "Moderator": [
            "view_orders", "add_orders",
            "view_products", "add_products"
        ]
    }

    # Fetch all roles and permissions
    roles = {role.name: role for role in db.query(Role).all()}
    permissions = {perm.name: perm for perm in db.query(Permission).all()}

    # Assign permissions to roles
    for role_name, perm_names in role_permissions.items():
        role = roles.get(role_name)
        if role:
            for perm_name in perm_names:
                permission = permissions.get(perm_name)
                if permission:
                    # Check if role-permission relationship already exists
                    existing_relation = db.query(RolePermission).filter_by(
                        role_id=role.id, permission_id=permission.id
                    ).first()
                    if not existing_relation:
                        # Add new role-permission relationship
                        db.add(RolePermission(role_id=role.id, permission_id=permission.id))

    db.commit()
