"""Module that implements the Message interface for a mail."""
from .message import Message
from .recipient import Recipients


class Mail(Message):
    """Implements a text/html mail message."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        recipients: Recipients,
        subject: str,
        text: str = "",
        html: str = "",
        headers: dict[str, str] = None,
    ):
        self._recipients = recipients
        self._subject = subject
        self._text = text
        self._html = html
        self._headers = headers or {}

    @property
    def recipients(self) -> Recipients:
        return self._recipients

    def with_recipients(self, recipients: Recipients) -> "Message":
        return Mail(recipients, self._subject, self._text, self._html, self._headers)

    @property
    def subject(self) -> str:
        return self._subject

    def with_subject(self, subject: str) -> "Message":
        return Mail(self._recipients, subject, self._text, self._html, self._headers)

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    def with_headers(self, headers: dict[str, str]) -> "Message":
        return Mail(self._recipients, self._subject, self._text, self._html, headers)

    @property
    def html(self) -> str | None:
        return self._html

    def with_html(self, html: str) -> "Message":
        return Mail(self._recipients, self._subject, self._text, html, self._headers)

    @property
    def text(self) -> str | None:
        return self._text

    def with_text(self, text: str) -> "Message":
        return Mail(self._recipients, self._subject, text, self._html, self._headers)
