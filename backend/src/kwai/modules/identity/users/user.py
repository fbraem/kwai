"""Module that implements a User entity."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId

UserIdentifier = IntIdentifier


@dataclass(kw_only=True)
class UserEntity:
    """A user entity."""

    name: Name
    email: EmailAddress
    id: UserIdentifier = field(default_factory=UserIdentifier)
    uuid: UniqueId = field(default_factory=UniqueId.generate)
    remark: str | None = None
    traceable_time: TraceableTime = field(default_factory=TraceableTime)
