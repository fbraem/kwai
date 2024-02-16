"""Module that defines the contact entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.club.members.value_objects import Address

ContactIdentifier = IntIdentifier


class ContactEntity(Entity[ContactIdentifier]):
    """A contact entity."""

    def __init__(
        self,
        *,
        id_: ContactIdentifier | None = None,
        email: EmailAddress,
        tel: str = "",
        mobile: str = "",
        address: Address,
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize the contact entity."""
        super().__init__(id_ or ContactIdentifier())
        self._email = email
        self._tel = tel
        self._mobile = mobile
        self._address = address
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def email(self) -> EmailAddress:
        """Return the email."""
        return self._email

    @property
    def tel(self) -> str:
        """Return the tel."""
        return self._tel

    @property
    def mobile(self) -> str:
        """Return the mobile."""
        return self._mobile

    @property
    def address(self) -> Address:
        """Return the address."""
        return self._address

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the traceable_time."""
        return self._traceable_time
