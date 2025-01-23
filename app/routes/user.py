# routes/user.py
from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.crud.user import create_jwt_token, create_user, verify_password
from app.db.db import get_db
from app.models.user import User  # Import User model

from app.crud import user as user_crud
from app.utils.mail import  send_verification_email
from app.utils.token import generate_verification_token

router = APIRouter()




@router.get("/resend-verify-email")
async def resend_verify_email(email: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    await send_verification_email(db_user.email, generate_verification_token(db_user.email))
    return {"message": "Verification email sent successfully"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token to get the user's email
        payload = jwt.decode(token, 'CHIPPA', algorithms=["HS256"])
        email = payload.get("sub")
        
        # Find the user with the given email
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the user is already verified
        if user.is_verified:
            raise HTTPException(status_code=400, detail="Email already verified")
        
        # Mark the user's email as verified
        user.is_verified = True
        db.commit()

        return {"message": "Email successfully verified!"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    

@router.post("/register/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the user using the CRUD function
    new_user = create_user(db=db, user=user)
    return new_user

# routes/user.py (add this to the same file)
from app.crud.user import get_user_by_id


@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    # Verify the password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # If login is successful, create JWT token
    token = create_jwt_token(db_user.email)

    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# routes/user.py (add this to the same file)
@router.get("/users/email/{email}", response_model=UserResponse)
def get_user_by_email_route(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# routes/user.py (add this to the same file)
from app.crud.user import update_user
from app.schemas.user import UserUpdate

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# routes/user.py (add this to the same file)
from app.crud.user import delete_user

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


