from uuid import uuid4
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.role import Role, UserAccountRole
from app.models.invitation import Invitation
from app.utils.mail import send_invitation_email
from app.schemas.invitation import InvitationCreate
from app.utils.token import generate_invitation_token
from sqlalchemy.orm import Session
from app.models.user import User

async def send_invitation(db: Session, invitation_data: InvitationCreate, inviter_id: int):
    # Step 1: Check if account_id is provided

    account_id = invitation_data.account_id
    

    if db.query(User).filter(User.id == inviter_id).first().email == invitation_data.invitee_email:
        raise HTTPException(status_code=400, detail="You cannot invite yourself")


    # Step 2: If account_id is provided, check if it exists
    if account_id:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
    else:
        # Step 3: If account_id is not provided, create an account for the inviter
        # Check if the inviter already has an account
        inviter_account = db.query(Account).filter(Account.user_id == inviter_id).first()

        

        if not inviter_account:
            # Create a new account for the inviter
            inviter_account = Account(user_id=inviter_id, name="Default Account")
            db.add(inviter_account)
            db.commit()
            db.refresh(inviter_account)
        
        # Use the newly created account's account_id
        account_id = inviter_account.id


    # Step 4: Create the invitation in the database
    invitation = Invitation(
        account_id=account_id,
        invitee_email=invitation_data.invitee_email,
        inviter_id = inviter_id,
        role_id= invitation_data.role_id,
    )


    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    

    # Step 5: Send the invitation email
    token = generate_invitation_token(invitation_data.invitee_email, invitation.id, inviter_id)  # Generate a token for the invitation
    
    return await send_invitation_email(invitation_data.invitee_email, token)
    




async def accept_invitation(db: Session, token: str):


    
    
    # Step 1: Verify the invitation token
    try:
        decoded_token = jwt.decode(token, "CHIPPA", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    
    invitee_email = decoded_token.get("email")
    inviter_id = decoded_token.get("inviter_id")
    id = decoded_token.get("invitation_id")

    if not inviter_id or not invitee_email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Step 2: Check if the user already exists
    user = db.query(User).filter(User.email == invitee_email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")

    # Step 3: Get the associated account for the invitation
    invitation = db.query(Invitation).filter(Invitation.id == id).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found or expired")

    account = db.query(Account).filter(Account.id == invitation.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Step 4: Assign the role to the user
    role = db.query(Role).filter(Role.id == invitation.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Assign the user to the account with the appropriate role
    account_role = UserAccountRole(
        account_id=account.id,
        user_id=user.id,
        role_id=role.id
    )
    db.add(account_role)
    db.commit()

    # Step 5: Mark invitation as accepted
    invitation.status = "accepted"
    db.commit()

    return {"status": "Invitation accepted successfully", "user_id": user.id}
