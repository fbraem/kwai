"""Module for the settings of this application."""

import os
import tomllib
from functools import lru_cache
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, Field

ENV_SETTINGS_FILE = "KWAI_SETTINGS_FILE"


class SettingsException(Exception):
    """Raised when a problem occurred while loading the settings."""


class ApplicationSettingsModel(BaseModel):
    """Settings that apply to all applications."""

    default: bool = False  # Set to true for selecting the default application
    vite_server: str | None = None  # Only required in development.
    variables: dict[str, Any] | None = None


class AuthenticationApplicationSettings(ApplicationSettingsModel):
    """Settings for the auth application."""

    name: Literal["auth"]


class AuthorApplicationSettings(ApplicationSettingsModel):
    """Settings for the author application."""

    name: Literal["author"]


class ClubApplicationSettings(ApplicationSettingsModel):
    """Settings for the club application."""

    name: Literal["club"]


class CoachApplicationSettings(ApplicationSettingsModel):
    """Settings for the portal application."""

    name: Literal["coach"]


class PortalApplicationSettings(ApplicationSettingsModel):
    """Settings for the portal application."""

    name: Literal["portal"]


Application = Annotated[
    Union[
        AuthenticationApplicationSettings,
        AuthorApplicationSettings,
        ClubApplicationSettings,
        CoachApplicationSettings,
        PortalApplicationSettings,
    ],
    Field(discriminator="name"),
]


class FrontendSettings(BaseModel):
    """Settings for the frontend."""

    test: bool = False
    path: str
    apps: list[Application]


class FilesSettings(BaseModel):
    """Settings for files (upload)."""

    path: str


class AdminSettings(BaseModel):
    """Settings for the administrator of the website."""

    name: str
    email: str


class WebsiteSettings(BaseModel):
    """Settings about the website."""

    url: str
    email: str
    name: str
    copyright: Optional[str] = None
    admin: Optional[AdminSettings] = None


class DatabaseSettings(BaseModel):
    """Settings for the database connection."""

    host: str
    name: str
    user: str
    password: str


class CORSSettings(BaseModel):
    """Settings for configuring CORS."""

    origins: list[str] = Field(default_factory=list)
    methods: list[str] = Field(default_factory=lambda: ["*"])
    headers: list[str] = Field(default_factory=lambda: ["*"])


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
    """Settings for Redis."""

    host: str = "127.0.0.1"
    port: int = 6379
    password: str | None = None
    logger: LoggerSettings | None = None


class SecuritySettings(BaseModel):
    """Setting or security."""

    access_token_expires_in: int = 60  # minutes
    refresh_token_expires_in: int = 43200  # 30 days
    jwt_algorithm: str = "HS256"
    jwt_secret: str
    jwt_refresh_secret: str


class Settings(BaseModel):
    """Class with settings."""

    frontend: FrontendSettings

    files: FilesSettings

    security: SecuritySettings

    logger: LoggerSettings | None = None

    cors: CORSSettings | None = None

    db: DatabaseSettings

    website: WebsiteSettings

    email: EmailSettings

    redis: RedisSettings


@lru_cache
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
                return Settings.model_validate(tomllib.load(file_handle))
        except OSError as exc:
            raise SettingsException(f"Could not load {settings_file}") from exc
    raise SettingsException(
        f"{ENV_SETTINGS_FILE} should be set as environment variable"
    )
