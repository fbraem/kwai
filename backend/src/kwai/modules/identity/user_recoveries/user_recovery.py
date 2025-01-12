"""Module that implements a user recovery entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity


UserRecoveryIdentifier = IntIdentifier


class UserRecoveryEntity(Entity[UserRecoveryIdentifier]):
    """A user recovery domain."""

    def __init__(
        self,
        *,
        id_: UserRecoveryIdentifier | None = None,
        user: UserEntity,
        expiration: Timestamp | None = None,
        uuid: UniqueId | None = None,
        remark: str = "",
        confirmation: Timestamp | None = None,
        mailed_at: Timestamp | None = None,
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or UserRecoveryIdentifier())
        self._user = user
        self._expiration = expiration or Timestamp()
        self._uuid = uuid or UniqueId.generate()
        self._remark = remark
        self._confirmation = confirmation or Timestamp()
        self._mailed_at = mailed_at or Timestamp()
        self._traceable_time = traceable_time or TraceableTime()

    def confirm(self):
        """Confirm the user recovery."""
        self._confirmation = Timestamp.create_now()
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def confirmed(self) -> bool:
        """Return True when this user recovery was confirmed."""
        return not self._confirmation.empty

    @property
    def confirmed_at(self) -> Timestamp:
        """Return the timestamp of the confirmation."""
        return self._confirmation

    @property
    def expiration(self) -> Timestamp:
        """Return the expiration timestamp."""
        return self._expiration

    @property
    def is_expired(self) -> bool:
        """Return True when the user recovery is expired."""
        return self._expiration.is_past

    @property
    def mailed(self) -> bool:
        """Return True if the email has already been sent."""
        return not self._mailed_at.empty

    @property
    def mailed_at(self) -> Timestamp:
        """Return the timestamp of mail."""
        return self._mailed_at

    def mail_sent(self):
        """Set the timestamp when mail has been sent."""
        self._mailed_at = Timestamp.create_now()
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamps."""
        return self._traceable_time

    @property
    def user(self) -> UserEntity:
        """Return the user."""
        return self._user

    @property
    def uuid(self) -> UniqueId:
        """Return the unique id of the user recovery."""
        return self._uuid
