import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


def _prepare_env_defaults() -> dict:
    """Prepare default values based on environment."""
    defaults = {}
    env = os.getenv("ENVIROMENT", "dev").lower()

    if env == "prod":
        defaults["DEBUG_MODE"] = False
        if os.getenv("LOG_LEVEL", "").upper() == "DEBUG":
            defaults["LOG_LEVEL"] = "INFO"  # No Debug level in prod

    return defaults


class Settings(BaseSettings):
    """Settings for the application"""

    ENVIROMENT: Literal["dev", "prod", "test"] = Field(
        default="dev",
        description="Environment setting (dev, prod, test)",
    )

    # ==== OPEN ROUTER ====
    OPENROUTER_API_KEY: str = Field(
        description="OpenRouter API key",
        min_length=10,
    )
    OPENROUTER_MODEL_NAME: str = Field(
        description="OpenRouter model name",
    )

    # ==== SITE ====
    BASE_URL: str = Field(
        default="http://127.0.0.1:8000/",
        description="Your site base URL",
    )
    API_URL: str = Field(
        default="http://127.0.0.1:8000/api/", description="Your site API URL"
    )
    SITE_NAME: str = Field(
        default="Default site name",
        description="Site title for rankings on openrouter.ai.",
    )

    # ==== OTHER ====
    DEBUG_MODE: bool = Field(default=False, description="Debug mode")

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    model_config = SettingsConfigDict(
        env_file=(".env.test" if os.getenv("ENVIROMENT") == "test" else ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    """Get settings instance"""
    return Settings(**_prepare_env_defaults())


settings = get_settings()
