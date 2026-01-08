import os
from pydantic import (
    field_validator,
    Field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class Settings(BaseSettings):
    """Settings for the application"""

    ENVIROMENT: Environment = Field(
        default=Environment.DEV,
        description="Environment setting (dev, prod, test)",
    )

    # ==== OPEN ROUTER ====
    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key",
        min_length=10,
    )
    OPENROUTER_MODEL_NAME: str = Field(
        default="anthropic/claude-3-haiku",
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

    # === VALIDATORS ===
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        """Validate the correctness of the log level"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of: {', '.join(allowed)}")
        return v.upper()

    @field_validator("ENVIROMENT", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Convert a string to an Environment enum"""
        if isinstance(v, str):
            v = v.lower()
            if v not in [e.value for e in Environment]:
                raise ValueError(
                    f"Environment must be one of: {', '.join([e.value for e in Environment])}"
                )
        return v

    @model_validator(mode="before")
    @classmethod
    def set_test_enviroment(cls, data):
        """Set defaults if env is for testing"""
        current_env = os.getenv("ENVIRONMENT", "dev").lower()

        if isinstance(data, dict) and "ENVIROMENT" in data:
            current_env = str(data["ENVIROMENT"]).lower()

            if current_env == "test":
                if isinstance(data, dict):
                    if not data.get("OPENROUTER_API_KEY"):
                        data["OPENROUTER_API_KEY"] = "test_dummy_key_1234567890"

        return data

    @model_validator(mode="after")
    def set_environment_defaults(self):
        """Set default values based on the environment"""
        if self.ENVIROMENT == Environment.PROD:
            self.DEBUG_MODE = False  # Always False in production
            if self.LOG_LEVEL == "DEBUG":
                self.LOG_LEVEL = "INFO"  # Minimum INFO in production
        return self

    # === PROPERTIES ====
    @property
    def is_dev(self) -> bool:
        """Check if environment is dev"""
        return self.ENVIROMENT == Environment.DEV

    @property
    def is_prod(self) -> bool:
        """Check if environment is prod"""
        return self.ENVIROMENT == Environment.PROD

    @property
    def is_test(self) -> bool:
        """Check if environment is test"""
        return self.ENVIROMENT == Environment.TEST

    model_config = SettingsConfigDict(
        env_file=(".env.test" if os.getenv("ENVIRONMENT") == "test" else ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings
