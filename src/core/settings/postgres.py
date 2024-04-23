from src.core.settings.base_config import BaseConfig


class PostgresSettings(BaseConfig):
    PG_NAME: str
    PG_HOST: str
    PG_PORT: str
    PG_USER: str
    PG_PASS: str

    def get_pg_url(self) -> str:
        """Получение URL postgres."""
        url: str = f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}'
        return url