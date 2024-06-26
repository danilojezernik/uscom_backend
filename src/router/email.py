from fastapi import APIRouter, HTTPException

from src.domain.mail import Email
from src.services import emails, db
from src.template import email

router = APIRouter()


# USER SENDING EMAIL TO AUTHOR
@router.post("/send-email")
async def sign_in(emailing: Email):
    body = email.html(name=emailing.name, surname=emailing.surname, email=emailing.email, content=emailing.content)

    if not emails.send(email_to=emailing.email, subject='USCOM | You got email ♥', body=body):
        return HTTPException(status_code=500, detail="Email not sent")

    email_data = {
        "name": emailing.name,
        "surname": emailing.surname,
        "email": emailing.email,
        "content": emailing.content
    }

    db.api.email.insert_one(email_data)

    return {"message": "Message was sent"}
