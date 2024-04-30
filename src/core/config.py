from src.core.settings import BaseConfig, PostgresSettings, RedisSettings
from src.api.auth.settings.jwt_auth import JWTAuthSettings


class Settings(BaseConfig):
    MODE: str

    postgres_settings: PostgresSettings = PostgresSettings()
    jwt_auth_settings: JWTAuthSettings = JWTAuthSettings()
    redis_settings: RedisSettings = RedisSettings()


settings: Settings = Settings()
