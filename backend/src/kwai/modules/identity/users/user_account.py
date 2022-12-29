"""Module that implements a user account entity"""
from dataclasses import dataclass, field
from datetime import datetime

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.users import User


@dataclass(kw_only=True)
class UserAccount:
    """A user account domain"""

    user: User
    password: Password = field(repr=False)
    last_login: datetime = None
    last_unsuccessful_login: datetime = None
    revoked: bool = False
    admin: bool = False

    def login(self, password) -> bool:
        """Checks if the given password is correct.

        When login succeeds, last_login will be updated.
        When login fails, last_unsuccessful_login will be updated.
        """
        if self.password.verify(password):
            self.last_login = datetime.utcnow()
            return True

        self.last_unsuccessful_login = datetime.utcnow()
        return False


class UserAccountEntity(Entity[UserAccount]):
    """User account entity."""
