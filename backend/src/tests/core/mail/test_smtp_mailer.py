from typing import Iterator

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.mail.mail import Mail
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.settings import get_settings

pytestmark = pytest.mark.integration


@pytest.fixture
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


def test_text_message(mailer):
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
    mailer.send(mail)
