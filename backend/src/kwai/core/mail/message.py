"""Module that defines an interface for a mail message."""

from abc import abstractmethod

from .recipient import Recipients


class Message:
    """Interface for an immutable message."""

    @property
    @abstractmethod
    def recipients(self) -> Recipients:
        """Returns the recipients for the message."""
        raise NotImplementedError

    @abstractmethod
    def with_recipients(self, recipients: Recipients) -> "Message":
        """Set the recipients for the message.

        This method must return a new Message instance.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def subject(self) -> str:
        """Return the subject of the message."""
        raise NotImplementedError

    @abstractmethod
    def with_subject(self, subject: str) -> "Message":
        """Set the subject for the message.

        This method must return a new Message instance.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        """Returns the headers for this message."""
        raise NotImplementedError

    @abstractmethod
    def with_headers(self, headers: dict[str, str]) -> "Message":
        """Set the headers for the message.

        This method must return a new Message instance.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def html(self) -> str | None:
        """Returns the HTML for the message."""
        raise NotImplementedError

    @abstractmethod
    def with_html(self, html: str) -> "Message":
        """Set the HTML for the message.

        This method must return a new Message instance.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def text(self) -> str | None:
        """Return the text for the message."""
        raise NotImplementedError

    @abstractmethod
    def with_text(self, text: str) -> "Message":
        """Set the text for the message.

        This method must return a new Message instance.
        """
        raise NotImplementedError
