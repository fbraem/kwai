"""Module that defines the system user"""
from dataclasses import dataclass

from kwai.core.domain.value_objects import UniqueId


@dataclass(kw_only=True, frozen=True, slots=True)
class SystemUser:
    """Represents the user that is currently logged in."""

    id: int
    uuid: UniqueId
