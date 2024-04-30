from src.core.settings.base_config import BaseConfig


class RedisSettings(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: str

    def get_rd_url(self) -> str:
        """Получение URL Redis."""
        url: str = f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'
        return url
