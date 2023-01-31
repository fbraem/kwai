"""
Module that defines a dependency injector container.

Auto-wiring is avoided. It should be clear why and when a class is loaded.
"""
from typing import Iterator

import dramatiq.brokers.rabbitmq
from lagom import Container, dependency_definition, ExplicitContainer, Singleton

from kwai.core.db.database import Database
from kwai.core.events.bus import Bus
from kwai.core.events.dramatiq_bus import DramatiqBus
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import Settings, get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine

container = ExplicitContainer()

container[Settings] = Singleton(lambda: get_settings())
container[TemplateEngine] = lambda c: Jinja2Engine(
    c[Settings].template.path, website=c[Settings].website
)


@dependency_definition(container)
def create_database(c: Container) -> Database:
    database = Database(c[Settings].db)
    database.connect()
    return database


@dependency_definition(container)
def create_mailer(c: Container) -> Iterator[Mailer]:
    """Creates the mailer."""
    mailer = SmtpMailer(
        host=c[Settings].email.host,
        port=c[Settings].email.port,
        tls=c[Settings].email.tls,
    )
    try:
        mailer.connect()
        if c[Settings].email.user:
            mailer.login(c[Settings].email.user, c[Settings].email.password)
        yield mailer
    finally:
        mailer.disconnect()


@dependency_definition(container)
def create_event_bus(c: Container) -> Bus:
    """Creates the event bus."""
    broker = dramatiq.brokers.rabbitmq.RabbitmqBroker(
        url=c[Settings].broker.url + "/" + c[Settings].broker.name
    )
    dramatiq.set_broker(broker)
    return DramatiqBus(broker)
