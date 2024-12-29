from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import Column, String, Integer, UniqueConstraint

# User Model (No change needed from previous code)
class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="unique_email"),)

    id: int = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    )
    name: Optional[str] = Field(max_length=100)
    email: Optional[str] = Field(max_length=100, sa_column=Column(String(100), unique=True, nullable=False))
    is_active: Optional[bool] = Field(default=True)

    # Relationship to Shopify stores
    stores: List["ShopifyStore"] = Relationship(back_populates="user")

# Shopify Store Model
class ShopifyStore(SQLModel, table=True):
    __tablename__ = "shopify_stores"
    
    id: int = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    )
    store_name: str = Field(max_length=100, sa_column=Column(String(100), unique=True, nullable=False))
    access_token: str = Field(sa_column=Column(String, nullable=False))

    # Foreign key to the user table
    user_id: int = Field(foreign_key="users.id", nullable=False)

    # Relationship back to User
    user: User = Relationship(back_populates="stores")


# Request model for updating the product
class UpdateProductRequest(BaseModel):
    product_id: str
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    product_type: Optional[str] = None
    collectionsToJoin: Optional[List[str]] = None
    collectionsToLeave: Optional[List[str]] = None