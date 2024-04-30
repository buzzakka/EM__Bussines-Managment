from email.message import EmailMessage
from celery import Celery
import smtplib

from src.core.config import settings


celery: Celery = Celery('tasks', broker=settings.redis_settings.get_rd_url())

SMTP_HOST: str = settings.smtp_settings.SMTP_HOST
SMTP_PORT: str = settings.smtp_settings.SMTP_PORT
SMTP_USER: str = settings.smtp_settings.SMTP_USER
SMTP_PASS: str = settings.smtp_settings.SMTP_PASSWORD


def get_invite_token_template(
    invite_token: str,
    to_email: str
):
    email = EmailMessage()
    email['Subject'] = 'Код подтверждения'
    email['From'] = settings.smtp_settings.SMTP_USER
    email['To'] = to_email

    email.set_content(
        '<div>'
        '<h1>Код подтверждения регистрации</h1>'
        f'<p>{invite_token}</p>'
        '</div>',
        subtype='html'
    )

    return email


@celery.task
def send_invite_token(email: str, invite_token: str):
    with smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        message: EmailMessage = get_invite_token_template(
            invite_token=invite_token,
            email=email
        )
        server.send_message(message)

