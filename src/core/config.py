from celery import Celery
from src.core.settings import BaseConfig, PostgresSettings, RedisSettings, SMTPSettings
from src.api.auth.settings.jwt_auth import JWTAuthSettings


class Settings(BaseConfig):
    MODE: str

    postgres_settings: PostgresSettings = PostgresSettings()
    jwt_auth_settings: JWTAuthSettings = JWTAuthSettings()
    redis_settings: RedisSettings = RedisSettings()
    smtp_settings: SMTPSettings = SMTPSettings()


settings: Settings = Settings()

celery: Celery = Celery('tasks', broker=settings.redis_settings.get_rd_url())
