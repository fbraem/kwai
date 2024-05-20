"""Module that defines the contact entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.club.domain.value_objects import Address

ContactIdentifier = IntIdentifier


class ContactEntity(Entity[ContactIdentifier]):
    """A contact entity."""

    def __init__(
        self,
        *,
        id_: ContactIdentifier | None = None,
        emails: list[EmailAddress] | None = None,
        tel: str = "",
        mobile: str = "",
        address: Address,
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize the contact entity."""
        super().__init__(id_ or ContactIdentifier())
        self._emails = emails or []
        self._tel = tel
        self._mobile = mobile
        self._address = address
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def emails(self) -> list[EmailAddress]:
        """Return the emails of the contact.

        Note: the returned list is a copy.
        """
        return self._emails.copy()

    def add_email(self, email: EmailAddress) -> None:
        """Add an email to the contact."""
        self._emails.append(email)

    def remove_email(self, email: EmailAddress) -> None:
        """Remove the email from the contact."""
        self._emails.remove(email)

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
