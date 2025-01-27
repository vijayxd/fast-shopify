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

 # Assuming you have these configured in your settings

def generate_invitation_token(invitee_email: str, invitation_id: int, inviter_id: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(days=7)  # Token valid for 7 days
    to_encode = {"email": invitee_email, "invitation_id": invitation_id, "exp": expiration, "inviter_id": inviter_id}
    encoded_token = jwt.encode(to_encode, 'CHIPPA', algorithm="HS256")
    return encoded_token
