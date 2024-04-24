from src.core.settings.base_config import BaseConfig
from src.core.settings.postgres import PostgresSettings
from src.api.auth.v1.settings.jwt_auth import JWTAuthSettings


class Settings(BaseConfig):
    MODE: str

    postgres_settings: PostgresSettings = PostgresSettings()
    jwt_auth_settings: JWTAuthSettings = JWTAuthSettings()


settings: Settings = Settings()
