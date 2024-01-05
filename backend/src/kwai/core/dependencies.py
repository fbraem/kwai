"""Module that defines a dependency injector container.

Auto-wiring is avoided. It should be clear why and when a class is loaded.
"""
from typing import AsyncGenerator

from fastapi import Depends

from kwai.core.db.database import Database
from kwai.core.settings import get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine


def get_template_engine(settings=Depends(get_settings)) -> TemplateEngine:
    """Create the template engine dependency."""
    return Jinja2Engine(settings.template.path, website=settings.website)


async def create_database(
    settings=Depends(get_settings),
) -> AsyncGenerator[Database, None]:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()
