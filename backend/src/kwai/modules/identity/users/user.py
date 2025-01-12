"""Module that implements a User entity."""

from dataclasses import dataclass, field
from typing import ClassVar, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.unique_id import UniqueId


class UserIdentifier(IntIdentifier):
    """Identifier for a user entity."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class UserEntity(DataclassEntity):
    """A user entity."""

    ID: ClassVar[Type] = UserIdentifier

    name: Name
    email: EmailAddress
    uuid: UniqueId = field(default_factory=UniqueId.generate)
    remark: str = ""

    def create_owner(self) -> Owner:
        """Create an owner value object from the user entity."""
        return Owner(id=self.id, uuid=self.uuid, name=self.name)
