"""Module for sharing fixtures in this module."""
import pytest

from kwai.core.db import Database
from kwai.core.domain.value_objects import EmailAddress
from kwai.core.mail import Mailer, Recipients, Recipient
from kwai.core.settings import get_settings


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
