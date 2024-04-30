from src.core.settings.base_config import BaseConfig


class SMTPSettings(BaseConfig):
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str
