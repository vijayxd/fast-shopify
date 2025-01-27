from sqlalchemy.orm import Session
from app.models.role import Role
from app.db.db import get_db

# Ensure roles are properly created
def check_and_seed_roles(db: Session):
    roles = [
        {"name": "Owner", "description": "Original user with full access"},
        {"name": "Admin", "description": "User with almost the same access as Owner"},
        {"name": "Moderator", "description": "User with limited access"}
    ]
    for role in roles:
        existing_role = db.query(Role).filter(Role.name == role["name"]).first()
        if not existing_role:
            new_role = Role(name=role["name"], description=role["description"])
            db.add(new_role)
    db.commit()
    print("Roles are set up correctly.")

