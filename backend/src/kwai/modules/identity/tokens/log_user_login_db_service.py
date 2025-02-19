"""Module that defines a LogUserLoginService with a database."""

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.log_user_login_service import LogUserLoginService
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.user_log import UserLogEntity
from kwai.modules.identity.tokens.user_log_db_repository import UserLogDbRepository
from kwai.modules.identity.tokens.value_objects import IpAddress, OpenId


class LogUserLoginDbService(LogUserLoginService):
    """Logs a login user request to the database."""

    def __init__(
        self,
        database: Database,
        *,
        email: str,
        client_ip: str,
        user_agent: str,
        open_id_sub: str = "",
        open_id_provider: str = "",
    ):
        self._db = database
        self._email = email
        self._client_ip = IpAddress.create(client_ip)
        self._user_agent = user_agent
        self._openId = OpenId(sub=open_id_sub, provider=open_id_provider)

    async def notify_failure(self, message: str = "") -> None:
        repo = UserLogDbRepository(self._db)
        await repo.create(
            UserLogEntity(
                success=False,
                email=self._email,
                client_ip=self._client_ip,
                user_agent=self._user_agent,
                remark=message,
                openid=self._openId,
            )
        )

    async def notify_success(self, refresh_token: RefreshTokenEntity) -> None:
        repo = UserLogDbRepository(self._db)
        await repo.create(
            UserLogEntity(
                success=True,
                email=self._email,
                refresh_token=refresh_token,
                client_ip=self._client_ip,
                user_agent=self._user_agent,
                openid=self._openId,
            )
        )
