"""Module that implements a User entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId

UserIdentifier = IntIdentifier


class UserEntity(Entity[UserIdentifier]):
    """A user entity."""

    def __init__(
        self,
        *,
        id_: UserIdentifier | None = None,
        name: Name,
        email: EmailAddress,
        remark: str | None = "",
        uuid: UniqueId | None = None,
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or UserIdentifier())
        self._name = name
        self._email = email
        self._uuid = uuid or UniqueId.generate()
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def email(self) -> EmailAddress:
        """Return the email address of the user."""
        return self._email

    @property
    def name(self) -> Name:
        """Return the name of the user."""
        return self._name

    def mark_for_update(self):
        """Mark the user as updated."""
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def remark(self) -> str:
        """Return the remark for the user."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of the user."""
        return self._traceable_time

    @property
    def uuid(self) -> UniqueId:
        """Return the unique id the user."""
        return self._uuid

    def create_owner(self) -> Owner:
        """Create an owner value object from the user entity."""
        return Owner(id=self.id, uuid=self.uuid, name=self.name)
