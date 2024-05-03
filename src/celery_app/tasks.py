from email.message import EmailMessage
import smtplib

from src.celery_app.celery_worker import celery

from src.core.config import settings


_SMTP_HOST: str = settings.smtp_settings.SMTP_HOST
_SMTP_PORT: str = settings.smtp_settings.SMTP_PORT
_SMTP_USER: str = settings.smtp_settings.SMTP_USER
_SMTP_PASS: str = settings.smtp_settings.SMTP_PASSWORD


@celery.task(name='send_invite_token')
def send_invite_token(to_email: str, invite_token: str):
    message = EmailMessage()
    message['Subject'] = 'Код подтверждения'
    message['From'] = settings.smtp_settings.SMTP_USER
    message['To'] = to_email

    message.set_content(
        '<div>'
        '<h1>Код подтверждения регистрации</h1>'
        f'<p>{invite_token}</p>'
        '</div>',
        subtype='html'
    )

    _send_message(message)


@celery.task(name='send_invite_link')
def send_invite_link(to_email: str, invite_link: str):
    message = EmailMessage()
    message['Subject'] = f'Приглашение'
    message['From'] = settings.smtp_settings.SMTP_USER
    message['To'] = to_email

    message.set_content(
        '<div>'
        f'<p>Ссылка для подтверждения регистрации: <a href="{invite_link}">ссылка</a>.</p>'
        '</div>',
        subtype='html'
    )

    _send_message(message)


def _send_message(message: EmailMessage):
    with smtplib.SMTP_SSL(host=_SMTP_HOST, port=_SMTP_PORT) as server:
        server.login(_SMTP_USER, _SMTP_PASS)
        server.send_message(message)
