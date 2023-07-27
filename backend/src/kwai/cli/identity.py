"""Identity contains all subcommands for managing identity in kwai.

Note:
    Make sure the environment variable KWAI_SETTINGS_FILE is set!

"""
import os
from asyncio import run

import typer
from rich import print
from typer import Typer

from kwai.core.db.database import Database
from kwai.core.dependencies import container
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.settings import ENV_SETTINGS_FILE
from kwai.modules.identity.create_user import CreateUser, CreateUserCommand
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


def check():
    """Check if the environment variable is set. If not, stop the cli."""
    if ENV_SETTINGS_FILE not in os.environ:
        print(
            f"[bold red]Please set env variable {ENV_SETTINGS_FILE} to "
            f"the configuration file.[/bold red]"
        )
        raise typer.Exit(code=1) from None


app = Typer(pretty_exceptions_short=True, callback=check)


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

    async def _main():
        """Closure for handling the async code."""
        command = CreateUserCommand(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            remark="This user was created using the CLI",
        )
        try:
            await CreateUser(UserAccountDbRepository(container[Database])).execute(
                command
            )
            print(
                f"[bold green]Success![/bold green] "
                f"User created with email address {email}"
            )
        except UnprocessableException as ex:
            print("[bold red]Failed![/bold red] User could not created:")
            print(ex)
            raise typer.Exit(code=1) from None

    run(_main())
