"""Module that defines a value object for a token identifier."""
from dataclasses import dataclass
from secrets import token_hex


@dataclass(frozen=True, kw_only=True)
class TokenIdentifier:
    """A value object for a token identifier."""

    hex_string: str

    @classmethod
    def generate(cls):
        """Create a new token identifier with a random text string."""
        return TokenIdentifier(hex_string=token_hex(40))

    def __str__(self):
        """Return a string representation of the token."""
        return self.hex_string
