"""Modules that defines all table classes for a user."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import table
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity, UserIdentifier
from kwai.modules.identity.users.user_account import (
    UserAccountEntity,
    UserAccountIdentifier,
)


# pylint: disable=too-many-instance-attributes
@table(name="users")
@dataclass(kw_only=True, frozen=True, slots=True)
class UsersTable:
    """Represent the users table."""

    id: int | None
    email: str
    first_name: str
    last_name: str
    remark: str | None
    uuid: str
    created_at: datetime
    updated_at: datetime | None
    member_id: int | None

    @classmethod
    def persist(cls, user: UserEntity) -> "UsersTable":
        """Transform a user entity into a table record."""
        return UsersTable(
            id=user.id.value,
            email=str(user.email),
            first_name=user.name.first_name,
            last_name=user.name.last_name,
            remark=None,
            uuid=str(user.uuid),
            created_at=user.traceable_time.created_at,
            updated_at=user.traceable_time.updated_at,
            member_id=None,
        )


@dataclass(kw_only=True, frozen=True)
class UserMapper:
    """Transform a table record into a user entity."""

    users_table: UsersTable

    def create_entity(self) -> UserEntity:
        """Create a user entity from a table row."""
        return UserEntity(
            id=UserIdentifier(self.users_table.id),
            uuid=UniqueId.create_from_string(self.users_table.uuid),
            name=Name(
                first_name=self.users_table.first_name,
                last_name=self.users_table.last_name,
            ),
            email=EmailAddress(self.users_table.email),
            traceable_time=TraceableTime(
                created_at=self.users_table.created_at,
                updated_at=self.users_table.updated_at,
            ),
        )


@table("users")
@dataclass(kw_only=True, frozen=True)
class UserAccountsTable:
    """Table for user accounts."""

    id: int | None
    email: str
    first_name: str
    last_name: str
    remark: str | None
    uuid: str
    created_at: datetime
    updated_at: datetime | None
    member_id: int | None
    last_login: datetime | None
    last_unsuccessful_login: datetime | None
    password: str
    revoked: int
    admin: int

    @classmethod
    def persist(cls, user_account: UserAccountEntity) -> "UserAccountsTable":
        """Transform a user account entity into a table record."""
        return UserAccountsTable(
            id=user_account.id.value,
            email=str(user_account.user.email),
            first_name=user_account.user.name.first_name,
            last_name=user_account.user.name.last_name,
            remark=None,
            uuid=str(user_account.user.uuid),
            created_at=user_account.user.traceable_time.created_at,
            updated_at=user_account.user.traceable_time.updated_at,
            member_id=None,
            last_login=user_account.last_login.timestamp,
            last_unsuccessful_login=user_account.last_unsuccessful_login.timestamp,
            password=str(user_account.password),
            revoked=1 if user_account.revoked else 0,
            admin=1 if user_account.admin else 0,
        )


@dataclass(kw_only=True, frozen=True)
class UserAccountMapper:
    """Transform a table record into a user account entity."""

    user_accounts_table: UserAccountsTable

    def create_entity(self) -> UserAccountEntity:
        """Create a user entity from a table row."""
        return UserAccountEntity(
            id=UserAccountIdentifier(self.user_accounts_table.id),
            password=Password(hashed_password=self.user_accounts_table.password),
            last_login=LocalTimestamp(self.user_accounts_table.last_login),
            last_unsuccessful_login=LocalTimestamp(
                self.user_accounts_table.last_unsuccessful_login
            ),
            revoked=self.user_accounts_table.revoked == 1,
            admin=self.user_accounts_table.admin == 1,
            user=UserEntity(
                uuid=UniqueId.create_from_string(self.user_accounts_table.uuid),
                name=Name(
                    first_name=self.user_accounts_table.first_name,
                    last_name=self.user_accounts_table.last_name,
                ),
                email=EmailAddress(self.user_accounts_table.email),
                traceable_time=TraceableTime(
                    created_at=self.user_accounts_table.created_at,
                    updated_at=self.user_accounts_table.updated_at,
                ),
            ),
        )
