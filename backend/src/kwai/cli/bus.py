"""bus contains subcommands for the event bus."""
import os

import typer
from rich import print  # pylint: disable=redefined-builtin
from typer import Typer

from kwai.core.dependencies import container
from kwai.core.settings import ENV_SETTINGS_FILE, Settings


def check():
    """Check if the environment variable is set. If not, stop the cli."""
    if ENV_SETTINGS_FILE not in os.environ:
        print(
            f"[bold red]Please set env variable {ENV_SETTINGS_FILE} to "
            f"the configuration file.[/bold red]"
        )
        raise typer.Exit(code=1)
    env_file = os.environ[ENV_SETTINGS_FILE]
    print(f"Settings will be loaded from [bold green]{env_file}[/bold green].")


app = Typer(pretty_exceptions_short=True, callback=check)


@app.command(help="Show the event bus (redis) settings.")
def show(password: bool = typer.Option(False, help="Show the password")):
    """Command for showing the active database settings.

    Args:
        password: show or hide the password (default is hide).
    """
    try:
        settings = container[Settings]
        print(f"Host: [bold]{settings.redis.host}[/bold]")
        print(f"Port: [bold]{settings.redis.port}[/bold]")
        if password:
            print(f"Password: [bold]{settings.redis.password}[/bold]")
    except Exception as ex:
        print("[bold red]Failed! [/bold red] Could not load the settings!")
        print(ex)
        raise typer.Exit(code=1)
