"""Module for sharing fixtures in this module."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.settings import get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


@pytest.fixture(scope="module")
def database():
    """Fixture for getting a connected database."""
    database = Database(get_settings().db)  # pylint: disable=redefined-outer-name
    database.connect()
    return database


@pytest.fixture
def mailer() -> Mailer:
    """Fixture for getting a mailer."""
    from kwai.core.mail.smtp_mailer import SmtpMailer

    settings = get_settings()
    m = SmtpMailer(settings.email.host, settings.email.port)
    m.connect(settings.email.user, settings.email.password)
    return m


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
    return Jinja2Engine(settings.template.path, website=settings.website)


@pytest.fixture(scope="module")
def user(database: Database) -> UserEntity:
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
    user_account = repo.create(user_account)
    yield user_account.user
    repo.delete(user_account)
