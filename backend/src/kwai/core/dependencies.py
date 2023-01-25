"""
Module that defines a dependency injector container.

Auto-wiring is avoided. It should be clear why and when a class is loaded.
"""
import dramatiq.brokers.rabbitmq

from lagom import Container, dependency_definition, ExplicitContainer, Singleton

from kwai.core.db import Database
from kwai.core.events import Bus, DramatiqBus
from kwai.core.mail import Mailer
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import Settings, get_settings
from kwai.core.template import TemplateEngine
from kwai.core.template.jinja2_engine import Jinja2Engine

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
def create_mailer(c: Container) -> Mailer:
    """Creates the mailer."""
    mailer = SmtpMailer(c[Settings].email.host, c[Settings].email.port)
    mailer.connect(c[Settings].email.user, c[Settings].email.password)
    return mailer


@dependency_definition(container)
def create_event_bus(c: Container) -> Bus:
    """Creates the event bus."""
    broker = dramatiq.brokers.rabbitmq.RabbitmqBroker(
        url=c[Settings].broker.url + "/" + c[Settings].broker.name
    )
    dramatiq.set_broker(broker)
    return DramatiqBus(broker)
