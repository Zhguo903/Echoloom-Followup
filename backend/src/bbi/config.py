from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BBI_", env_file=".env", extra="ignore")

    env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./var/bbi.sqlite3"
    default_provider: str = "mock"
    default_model: str = "mock-v1"
    admin_token: str = "change-me-locally"
    study_mode: bool = False
    store_raw_provider_outputs: bool = False
    log_prompt_content: bool = False
    cors_origins: str = "http://localhost:5173"
    max_input_chars: int = Field(default=8_000, ge=100, le=100_000)

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
