"""Module for the settings of this application."""
import os

import tomli
from pydantic import BaseModel, Field

ENV_SETTINGS_FILE = "KWAI_SETTINGS_FILE"


class SettingsException(Exception):
    """Raised when a problem occurred while loading the settings."""


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
    ssl: bool = True
    tls: bool = True
    user: str | None = None
    password: str | None = None
    address: str = Field(alias="from")


class RedisSettings(BaseModel):
    """Settings for redis."""

    host: str
    port: int | None
    logger: LoggerSettings | None = None


class SecuritySettings(BaseModel):
    """Setting or security."""

    access_token_expires_in: int
    refresh_token_expires_in: int
    jwt_algorithm: str
    jwt_secret: str
    jwt_refresh_secret: str
    cors_origin: list[str] = []


class TemplateSettings(BaseModel):
    """Settings for template."""

    path: str


class Settings(BaseModel):
    """Class with settings."""

    security: SecuritySettings

    template: TemplateSettings

    logger: LoggerSettings | None = None

    db: DatabaseSettings

    website: WebsiteSettings

    email: EmailSettings

    redis: RedisSettings


def get_settings() -> Settings:
    """Dependency function for creating the Settings instance.

    The settings are cached with lru_cache, which means the file is only loaded ounce.

    :raises:
        core.settings.SettingsException: Raised when the env variable is not set, or
            when the file
            can't be read.
    """
    if ENV_SETTINGS_FILE in os.environ:
        settings_file = os.environ.get(ENV_SETTINGS_FILE, "")
        try:
            with open(settings_file, mode="rb") as file_handle:
                return Settings.parse_obj(tomli.load(file_handle))
        except OSError as exc:
            raise SettingsException(f"Could not load {settings_file}") from exc
    raise SettingsException(
        f"{ENV_SETTINGS_FILE} should be set as environment variable"
    )
