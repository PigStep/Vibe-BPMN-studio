import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pydantic import model_validator


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

    PROVIDER_NAME: Literal["openrouter", "gemini"]

    # ==== PROVIDER ====
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL_NAME: str | None = None

    # === GEMENI ====
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL_NAME: str | None = None

    # ==== SITE ====
    BASE_URL: str | None = None
    API_URL: str | None = None
    SITE_NAME: str | None = None

    # ==== OTHER ====
    DEBUG_MODE: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # ==== VALIDATION ====
    @model_validator(mode="after")
    def validate_provider_choosen(self):
        """Check if API and model name set for choosen provider"""
        if self.PROVIDER_NAME == "openrouter":
            if self.OPENROUTER_API_KEY is None:
                raise ValueError("OPENROUTER_API_KEY is not set")
            if self.OPENROUTER_MODEL_NAME is None:
                raise ValueError("OPENROUTER_MODEL_NAME is not set")
        elif self.PROVIDER_NAME == "gemini":
            if self.GEMINI_API_KEY is None:
                raise ValueError("GEMINI_API_KEY is not set")
            if self.GEMINI_MODEL_NAME is None:
                raise ValueError("GEMINI_MODEL_NAME is not set")
        return self

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
