"""Module that implements a user account entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.exceptions import NotAllowedException
from kwai.modules.identity.users.user import UserEntity

UserAccountIdentifier = IntIdentifier


class UserAccountEntity(Entity[UserAccountIdentifier]):
    """A user account entity."""

    def __init__(
        self,
        *,
        user: UserEntity,
        password: Password,
        id_: UserAccountIdentifier | None = None,
        last_login: Timestamp | None = None,
        last_unsuccessful_login: Timestamp | None = None,
        revoked: bool = False,
        admin: bool = False,
    ):
        super().__init__(id_ or UserAccountIdentifier())
        self._user = user
        self._password = password
        self._last_login = last_login or Timestamp()
        self._last_unsuccessful_login = last_unsuccessful_login or Timestamp()
        self._revoked = revoked
        self._admin = admin

    @property
    def admin(self) -> bool:
        """Check if this user an administrator."""
        return self._admin

    @property
    def last_login(self) -> Timestamp:
        """Return the timestamp of the last successful login."""
        return self._last_login

    @property
    def last_unsuccessful_login(self) -> Timestamp:
        """Return the timestamp of the last unsuccessful login."""
        return self._last_unsuccessful_login

    def login(self, password: str) -> bool:
        """Check if the given password is correct.

        When login succeeds, last_login will be updated.
        When login fails, last_unsuccessful_login will be updated.

        Args:
            password(str): The password.
        """
        if self._password.verify(password):
            self._last_login = Timestamp.create_now()
            return True

        self._last_unsuccessful_login = Timestamp.create_now()
        return False

    @property
    def password(self) -> Password:
        """Return the password of the user."""
        return self._password

    def reset_password(self, password: Password):
        """Reset the password of the user account.

        Args:
            password(Password): The new password.
        """
        if self._revoked:
            raise NotAllowedException()

        self._password = password
        self._user.mark_for_update()

    def revoke(self):
        """Revoke a user account."""
        self._revoked = True
        self._user.mark_for_update()

    @property
    def revoked(self) -> bool:
        """Check if this user is revoked."""
        return self._revoked

    @property
    def user(self) -> UserEntity:
        """Return the associated user entity."""
        return self._user
