"""Identity contains all subcommands for managing identity in kwai.

Note:
    Make sure the environment variable KWAI_SETTINGS_FILE is set!
"""
import os

import typer
from rich import print  # pylint: disable=redefined-builtin
from typer import Typer

from kwai.core.db.database import Database
from kwai.core.dependencies import container
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.settings import ENV_SETTINGS_FILE
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)

app = Typer(pretty_exceptions_short=True)


@app.callback()
def check():
    """Check if the environment variable is set. If not, stop the cli."""
    if ENV_SETTINGS_FILE not in os.environ:
        print(
            f"[bold red]Please set env variable {ENV_SETTINGS_FILE} to "
            f"the configuration file.[/bold red]"
        )
        raise typer.Exit(code=1)


@app.command(help="Create a user account.")
def create(
    email: str = typer.Option(
        ..., help="The email address of the new user", prompt=True
    ),
    first_name: str = typer.Option(
        ..., help="The first name of the new user", prompt=True
    ),
    last_name: str = typer.Option(
        ..., help="The last name of the new user", prompt=True
    ),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True
    ),
):
    """Create a user account.

    Use this command to create a new user account (for the root user for example).

    Args:
        email: The email address of the new user
        first_name: The firstname of the new user
        last_name: The lastname of the new user
        password: The password of the new user
    """
    user_account = UserAccountEntity(
        user=UserEntity(
            name=Name(first_name=first_name, last_name=last_name),
            email=EmailAddress(email),
            remark="This user was created using the CLI",
        ),
        password=Password.create_from_string(password),
    )
    repo = UserAccountDbRepository(container[Database])
    repo.create(user_account)
