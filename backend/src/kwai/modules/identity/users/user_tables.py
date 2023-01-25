"""Modules that defines all table classes for a user."""
from datetime import datetime
from dataclasses import dataclass

from kwai.core.db import table
from kwai.core.domain.value_objects import UniqueId, Name, EmailAddress, TraceableTime
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.users.user import User, UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity, UserAccount


# pylint: disable=too-many-instance-attributes
@table(name="users")
@dataclass(kw_only=True, frozen=True, slots=True)
class UsersTable:
    """Represents the users table"""

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
    def persist(cls, user: User) -> "UsersTable":
        return UsersTable(
            id=None,
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
    users_table: UsersTable

    def create_entity(self) -> UserEntity:
        """Creates a user entity from a table row."""
        return UserEntity(
            id=self.users_table.id,
            domain=User(
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
    def persist(cls, user_account: UserAccount) -> "UserAccountsTable":
        return UserAccountsTable(
            id=None,
            email=str(user_account.user.email),
            first_name=user_account.user.name.first_name,
            last_name=user_account.user.name.last_name,
            remark=None,
            uuid=str(user_account.user.uuid),
            created_at=user_account.user.traceable_time.created_at,
            updated_at=user_account.user.traceable_time.updated_at,
            member_id=None,
            last_login=user_account.last_login,
            last_unsuccessful_login=user_account.last_unsuccessful_login,
            password=str(user_account.password),
            revoked=1 if user_account.revoked else 0,
            admin=1 if user_account.admin else 0,
        )


@dataclass(kw_only=True, frozen=True)
class UserAccountMapper:
    user_accounts_table: UserAccountsTable

    def create_entity(self) -> UserAccountEntity:
        """Creates a user entity from a table row."""
        return UserAccountEntity(
            id=self.user_accounts_table.id,
            domain=UserAccount(
                password=Password(hashed_password=self.user_accounts_table.password),
                last_login=self.user_accounts_table.last_login,
                last_unsuccessful_login=self.user_accounts_table.last_unsuccessful_login,
                revoked=self.user_accounts_table.revoked == 1,
                admin=self.user_accounts_table.admin == 1,
                user=User(
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
            ),
        )
