"""Module for an email address value object."""
from dataclasses import dataclass

from pyisemail import is_email


class InvalidEmailException(Exception):
    """Raised when the email address is not valid."""


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """A value object for an email address."""

    email: str

    def __post_init__(self):
        """Check if the email address is valid."""
        if not is_email(self.email):
            raise InvalidEmailException()

    def __str__(self):
        """Return the string representation of an email address."""
        return self.email
