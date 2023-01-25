"""Module that defines an interface for a mail service."""
from abc import abstractmethod

from .message import Message


class MailerException(Exception):
    """Exception raised from a Mailer."""


class Mailer:
    """Interface for a mail service."""

    @abstractmethod
    def send(self, message: Message):
        """Sends the message."""
        raise NotImplementedError
