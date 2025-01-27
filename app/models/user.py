# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)  # Add length for VARCHAR
    last_name = Column(String(255), nullable=False)   # Add length for VARCHAR
    email = Column(String(255), unique=True, nullable=False)  # Add length for VARCHAR
    password = Column(String(255), nullable=False)  # Add length for VARCHAR
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Add the is_verified field

    created_at = Column(String(255), default=datetime.now(timezone.utc))
    updated_at = Column(String(255), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    accounts = relationship("Account", secondary="user_account_roles", overlaps="roles")

    
