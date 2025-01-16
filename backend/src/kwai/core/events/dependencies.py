"""Module that defines the dependencies for events."""

from typing import AsyncGenerator

from fast_depends import Depends

from kwai.core.db.database import Database
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import Settings, get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine


async def create_database(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator[Database, None]:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()


def create_template_engine(
    settings: Settings = Depends(get_settings),
) -> TemplateEngine:
    """Create the template engine dependency."""
    return Jinja2Engine(website=settings.website)


def create_mailer(settings: Settings = Depends(get_settings)) -> Mailer:
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
