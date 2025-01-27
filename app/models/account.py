# app/models/user.py
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime, timezone

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    # Relationships
    invitations = relationship("Invitation", back_populates="account")
    users = relationship("User", secondary="user_account_roles", back_populates="accounts")
    user_account_roles = relationship("UserAccountRole", back_populates="account")

