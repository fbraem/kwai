"""Module that defines an interface for a service that uses a mailer."""
from abc import abstractmethod

from kwai.core.mail.message import Message


class MailerService:
    """Interface for a mailer service."""

    @abstractmethod
    def send(self) -> Message:
        """Send the mail."""
        raise NotImplementedError
