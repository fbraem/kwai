"""Module that implements a user account entity."""

from dataclasses import dataclass, field, replace
from typing import ClassVar, Self, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.exceptions import NotAllowedException
from kwai.modules.identity.users.user import UserEntity


class UserAccountIdentifier(IntIdentifier):
    """Identifier for a user account."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class UserAccountEntity(DataclassEntity):
    """A user account entity.

    Attributes:
        user: The associated user entity.
        password: The password of the user.
        logged_in: Whether the user is logged in.
        last_login: Timestamp of the last login.
        last_unsuccessful_login: Timestamp of the last unsuccessful login.
        revoked: Whether the user is revoked.
        admin: Whether the user is an administrator.
    """

    ID: ClassVar[Type] = UserAccountIdentifier

    user: UserEntity
    password: Password
    logged_in: bool = False
    last_login: Timestamp = field(default_factory=Timestamp)
    last_unsuccessful_login: Timestamp = field(default_factory=Timestamp)
    revoked: bool = False
    admin: bool = False

    def login(self, password: str) -> Self:
        """Check if the given password is correct.

        When login succeeds, last_login will be updated.
        When login fails, last_unsuccessful_login will be updated.

        Args:
            password: The password.
        """
        if self.password.verify(password):
            return replace(self, last_login=Timestamp.create_now(), logged_in=True)

        return replace(
            self, last_unsuccessful_login=Timestamp.create_now(), logged_in=False
        )

    def reset_password(self, password: Password) -> Self:
        """Reset the password of the user account.

        Args:
            password: The new password.
        """
        if self.revoked:
            raise NotAllowedException()

        return replace(
            self,
            password=password,
            traceable_time=self.traceable_time.mark_for_update(),
        )

    def revoke(self) -> Self:
        """Revoke a user account."""
        return replace(
            self, revoked=True, traceable_time=self.traceable_time.mark_for_update()
        )

    def enact(self) -> Self:
        """Reactivate a user account."""
        return replace(
            self, revoked=False, traceable_time=self.traceable_time.mark_for_update()
        )
