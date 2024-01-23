"""Module that defines dependencies for the CLI program."""
import contextlib
from typing import AsyncGenerator

import inject
from inject import Binder

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


def _configure_dependencies(binder: Binder):
    binder.bind_to_provider(Settings, get_settings)
    binder.bind_to_provider(Database, create_database)


def configure():
    """Configure the dependency injection system for the CLI program."""
    inject.configure(_configure_dependencies)
