from typing import Literal
from pathlib import Path
from pydantic import SecretStr, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path.cwd().parent.parent

class Settings(BaseSettings):
    """Загрузка переменных среды"""
    # Bot
    BOT_TOKEN: SecretStr = SecretStr('')

    # AI
    AI_PROVIDER: Literal["gigachat", "yandexgpt"] = "gigachat"
    AI_MODEL: str = "GigaChat"
    AI_API_KEY: SecretStr = SecretStr('')
    AI_TEMP: float = Field(default=0.0, ge=0.0, le=1.0)

    # Database
    DATABASE_URL: PostgresDsn = PostgresDsn('postgresql://user:pass@localhost')
    DATABASE_POOL_SIZE: int = Field(default=20, ge=1, le=100)
    DATABASE_ECHO: bool = False

    # DEBUG
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=ROOT/".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

ENV = Settings()
