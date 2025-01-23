# app/utils/token.py
import jwt
from datetime import datetime, timedelta,timezone

def generate_verification_token(email: str) -> str:
    expiration_time = timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + expiration_time
    }
    token = jwt.encode(payload, 'CHIPPA', algorithm="HS256")
    return token
