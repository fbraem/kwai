"""Module for an email address value object."""

from dataclasses import dataclass

from email_validator import validate_email


class InvalidEmailException(Exception):
    """Raised when the email address is not valid."""


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """A value object for an email address."""

    email: str

    def __post_init__(self):
        """Check if the email address is valid."""
        from email_validator import EmailNotValidError

        try:
            validate_email(self.email, check_deliverability=False)
        except EmailNotValidError as exc:
            raise InvalidEmailException(
                f"{self.email} is not a valid email address: {exc}"
            ) from exc

    def __str__(self):
        """Return the string representation of an email address."""
        return self.email
