# app/api/invitations.py
from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from app.db.db import get_db
router = APIRouter()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.invitation import InvitationCreate, InvitationAcceptSchema
from app.services.invitation import accept_invitation, send_invitation
from app.security.dependency import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/invitations")
async def create_invitation(
    invitation: InvitationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
   return await send_invitation(db,invitation,user.id)


@router.get("/accept-invitation")
async def accept_invitation_route(
    token: str, db: Session = Depends(get_db)
):
    """
    Accepts the invitation by validating the JWT token, checking if the user exists,
    assigning the role, and marking the invitation as accepted.
    """
    try:
        result = await accept_invitation(db=db, token=token)
        return result
    except HTTPException as e:
        raise e  # Re-raise the HTTPException for proper handling by FastAPI




