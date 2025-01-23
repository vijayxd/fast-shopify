# app/api/v1/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from app.models.user import User
from app.db.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException

# OAuth2PasswordBearer will retrieve the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode(token, 'CHIPPA', algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
