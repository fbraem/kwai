"""Module that defines dependencies for the CLI program."""
import contextlib
from typing import AsyncGenerator

import inject
from inject import Binder
from redis.asyncio import Redis

from kwai.core.db.database import Database
from kwai.core.settings import Settings, get_settings


@contextlib.asynccontextmanager
@inject.autoparams()
async def create_database(settings: Settings) -> AsyncGenerator[Database, None]:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()


@contextlib.asynccontextmanager
@inject.autoparams()
async def create_redis(settings: Settings) -> AsyncGenerator[Redis, None]:
    """Create the Redis dependency."""
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
    )
    try:
        yield redis
    finally:
        await redis.aclose()


def _configure_dependencies(binder: Binder):
    binder.bind_to_provider(Settings, get_settings)
    binder.bind_to_provider(Database, create_database)
    binder.bind_to_provider(Redis, create_redis)


def configure():
    """Configure the dependency injection system for the CLI program."""
    inject.configure(_configure_dependencies)
