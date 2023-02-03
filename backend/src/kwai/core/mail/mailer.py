"""Module that defines an interface for a mail service."""
from abc import abstractmethod, ABC

from .message import Message


class MailerException(Exception):
    """Exception raised from a Mailer."""


class Mailer(ABC):
    """Interface for a mail service."""

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def send(self, message: Message):
        """Send the message."""
        raise NotImplementedError
