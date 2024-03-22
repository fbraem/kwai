"""Module that defines a value object for a password."""

from dataclasses import dataclass
from typing import Self

import bcrypt


@dataclass(frozen=True, slots=True)
class Password:
    """A value object for a password."""

    hashed_password: bytes

    @classmethod
    def create_from_string(cls, password: str) -> Self:
        """Create a password from a string."""
        return cls(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))

    def verify(self, password: str) -> bool:
        """Verify this password against the given password."""
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def __str__(self):
        """Return a string representation (hashed password)."""
        return self.hashed_password.decode()
