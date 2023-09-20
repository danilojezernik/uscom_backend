from fastapi import APIRouter, HTTPException

from src.domain.mail import Email
from src.services import emails, db
from src.template import email

router = APIRouter()


# USER SENDING EMAIL TO AUTHOR
@router.post("/send-email")
async def sign_in(emailing: Email):
    try:
        if ' ' in emailing.name or len(emailing.name) < 3:
            return HTTPException(status_code=400, detail="There are white spaces in name")

        if ' ' in emailing.surname or len(emailing.surname) < 3:
            return HTTPException(status_code=400, detail="There are white spaces in surname")

        if not emails.exists(emailing.email):
            return HTTPException(status_code=400, detail="Email not existing")

        body = email.html(name=emailing.name, surname=emailing.surname, email=emailing.email, content=emailing.content)

        # Wait for the email to be sent
        email_sent = await emails.send(email_to=emailing.email, subject='USCOM | You got email ♥', body=body)

        if not email_sent:
            return HTTPException(status_code=500, detail="Email not sent")

        email_data = {
            "name": emailing.name,
            "surname": emailing.surname,
            "email": emailing.email,
            "content": emailing.content
        }

        db.api.email.insert_one(email_data)

        return {"message": "Message was sent"}

    except Exception as e:
        return HTTPException(status_code=500, detail="An error occurred while processing the request")
