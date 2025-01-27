from sqlalchemy.orm import Session
from app.models.permission import Permission

def seed_permissions(db:Session ):
    # Define the permissions you want to seed
    permissions = [
        {"name": "view_orders", "description": "Can view orders"},
        {"name": "add_orders", "description": "Can add new orders"},
        {"name": "edit_orders", "description": "Can edit existing orders"},
        {"name": "delete_orders", "description": "Can delete orders"},
        
        {"name": "view_products", "description": "Can view products"},
        {"name": "add_products", "description": "Can add new products"},
        {"name": "edit_products", "description": "Can edit existing products"},
        {"name": "delete_products", "description": "Can delete products"},
        
        {"name": "view_users", "description": "Can view users"},
        {"name": "add_users", "description": "Can add new users"},
        {"name": "edit_users", "description": "Can edit user details"},
        {"name": "delete_users", "description": "Can delete users"},
        
        {"name": "view_roles", "description": "Can view roles"},
        {"name": "edit_roles", "description": "Can edit roles"},
        {"name": "assign_roles", "description": "Can assign roles to users"}
    ]
    
    # Check if permissions already exist, if not, add them
    for perm in permissions:
        existing_perm = db.query(Permission).filter(Permission.name == perm['name']).first()
        if not existing_perm:
            permission = Permission(
                name=perm["name"], 
                description=perm["description"]
            )
            db.add(permission)
    
    db.commit()
    print("Permissions have been seeded successfully.")