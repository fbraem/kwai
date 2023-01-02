"""Module that defines a mailer service with SMTP."""
import smtplib
import ssl
from email.headerregistry import Address
from email.message import EmailMessage

from kwai.core.mail import Mailer, Message, MailerException


class SmtpMailer(Mailer):
    def __init__(self, host: str, port: int | None = None, ssl_: bool = False):
        self._host = host
        if port is None:
            self._port = 456 if ssl_ else 587
        else:
            self._port = port
        self._ssl = ssl_
        self._server = None

    def __del__(self):
        self.disconnect()

    def connect(self, user: str, password: str):
        context = ssl.create_default_context()
        if self._ssl:
            self._server = smtplib.SMTP_SSL(self._host, self._port, context=context)
        else:
            self._server = smtplib.SMTP(self._host, self._port)
            try:
                self._server.starttls(context=context)
            except smtplib.SMTPException as exc:
                raise MailerException("STARTTLS failed.") from exc

        try:
            self._server.login(user, password)
        except smtplib.SMTPException as exc:
            raise MailerException("Login failed.") from exc

    def disconnect(self):
        if self._server:
            try:
                self._server.quit()
            except smtplib.SMTPException:
                pass  # Ignore exceptions here
            self._server = None

    def send(self, message: Message):
        email_message = EmailMessage()

        email_message["Subject"] = message.subject
        email_message.set_content(message.text)
        for header_name, header_value in message.headers.items():
            email_message.add_header(header_name, header_value)

        email_message["From"] = Address(
            display_name=message.recipients.from_.name,
            addr_spec=str(message.recipients.from_.email),
        )

        email_message["To"] = [
            Address(display_name=to.name, addr_spec=str(to.email))
            for to in message.recipients.to
        ]
        if len(message.recipients.cc) > 0:
            email_message["Cc"] = [
                Address(display_name=cc.name, addr_spec=str(cc.email))
                for cc in message.recipients.cc
            ]
        if len(message.recipients.bcc) > 0:
            email_message["Bcc"] = [
                Address(display_name=bcc.name, addr_spec=str(bcc.email))
                for bcc in message.recipients.bcc
            ]

        if len(message.html) > 0:
            email_message.add_alternative(message.html, subtype="html")

        try:
            self._server.send_message(email_message)
        except smtplib.SMTPException as exc:
            raise MailerException("Sendmail failed") from exc
