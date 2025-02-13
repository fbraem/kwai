"""Module for sharing fixtures in this module."""

import asyncio

from typing import AsyncGenerator, AsyncIterator, Iterator

import pytest

from redis.asyncio import Redis

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.password import Password
from kwai.core.events.publisher import Publisher
from kwai.core.events.redis_bus import RedisBus
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipient, Recipients
from kwai.core.settings import get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


@pytest.fixture(scope="session")
def event_loop():
    """Fixture for the event loop.

    Without this fixture some async test methods fail.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def database():
    """Fixture for getting a database."""
    db = Database(get_settings().db)
    yield db
    await db.close()


@pytest.fixture(scope="session")
async def redis() -> AsyncGenerator[Redis, None]:
    """Fixture for a redis instance."""
    settings = get_settings()
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
    )
    yield redis
    await redis.aclose()


@pytest.fixture(scope="session")
async def bus(redis: Redis) -> RedisBus:
    """Fixture for a message bus."""
    return RedisBus(redis)


@pytest.fixture(scope="module")
async def publisher(bus: RedisBus) -> Publisher:
    """Fixture for a publisher."""
    return bus


@pytest.fixture(scope="module")
def mailer() -> Iterator[Mailer]:
    """Fixture for getting a mailer."""
    from kwai.core.mail.smtp_mailer import SmtpMailer

    settings = get_settings()
    mailer = SmtpMailer(
        host=settings.email.host, port=settings.email.port, tls=settings.email.tls
    )
    try:
        mailer.connect()
        if settings.email.user:
            mailer.login(settings.email.user, settings.email.password)
        yield mailer
    finally:
        mailer.disconnect()


@pytest.fixture
def recipients() -> Recipients:
    """Fixture for getting recipients."""
    return Recipients(
        from_=Recipient(email=EmailAddress("webmaster@kwai.com"), name="Webmaster"),
        to=[Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")],
    )


@pytest.fixture(scope="module")
def template_engine() -> TemplateEngine:
    """Fixture for getting a template engine."""
    settings = get_settings()
    return Jinja2Engine(website=settings.website)


@pytest.fixture(scope="module")
async def user_account(database: Database) -> AsyncIterator[UserAccountEntity]:
    """Fixture that provides a user account in the database.

    The user will be removed again after running the tests.
    """
    user_account = UserAccountEntity(
        user=UserEntity(
            email=EmailAddress("jigoro.kano@kwai.com"),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
        password=Password.create_from_string("Nage-waza/1882"),
    )
    repo = UserAccountDbRepository(database)

    async with UnitOfWork(database):
        user_account = await repo.create(user_account)

    yield user_account

    async with UnitOfWork(database):
        await repo.delete(user_account)


@pytest.fixture(scope="module")
def user(user_account: UserAccountEntity) -> UserEntity:
    """Fixture that provides a user account in the database.

    The user will be removed again after running the tests.
    """
    return user_account.user


@pytest.fixture(scope="module")
def owner(user: UserEntity) -> Owner:
    """Fixture for an owner."""
    return Owner(id=user.id, uuid=user.uuid, name=user.name)
