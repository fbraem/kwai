"""Module that implements a user account entity."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.users.user import UserEntity

UserAccountIdentifier = IntIdentifier


@dataclass(kw_only=True)
class UserAccountEntity:
    """A user account entity."""

    user: UserEntity
    password: Password = field(repr=False)
    id: UserAccountIdentifier = UserAccountIdentifier()
    last_login: LocalTimestamp = LocalTimestamp()
    last_unsuccessful_login: LocalTimestamp = LocalTimestamp()
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

    def revoke(self):
        """Revoke a user account."""
        self.revoked = True
        self.user.traceable_time = self.user.traceable_time.mark_for_update()
