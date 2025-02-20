"""Module that defines the UserLog entity."""

from dataclasses import dataclass, field
from typing import ClassVar, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.value_objects import IpAddress, OpenId
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserLogIdentifier(IntIdentifier):
    """Identifier for a UserLog entity."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class UserLogEntity(DataclassEntity):
    """A UserLog entity.

    Attributes:
        success: Was this user logged in successfully?
        email: Email used to log in.
        user_account: User account used to log in.
        refresh_token: Refresh token created for the login.
        client_ip: Client IP address
        user_agent: User agent string
        openid: OpenId information
        remark: A remark
        created_at: Timestamp of login
    """

    ID: ClassVar[Type] = UserLogIdentifier

    success: bool = False
    email: str = ""
    user_account: UserAccountEntity | None = None
    refresh_token: RefreshTokenEntity | None = None
    client_ip: IpAddress
    user_agent: str
    openid: OpenId = field(default_factory=OpenId)
    remark: str = ""
    created_at: Timestamp = field(default_factory=Timestamp.create_now)
