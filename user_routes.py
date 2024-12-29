from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from database import get_session
from models import User
from typing import List, Optional

# Router setup
router = APIRouter()


# Create User
@router.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # Ensure unique email
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user

# Update User (Partial update)
@router.patch("/users/{user_id}", response_model=User)
def update_user(
    user_id: int, user_update: User, session: Session = Depends(get_session)
):
    # Fetch the user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the fields provided
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

# Delete User
@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    # Fetch the user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    
    return user

# Get All Users
@router.get("/users/", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# Get User by ID
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
