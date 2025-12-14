import os
from pydantic import (
    BaseSettings,
    SettingsConfigDict,
    field_validator,
    Field,
    model_validator,
)
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TESTING = "test"


class Settings(BaseSettings):
    """Settings for the application"""

    environment: Environment = Field(
        default=Environment.DEV,
        description="Environment setting (dev, prod, test)",
    )

    # ==== OPEN ROUTER ====
    openrouter_api_key: str = Field(
        ...,
        description="OpenRouter API key",
        min_length=10,
    )
    openrouter_model_name: str = Field(
        ...,
        description="OpenRouter model name",
    )

    # ==== SITE ====
    your_site_url: str = Field(
        default="https://site_url_default.com",
        description="Site URL for rankings on openrouter.ai.",
    )
    your_site_name: str = Field(
        default="Default site name",
        description="Site title for rankings on openrouter.ai.",
    )

    # ==== OTHER ====
    debug: bool = Field(default=False, description="Debug mode")

    log_level: str = Field(default="INFO", description="Logging level")

    # === VALIDATORS ===
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate the correctness of the log level"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of: {', '.join(allowed)}")
        return v.upper()

    @field_validator("environment", mode="before")
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

    @model_validator(mode="after")
    def set_environment_defaults(self):
        """Set default values based on the environment"""
        if self.environment == Environment.PROD:
            self.debug = False  # Always False in production
            if self.log_level == "DEBUG":
                self.log_level = "INFO"  # Minimum INFO in production
        return self

    # === PROPERTIES ====
    @property
    def is_dev(self) -> bool:
        """Check if environment is dev"""
        return self.environment == Environment.DEV

    @property
    def is_prod(self) -> bool:
        """Check if environment is prod"""
        return self.environment == Environment.PROD

    @property
    def is_test(self) -> bool:
        """Check if environment is test"""
        return self.environment == Environment.TEST

    model_config = SettingsConfigDict(
        env_file=(
            ".env"
            if Environment(os.getenv("ENVIRONMENT", "dev")) == Environment.DEV
            else None
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings
