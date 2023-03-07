"""Use case: create a user."""
from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(kw_only=True, frozen=True, slots=False)
class CreateUserCommand:
    """Input for the CreateUser use case.

    See: [CreateUser][kwai.modules.identity.create_user.CreateUser]

    Attributes:
        email: The email address for the new user.
        first_name: The first name of the new user.
        last_name: The last name of the new user.
        password: The password for the new user.
        remark: A remark about the new user.
    """

    email: str
    first_name: str
    last_name: str
    password: str
    remark: str


class CreateUser:  # pylint: disable=too-few-public-methods
    """Use case for creating a new user."""

    def __init__(self, user_account_repo: UserAccountRepository):
        """Constructor.

        Args:
            user_account_repo: Repository that creates a new user account.
        """
        self._user_account_repo = user_account_repo

    def execute(self, command: CreateUserCommand) -> UserAccountEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            An entity for a user account.

        Raises:
            UnprocessableException: when the email address is already used by another
                user.
        """
        email = EmailAddress(command.email)
        if self._user_account_repo.exists_with_email(email):
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
        return self._user_account_repo.create(user_account)
