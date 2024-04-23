from src.core.settings.base_config import BaseConfig
from src.core.settings.postgres import PostgresSettings


class Settings(BaseConfig):
    MODE: str

    postgres_settings: PostgresSettings = PostgresSettings()


settings: Settings = Settings()
