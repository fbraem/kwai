"""Module that defines a value object for a token identifier."""
from dataclasses import dataclass
from secrets import token_hex


@dataclass
class TokenIdentifier:
    """A value object for a token identifier."""

    bytes: str

    @classmethod
    def generate(cls):
        """Creates a new token identifier with a random text string."""
        return TokenIdentifier(token_hex(40))

    def __str__(self):
        return self.bytes
