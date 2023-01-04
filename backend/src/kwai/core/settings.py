"""Module for the settings of this application."""
from functools import lru_cache

from pydantic import BaseSettings, BaseModel, Field


class WebsiteSettings(BaseModel):
    """Settings about the website."""

    url: str
    email: str
    name: str


class DatabaseSettings(BaseModel):
    """Settings for the database connection."""

    host: str
    name: str
    user: str
    password: str


class LoggerSettings(BaseModel):
    """Settings for the logger."""

    file: str = "kwai.log"
    level: str = "DEBUG"
    retention: str = "7 days"
    rotation: str = "1 day"


class EmailSettings(BaseModel):
    """Settings for sending emails."""

    host: str
    port: int
    user: str
    password: str
    address: str = Field(alias="from")


class Settings(BaseSettings):
    """Class with settings."""

    access_token_expires_in: int
    refresh_token_expires_in: int
    jwt_algorithm: str
    jwt_secret: str
    jwt_refresh_secret: str

    template_path: str

    cors_origin: list[str] = []

    logger: LoggerSettings | None = None

    db: DatabaseSettings

    website: WebsiteSettings

    email: EmailSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


@lru_cache()
def get_settings():
    """Dependency function for creating the Settings instance."""
    return Settings()
