"""Module that implements a user account entity."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.exceptions import NotAllowedException
from kwai.modules.identity.users.user import UserEntity

UserAccountIdentifier = IntIdentifier


@dataclass(kw_only=True)
class UserAccountEntity:
    """A user account entity."""

    user: UserEntity
    password: Password = field(repr=False)
    id: UserAccountIdentifier = field(default_factory=UserAccountIdentifier)
    last_login: LocalTimestamp = field(default_factory=LocalTimestamp)
    last_unsuccessful_login: LocalTimestamp = field(default_factory=LocalTimestamp)
    revoked: bool = False
    admin: bool = False

    def login(self, password) -> bool:
        """Check if the given password is correct.

        When login succeeds, last_login will be updated.
        When login fails, last_unsuccessful_login will be updated.
        """
        if self.password.verify(password):
            self.last_login = LocalTimestamp.create_now()
            return True

        self.last_unsuccessful_login = LocalTimestamp.create_now()
        return False

    def reset_password(self, password: Password):
        """Reset the password of the user account."""
        if self.revoked:
            raise NotAllowedException()

        self.password = password
        self.user.traceable_time = self.user.traceable_time.mark_for_update()

    def revoke(self):
        """Revoke a user account."""
        self.revoked = True
        self.user.traceable_time = self.user.traceable_time.mark_for_update()
