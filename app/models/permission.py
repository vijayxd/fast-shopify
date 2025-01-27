from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.db import Base
from sqlalchemy.orm import relationship

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete")
    assigned_roles = relationship(
        "UserAccountRole",
        secondary="user_account_role_permissions",
        back_populates="custom_permissions",
        cascade="all, delete",
    )



class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")



class UserAccountRolePermission(Base):
    __tablename__ = "user_account_role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_account_role_id = Column(Integer, ForeignKey("user_account_roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    # user_account_role = relationship("UserAccountRole", back_populates="custom_permissions")
    # permission = relationship("Permission", back_populates="assigned_roles")