"""Module that defines a value object for a name."""

from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Name:
    """A value object for a name."""

    first_name: str | None
    last_name: str | None

    def __str__(self):
        """Return a string representation."""
        return " ".join(filter(None, [self.first_name, self.last_name]))
