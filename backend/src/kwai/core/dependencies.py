"""Module that defines a dependency injector container.

Auto-wiring is avoided. It should be clear why and when a class is loaded.
"""

from lagom import Container, ExplicitContainer, Singleton, dependency_definition
from redis.asyncio import Redis

from kwai.core.db.database import Database
from kwai.core.events.bus import Bus
from kwai.core.events.redis_bus import RedisBus
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import Settings, get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine

container = ExplicitContainer()

container[Settings] = Singleton(get_settings)
container[TemplateEngine] = lambda c: Jinja2Engine(
    c[Settings].template.path, website=c[Settings].website
)


@dependency_definition(container)
def create_database(c: Container) -> Database:
    """Create the database dependency."""
    database = Database(c[Settings].db)
    return database


@dependency_definition(container)
def create_mailer(c: Container) -> Mailer:
    """Create the mailer dependency."""
    mailer = SmtpMailer(
        host=c[Settings].email.host,
        port=c[Settings].email.port,
        ssl_=c[Settings].email.ssl,
        tls=c[Settings].email.tls,
    )
    mailer.connect()
    if c[Settings].email.user:
        mailer.login(c[Settings].email.user, c[Settings].email.password)
    return mailer


@dependency_definition(container)
def create_redis(c: Container) -> Redis:
    """Create the redis dependency."""
    redis_settings = c[Settings].redis
    return Redis(
        host=redis_settings.host,
        port=redis_settings.port or 6379,
        password=redis_settings.password,
    )


@dependency_definition(container)
def create_event_bus(c: Container) -> Bus:
    """Create the event bus dependency."""
    return RedisBus(c[Redis])
