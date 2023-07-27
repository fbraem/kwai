"""Module for testing smtp mailer."""
from typing import Iterator

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.mail.mail import Mail
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipient, Recipients
from kwai.core.settings import get_settings

pytestmark = pytest.mark.integration


@pytest.fixture
def smtp_mailer() -> Iterator[Mailer]:
    """Fixture for getting a mailer."""
    from kwai.core.mail.smtp_mailer import SmtpMailer

    settings = get_settings()
    smtp_mailer = SmtpMailer(
        host=settings.email.host, port=settings.email.port, tls=settings.email.tls
    )
    try:
        smtp_mailer.connect()
        if settings.email.user:
            smtp_mailer.login(settings.email.user, settings.email.password)
        yield smtp_mailer
    finally:
        smtp_mailer.disconnect()


def test_text_message(smtp_mailer: Mailer):
    """Test sending a text message."""
    mail = Mail(
        subject="test_text_message",
        recipients=Recipients(
            from_=Recipient(email=EmailAddress("webmaster@kwai.com"), name="Webmaster"),
            to=[
                Recipient(
                    email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano"
                )
            ],
        ),
        text="Hell world",
        html="<b>Hello World</b>",
    )
    smtp_mailer.send(mail)
