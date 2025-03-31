"""Module that implements the use case for accepting a user invitation."""

from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(kw_only=True, frozen=True, slots=False)
class AcceptUserInvitationCommand:
    """Input for the AcceptUserInvitation use case.

    See: [AcceptUserInvitation][kwai.modules.identity.accept_user_invitation.AcceptUserInvitation]

    Attributes:
        uuid: The unique id of the user invitation.
        email: The email address for the new user.
        first_name: The first name of the new user.
        last_name: The last name of the new user.
        password: The password for the new user.
        remark: A remark about the new user.
    """

    uuid: str
    email: str
    first_name: str
    last_name: str
    password: str
    remark: str


class AcceptUserInvitation:
    """Use case for accepting a user invitation."""

    def __init__(
        self,
        user_invitation_repo: UserInvitationRepository,
        user_account_repo: UserAccountRepository,
        presenter: Presenter[UserAccountEntity],
    ):
        """Create the use case.

        Args:
            user_invitation_repo: Repository for checking the user invitation.
            user_account_repo: Repository that creates a new user account.
            presenter: A presenter for a user account entity.
        """
        self._user_invitation_repo = user_invitation_repo
        self._user_account_repo = user_account_repo
        self._presenter = presenter

    async def execute(self, command: AcceptUserInvitationCommand) -> None:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            An entity for a user account.

        Raises:
            UserInvitationNotFoundExeption: when the user invitation does not
                exist.
            UnprocessableException: when the email address is already used by another
                user.
                When the user invitation is expired or was already accepted.
                When the user invitation is revoked.
        """
        uuid = UniqueId.create_from_string(command.uuid)
        user_invitation = await self._user_invitation_repo.get_invitation_by_uuid(uuid)
        if user_invitation.revoked:
            raise UnprocessableException(
                f"The user invitation with id {uuid} is revoked."
            )
        if user_invitation.is_expired:
            raise UnprocessableException(
                f"The user invitation with id {uuid} is expired."
            )
        if user_invitation.confirmed:
            raise UnprocessableException(
                f"The user invitation with id {uuid} was already accepted."
            )

        email = EmailAddress(command.email)
        if await self._user_account_repo.exists_with_email(email):
            raise UnprocessableException(
                f"A user with email {command.email} already exists."
            )

        user_account = UserAccountEntity(
            user=UserEntity(
                email=email,
                remark=command.remark,
                name=Name(first_name=command.first_name, last_name=command.last_name),
            ),
            password=Password.create_from_string(command.password),
        )

        user_invitation = user_invitation.confirm()
        await self._user_invitation_repo.update(user_invitation)

        user_account = await self._user_account_repo.create(user_account)
        self._presenter.present(user_account)
