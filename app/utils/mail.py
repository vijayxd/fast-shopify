# app/utils.py

from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Configure email client
conf = ConnectionConfig(
    MAIL_USERNAME = "support@gaga.3djungle.io",
    MAIL_PASSWORD = "Moni9391!",
    MAIL_FROM = "support@gaga.3djungle.io",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.hostinger.com",  # Use your email service provider
    MAIL_STARTTLS = False,  # Correct field name
    MAIL_SSL_TLS = True,  # Correct field name
    USE_CREDENTIALS = True,
    # TEMPLATE_FOLDER = "./templates",
)


# Send invitation email
async def send_invitation_email(email: str, token: str):
    message = MessageSchema(
        subject="You have been invited to join our platform",
        recipients=[email],  # List of recipients
        body=f"Click the link to accept the invitation: http://192.168.74.100:8000/accept-invitation?token={token}",
        subtype="html"
    )

    fm = FastMail(conf)
    
    try:
            # Send the email
        await fm.send_message(message)
        return {"message": "Invitation email sent successfully"}
    except Exception as e:
            print(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send verification email.")
    

# Send verification email
async def send_verification_email(email: str, token: str):
    message = MessageSchema(
        subject="Please verify your email",
        recipients=[email],  # List of recipients
        body=f"Click the link to verify your email: http://192.168.74.100:8000/users/verify-email?token={token}",
        subtype="html"
    )
    
    fm = FastMail(conf)
    
    try:
            # Send the email
        await fm.send_message(message)
    except Exception as e:
            print(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send verification email.")

async def send_test_email(to_email: str):
    message = MessageSchema(
        subject="Test Email",
        recipients=[to_email],
        body="This is a test email to verify email functionality.",
        subtype="html",
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"message": "Test email sent successfully"}
    except HTTPException as e:
        return {"error": str(e)}