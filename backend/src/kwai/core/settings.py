"""Module for the settings of this application."""
import logging
from functools import lru_cache

from pydantic import BaseSettings, BaseModel


class DatabaseSettings(BaseModel):
    """Settings for the database connection."""

    host: str
    name: str
    user: str
    password: str


class LoggerSettings(BaseModel):
    file: str = "kwai.log"
    level: str = "DEBUG"
    retention: str = "7 days"
    rotation: str = "1 day"


class Settings(BaseSettings):
    """Class with settings."""

    access_token_expires_in: int
    refresh_token_expires_in: int
    jwt_algorithm: str
    jwt_secret: str
    jwt_refresh_secret: str

    logger: LoggerSettings | None = None

    db: DatabaseSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


@lru_cache()
def get_settings():
    """Dependency function for creating the Settings instance."""
    return Settings()
