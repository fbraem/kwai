"""Module that implements a User entity."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects import EmailAddress, UniqueId, Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime


@dataclass(kw_only=True)
class User:
    """A user domain."""

    uuid: UniqueId
    name: Name
    email: EmailAddress
    remark: str | None = None
    traceable_time: TraceableTime = TraceableTime()


class UserEntity(Entity[User]):
    """An entity for the user domain."""
