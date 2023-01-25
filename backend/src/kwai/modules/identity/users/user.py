"""Module that implements a User entity."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId


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
