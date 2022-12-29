"""Module that defines a value object for a password."""
from dataclasses import dataclass

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(kw_only=True, frozen=True, slots=True)
class Password:
    """A value object for a password."""

    hashed_password: str

    @classmethod
    def create_from_string(cls, password: str) -> "Password":
        """Factory method to create a password from a string."""
        return Password(hashed_password=pwd_context.hash(password))

    def verify(self, password: str) -> bool:
        """Verifies this password against the given password."""
        return pwd_context.verify(password, self.hashed_password)

    def __str__(self):
        return self.hashed_password
