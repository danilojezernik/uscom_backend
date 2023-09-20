from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.domain.mail import Email
from src.services import emails, db
from src.template import email

router = APIRouter()


@router.post("/send-email")
async def send_email(emailing: Email, background_tasks: BackgroundTasks):
    # Check for white spaces in name and surname
    if ' ' in emailing.name or len(emailing.name) < 3:
        raise HTTPException(status_code=400, detail="There are white spaces in name")

    if ' ' in emailing.surname or len(emailing.surname) < 3:
        raise HTTPException(status_code=400, detail="There are white spaces in surname")

    # Check if email exists
    if not emails.exists(emailing.email):
        raise HTTPException(status_code=400, detail="Email not existing")

    body = email.html(name=emailing.name, surname=emailing.surname, email=emailing.email, content=emailing.content)

    # Send the email in the background
    background_tasks.add_task(send_email_background, email_to=emailing.email, subject='USCOM | You got email ♥', body=body)

    email_data = {
        "name": emailing.name,
        "surname": emailing.surname,
        "email": emailing.email,
        "content": emailing.content
    }

    # Insert email data into the database
    db.api.email.insert_one(email_data)

    return {"message": "Message was sent"}


def send_email_background(email_to: str, subject: str, body: str):
    try:
        email_sent = emails.send(email_to=email_to, subject=subject, body=body)
        if not email_sent:
            raise Exception("Email not sent")
    except Exception as e:
        # Handle any exceptions that occur during email sending
        # You might want to log the error for debugging purposes
        print(f"Error sending email: {str(e)}")
