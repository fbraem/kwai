"""Module for a use case that logs a user login."""

from dataclasses import dataclass

from kwai.modules.identity.tokens.refresh_token import (
    RefreshTokenEntity,
)
from kwai.modules.identity.tokens.user_log import UserLogEntity
from kwai.modules.identity.tokens.user_log_repository import UserLogRepository
from kwai.modules.identity.tokens.value_objects import IpAddress


@dataclass(frozen=True, kw_only=True, slots=True)
class LogUserLoginCommand:
    """Input for the use case."""

    success: bool
    email: str = ""
    client_ip: str
    user_agent: str
    openid_sub: str | None = None
    openid_provider: str | None = None


class LogUserLogin:
    """Use case for logging the login of a user."""

    def __init__(
        self,
        user_log_repository: UserLogRepository,
        refresh_token: RefreshTokenEntity | None,
    ):
        """Initialize the use case."""
        self._repo = user_log_repository
        self._refresh_token = refresh_token

    async def execute(self, command: LogUserLoginCommand):
        """Execute the use case."""
        await self._repo.create(
            UserLogEntity(
                success=command.success,
                email=command.email,
                refresh_token=self._refresh_token,
                client_ip=IpAddress.create(command.client_ip),
                user_agent=command.user_agent,
            )
        )
