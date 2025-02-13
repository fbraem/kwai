"""Module that implements the logout use case."""

from dataclasses import dataclass

from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


@dataclass(frozen=True, kw_only=True)
class LogoutCommand:
    """Command for the logout use case.

    Attributes:
        identifier(str): The refresh token to revoke
    """

    identifier: str


class Logout:
    """Use case: logout a user.

    A user is logged out by revoking the refresh token. The access token that is
    related to this refresh token will also be revoked.

    Attributes:
        _refresh_token_repository (RefreshTokenRepository): The repository to
            get and update the refresh token.
        _access_token_repository (AccessTokenRepository): The repository to
            get and update the access token.
    """

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        access_token_repository: AccessTokenRepository,
    ):
        self._refresh_token_repository = refresh_token_repository
        self._access_token_repository = access_token_repository

    async def execute(self, command: LogoutCommand):
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            RefreshTokenNotFoundException: The refresh token with the identifier
                could not be found.
        """
        refresh_token = await self._refresh_token_repository.get_by_token_identifier(
            TokenIdentifier(hex_string=command.identifier)
        )
        refresh_token = refresh_token.revoke()

        await self._refresh_token_repository.update(refresh_token)
        await self._access_token_repository.update(refresh_token.access_token)
