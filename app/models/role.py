from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.db import Base

# Roles table
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship for debugging or advanced queries
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete")
    

    

    accounts = relationship("Account", secondary="user_account_roles", back_populates="roles", viewonly=True)


class UserAccountRole(Base):
    __tablename__ = "user_account_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Could link to an Account table in the future
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    custom_permissions = relationship(
        "Permission",
        secondary="user_account_role_permissions",
        back_populates="assigned_roles",
        cascade="all, delete",
    )

  


