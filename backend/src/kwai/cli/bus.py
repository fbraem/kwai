"""bus contains subcommands for the event bus."""
import os
from asyncio import run

import typer
from redis.asyncio import Redis
from rich import print  # pylint: disable=redefined-builtin
from typer import Typer

from kwai.core.dependencies import container
from kwai.core.events.stream import RedisStream
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
        print("[bold red]Failed![/bold red] Could not load the settings!")
        print(ex)
        raise typer.Exit(code=1) from None


@app.command(help="Test the redis connection.")
def test():
    """Command for testing the redis connection."""
    try:
        container[Redis]
    except Exception as ex:
        print("[bold red]Failed![/bold red] Could not connect to redis!")
        print(ex)
        raise typer.Exit(code=1) from None

    print("[bold green]Success![/bold green] Connection to redis established!")


@app.command(help="Get information about a stream")
def stream(name: str = typer.Option(..., help="The name of the stream")):
    """Command for getting information about a stream.

    Args:
        name: The name of the stream.
    """
    try:
        redis = container[Redis]
    except Exception as ex:
        print("[bold red]Failed![/bold red] Could not connect to redis!")
        print(ex)
        raise typer.Exit(code=1) from None

    async def _info():
        stream_ = RedisStream(redis, f"kwai.{name}")
        info = await stream_.info()
        print(f"Stream: [bold]{stream_.name}[/bold]")
        print(f"Number of messages: [bold]{info.length}[/bold]")
        print(f"First entry: [bold]{info.first_entry}[/bold]")
        print(f"Last entry: [bold]{info.last_entry}[/bold]")

    run(_info())
