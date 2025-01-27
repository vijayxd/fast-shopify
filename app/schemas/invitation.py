# app/schemas/invitation.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class InvitationCreate(BaseModel):
    account_id: int  # The account to which the invitee is being invited
    invitee_email: EmailStr  # Email of the user being invited
    role_id: int  # Role assigned to the invitee (e.g., 'Admin', 'Moderator')
    message: Optional[str] = None 

    class Config:
        from_attributes = True

from pydantic import BaseModel

class InvitationAcceptSchema(BaseModel):
    token: str
   