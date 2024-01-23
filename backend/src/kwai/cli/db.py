"""db contains subcommands for the database."""
import os
from asyncio import run

import inject
import typer
from rich import print
from typer import Typer

from kwai.core.db.database import Database
from kwai.core.settings import ENV_SETTINGS_FILE, get_settings


def check():
    """Check if the environment variable is set. If not, stop the cli."""
    if ENV_SETTINGS_FILE not in os.environ:
        print(
            f"[bold red]Please set env variable {ENV_SETTINGS_FILE} to "
            f"the configuration file.[/bold red]"
        )
        raise typer.Exit(code=1) from None
    env_file = os.environ[ENV_SETTINGS_FILE]
    print(f"Settings will be loaded from [bold green]{env_file}[/bold green].")


app = Typer(pretty_exceptions_short=True, callback=check)


@app.command(help="Show the database settings.")
def show(password: bool = typer.Option(False, help="Show the password")):
    """Command for showing the active database settings.

    Args:
        password: show or hide the password (default is hide).
    """
    try:
        settings = get_settings()
        print(f"Host: [bold]{settings.db.host}[/bold]")
        print(f"Name: [bold]{settings.db.name}[/bold]")
        print(f"User: [bold]{settings.db.user}[/bold]")
        if password:
            print(f"Password: [bold]{settings.db.password}[/bold]")
    except Exception as ex:
        print("[bold red]Failed! [/bold red] Could not load the settings!")
        print(ex)
        raise typer.Exit(code=1) from None


@app.command(help="Test the database connection.")
def test():
    """Command for testing the database connection."""

    @inject.autoparams()
    async def _main(database: Database):
        """Closure for handling the async code."""
        try:
            await database.check_connection()
            await database.close()
        except Exception as ex:
            print("[bold red]Failed! [/bold red] Could not connect to the database!")
            print(ex)
            raise typer.Exit(code=1) from None

        print(
            "[bold green]Success! [/bold green] Connection to the database established!"
        )

    run(_main())
