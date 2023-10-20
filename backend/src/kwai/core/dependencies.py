"""Module that defines a dependency injector container.

Auto-wiring is avoided. It should be clear why and when a class is loaded.
"""
from fastapi import Depends
from redis.asyncio import Redis

from kwai.core.db.database import Database
from kwai.core.events.bus import Bus
from kwai.core.events.redis_bus import RedisBus
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine


def get_template_engine(settings=Depends(get_settings)) -> TemplateEngine:
    """Create the template engine dependency."""
    return Jinja2Engine(settings.template.path, website=settings.website)


async def create_database(settings=Depends(get_settings)) -> Database:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()


def create_mailer(settings=Depends(get_settings)) -> Mailer:
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


def create_redis(settings=Depends(get_settings)) -> Redis:
    """Create the redis dependency."""
    redis_settings = settings.redis
    return Redis(
        host=redis_settings.host,
        port=redis_settings.port or 6379,
        password=redis_settings.password,
    )


def create_event_bus(redis=Depends(create_redis)) -> Bus:
    """Create the event bus dependency."""
    return RedisBus(redis)
