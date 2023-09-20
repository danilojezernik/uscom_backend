from validate_email import validate_email

from email.message import EmailMessage
import smtplib

from src import env


def exists(email: str) -> bool:
    is_valid = validate_email(email_address=email, check_format=True)
    return is_valid


def send(email_to: str, subject: str, body: str) -> bool:
    em = EmailMessage()
    em['From'] = email_to
    em['To'] = env.EMAIL_SENDER
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(env.EMAIL_SENDER, env.EMAIL_PASSWORD)
        sendemail = smtp.sendmail(env.EMAIL_SENDER, email_to, em.as_string())
        if not sendemail:
            return True
        else:
            return False
