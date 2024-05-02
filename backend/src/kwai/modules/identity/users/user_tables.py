"""Modules that defines all table classes for a user."""

from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity, UserIdentifier
from kwai.modules.identity.users.user_account import (
    UserAccountEntity,
    UserAccountIdentifier,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class UserRow:
    """Represent a row in the users table."""

    id: int | None
    email: str
    first_name: str
    last_name: str
    remark: str | None
    uuid: str
    created_at: datetime
    updated_at: datetime | None
    person_id: int | None

    def create_entity(self) -> UserEntity:
        """Create a user entity from a table row."""
        return UserEntity(
            id_=UserIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            name=Name(
                first_name=self.first_name,
                last_name=self.last_name,
            ),
            remark=self.remark,
            email=EmailAddress(self.email),
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(timestamp=self.created_at),
                updated_at=LocalTimestamp(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, user: UserEntity) -> "UserRow":
        """Transform a user entity into a table record."""
        return UserRow(
            id=user.id.value,
            email=str(user.email),
            first_name=user.name.first_name,
            last_name=user.name.last_name,
            remark=user.remark,
            uuid=str(user.uuid),
            created_at=user.traceable_time.created_at.timestamp,
            updated_at=user.traceable_time.updated_at.timestamp,
            person_id=None,
        )


UsersTable = Table("users", UserRow)


@dataclass(kw_only=True, frozen=True)
class UserAccountRow:
    """Represent a row in the user table with user account information."""

    id: int | None
    email: str
    first_name: str
    last_name: str
    remark: str | None
    uuid: str
    created_at: datetime
    updated_at: datetime | None
    person_id: int | None
    last_login: datetime | None
    last_unsuccessful_login: datetime | None
    password: str
    revoked: int
    admin: int

    def create_entity(self) -> UserAccountEntity:
        """Create a user account entity from the table row."""
        return UserAccountEntity(
            id_=UserAccountIdentifier(self.id),
            password=Password(self.password.encode()),
            last_login=LocalTimestamp(self.last_login),
            last_unsuccessful_login=LocalTimestamp(self.last_unsuccessful_login),
            revoked=self.revoked == 1,
            admin=self.admin == 1,
            user=UserEntity(
                id_=UserIdentifier(self.id),
                uuid=UniqueId.create_from_string(self.uuid),
                name=Name(
                    first_name=self.first_name,
                    last_name=self.last_name,
                ),
                email=EmailAddress(self.email),
                traceable_time=TraceableTime(
                    created_at=LocalTimestamp(self.created_at),
                    updated_at=LocalTimestamp(self.updated_at),
                ),
            ),
        )

    @classmethod
    def persist(cls, user_account: UserAccountEntity) -> "UserAccountRow":
        """Transform a user account entity into a table record."""
        return UserAccountRow(
            id=user_account.id.value,
            email=str(user_account.user.email),
            first_name=user_account.user.name.first_name,
            last_name=user_account.user.name.last_name,
            remark=None,
            uuid=str(user_account.user.uuid),
            created_at=user_account.user.traceable_time.created_at.timestamp,
            updated_at=user_account.user.traceable_time.updated_at.timestamp,
            person_id=None,
            last_login=user_account.last_login.timestamp,
            last_unsuccessful_login=user_account.last_unsuccessful_login.timestamp,
            password=str(user_account.password),
            revoked=1 if user_account.revoked else 0,
            admin=1 if user_account.admin else 0,
        )


UserAccountsTable = Table("users", UserAccountRow)
