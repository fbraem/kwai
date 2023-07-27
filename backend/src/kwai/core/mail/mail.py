"""Module that implements the Message interface for a mail."""
from .message import Message
from .recipient import Recipients


class Mail(Message):
    """Implements a text/html mail message."""

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
        """Return the recipients."""
        return self._recipients

    def with_recipients(self, recipients: Recipients) -> "Message":
        """Clone the current mail and set the recipients."""
        return Mail(recipients, self._subject, self._text, self._html, self._headers)

    @property
    def subject(self) -> str:
        """Return the subject of the mail."""
        return self._subject

    def with_subject(self, subject: str) -> "Message":
        """Clone the current mail and set the subject."""
        return Mail(self._recipients, subject, self._text, self._html, self._headers)

    @property
    def headers(self) -> dict[str, str]:
        """Return the headers."""
        return self._headers

    def with_headers(self, headers: dict[str, str]) -> "Message":
        """Clone the current mail and set the headers."""
        return Mail(self._recipients, self._subject, self._text, self._html, headers)

    @property
    def html(self) -> str | None:
        """Return the HTML content."""
        return self._html

    def with_html(self, html: str) -> "Message":
        """Clone the current mail and set the HTML content."""
        return Mail(self._recipients, self._subject, self._text, html, self._headers)

    @property
    def text(self) -> str | None:
        """Return the text content."""
        return self._text

    def with_text(self, text: str) -> "Message":
        """Clone the current mail and set the text content."""
        return Mail(self._recipients, self._subject, text, self._html, self._headers)
