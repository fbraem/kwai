"""Module that defines the dependencies for events."""

import contextlib
from typing import AsyncGenerator

import inject
from inject import Binder

from kwai.core.db.database import Database
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import Settings, get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine


@contextlib.asynccontextmanager
@inject.autoparams()
async def create_database(settings: Settings) -> AsyncGenerator[Database, None]:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()


@inject.autoparams()
def create_template_engine(settings: Settings) -> TemplateEngine:
    """Create the template engine dependency."""
    return Jinja2Engine(website=settings.website)


@inject.autoparams()
def create_mailer(settings: Settings) -> Mailer:
    """Create the mailer dependency."""
    mailer = SmtpMailer(
        host=settings.email.host,
        port=settings.email.port,
        ssl_=settings.email.ssl,
        tls=settings.email.tls,
    )
    mailer.connect()
    if settings.email.user:
        mailer.login(settings.email.user, settings.email.password)
    return mailer


def _configure_dependencies(binder: Binder):
    binder.bind_to_provider(Settings, get_settings)
    binder.bind_to_provider(Database, create_database)
    binder.bind_to_provider(TemplateEngine, create_template_engine)
    binder.bind_to_provider(Mailer, create_mailer)


def configure():
    """Configure the dependency injection system.

    Note: only use dependency injection for injecting dependencies into tasks. A task
    method is used as entry from outside. DI makes it possible to pass dependencies to
    this method. Regular constructors should be used for injecting dependencies into
    domain classes.
    """
    inject.configure(_configure_dependencies)
