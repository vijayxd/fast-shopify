# app/crud/user.py
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.orm import Session, joinedload
from app.models.account import Account
from app.models.role import UserAccountRole, Role
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserDetailsResponse
from app.security.password import hash_password, verify_password  # Assuming you have a separate file for hashing
from app.utils.mail import send_verification_email  # Assuming utility for email sending
import uuid
from passlib.context import CryptContext
from app.models.account import Account
from app.models.permission import Permission, RolePermission
from app.utils.token import generate_verification_token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_account(db:Session, user_id:int):
    acc = Account(name="Default",user_id=user_id)
    db.add(acc)
    db.commit()
    db.refresh(acc)

    userRole = UserAccountRole(user_id = user_id,account_id= acc.id,role_id=1)
    db.add(userRole)
    db.commit()
    db.refresh(userRole)


def create_jwt_token(email: str) -> str:
    expiration_time = timedelta(days=7)
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + expiration_time
    }
    token = jwt.encode(payload, 'CHIPPA', algorithm="HS256")
    return token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# Create a new user
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)  # Store hashed password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    await send_verification_email(db_user.email, generate_verification_token(db_user.email))
    return db_user

# Update user data
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_update.first_name:
            db_user.first_name = user_update.first_name
        if user_update.last_name:
            db_user.last_name = user_update.last_name
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.password = hash_password(user_update.password)
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active

        db.commit()
        db.refresh(db_user)
        return db_user
    return None

# Get a user by ID
def get_user_by_id(db: Session, user_id: int):
    user = (
        db.query(User)
        .options(
            joinedload(User.accounts).joinedload(Account.roles) # Eager load accounts
        )
        .filter(User.id == user_id)
        .first()
    )
    return user

# Get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# crud/user.py (add this to the same file)
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
