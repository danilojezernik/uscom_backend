from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.domain.mail import Email
from src.services import emails, db
from src.template import email
import asyncio

router = APIRouter()


# This timeout decorator allows setting a timeout for the request processing
def timeout(seconds: int):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
                return result
            except asyncio.TimeoutError:
                raise HTTPException(status_code=504, detail="Request processing timed out")

        return wrapper

    return decorator


@router.post("/send-email")
@timeout(30)  # Set the timeout for request processing (e.g., 30 seconds)
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
    background_tasks.add_task(
        emails.send, email_to=emailing.email, subject='USCOM | You got email ♥', body=body
    )

    email_data = {
        "name": emailing.name,
        "surname": emailing.surname,
        "email": emailing.email,
        "content": emailing.content
    }

    # Insert email data into the database
    db.api.email.insert_one(email_data)

    return {"message": "Message was sent"}
