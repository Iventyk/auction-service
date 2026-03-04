from functools import lru_cache
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    app_port: int = 8000

    model_config = SettingsConfigDict(extra="ignore")

    @property
    def database_url(self) -> str:
        """
        Build async database URL.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached settings instance
    with environment variables explicitly passed.
    """
    return Settings(
        postgres_db=os.getenv("POSTGRES_DB", ""),
        postgres_user=os.getenv("POSTGRES_USER", ""),
        postgres_password=os.getenv("POSTGRES_PASSWORD", ""),
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", 5432)),
        app_port=int(os.getenv("APP_PORT", 8000)),
    )
