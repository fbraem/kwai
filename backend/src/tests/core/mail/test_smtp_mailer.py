import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.mail.mail import Mail
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.mail.smtp_mailer import SmtpMailer
from kwai.core.settings import get_settings


@pytest.fixture
def mailer():
    settings = get_settings()
    m = SmtpMailer(settings.email.host, settings.email.port)
    m.connect(settings.email.user, settings.email.password)
    return m


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
