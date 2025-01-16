"""bus contains subcommands for the event bus."""

import os

from asyncio import run
from typing import Optional

import inject
import typer

from redis import RedisError
from redis.asyncio import Redis
from rich import print
from rich.tree import Tree
from typer import Typer

from kwai.core.events.stream import RedisStream
from kwai.core.settings import ENV_SETTINGS_FILE, get_settings


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


async def _create_groups_tree(stream_: RedisStream) -> Tree:
    tree = Tree("Groups:")
    groups_ = await stream_.get_groups()
    for group_info in groups_.values():
        leaf = tree.add(group_info.name)
        leaf.add(f"[bold]Pending: [/bold]{group_info.pending}")
        leaf.add(f"[bold]Consumers: [/bold]{group_info.consumers}")
        leaf.add(f"[bold]Last delivered: [/bold]{group_info.last_delivered_id}")
    return tree


@app.command(name="show", help="Show the event bus (redis) settings.")
def show_command(password: bool = typer.Option(False, help="Show the password")):
    """Command for showing the active database settings.

    Args:
        password: show or hide the password (default is hide).
    """
    try:
        settings = get_settings()
        print(f"Host: [bold]{settings.redis.host}[/bold]")
        print(f"Port: [bold]{settings.redis.port}[/bold]")
        if password:
            print(f"Password: [bold]{settings.redis.password}[/bold]")
    except Exception as ex:
        print("[bold red]Failed![/bold red] Could not load the settings!")
        print(ex)
        raise typer.Exit(code=1) from None


@app.command(name="test", help="Test the redis connection.")
def test_command():
    """Command for testing the redis connection.

    When a connection was successful, a PING command will be sent to the redis server.
    """

    @inject.autoparams()
    async def execute(redis: Redis):
        try:
            ping_result = await redis.ping()
            if ping_result:
                print("Ping [bold green]success[/bold green]!")
            else:
                print("Ping [bold red]failed[/bold red]!")
                raise typer.Exit(code=1) from None
        except RedisError as ex:
            print("[bold red]Failed![/bold red] Could not connect to redis!")
            print(ex)
            print("The show command can be used to check the settings.")
            raise typer.Exit(code=1) from None

    run(execute())


@app.command(name="groups", help="")
def groups_command(
    stream: str = typer.Option(help="Name of the stream"),
    group: Optional[str] = typer.Option(default=None, help="Name of the group"),
    delete: Optional[bool] = typer.Option(default=False, help="Delete the group?"),
):
    """Command for showing groups of a stream."""

    @inject.autoparams()
    async def execute(redis: Redis):
        stream_ = RedisStream(redis, stream)

        if group is None:  # Print all groups
            try:
                tree = await _create_groups_tree(stream_)
                print(tree)
            except RedisError as exc:
                print("Could not retrieve group(s)!")
                raise typer.Exit(code=1) from exc
            return

        try:
            group_info = await stream_.get_group(group)
            if group_info is None:
                print(
                    f"Group [bold red]{group}[/bold red] does not exist "
                    f"in stream [bold red]{stream}[/bold red]"
                )
                raise typer.Exit(code=1) from None
        except RedisError as ex:
            print("Could not retrieve group(s)!")
            raise typer.Exit(code=1) from ex

        tree = Tree(group_info.name)
        tree.add(f"[bold]Pending: [/bold]{group_info.pending}")
        tree.add(f"[bold]Consumers: [/bold]{group_info.consumers}")
        tree.add(f"[bold]Last delivered: [/bold]{group_info.last_delivered_id}")
        print(tree)

        if delete:
            if group_info.pending > 0:
                print(
                    f"[bold]There are still "
                    f"[bold red]{group_info.pending}[/bold red] "
                    f"messages pending![/bold]"
                )
            if not typer.confirm(
                f"Are you sure to delete the group {group} from stream {stream}?"
            ):
                return

            try:
                await stream_.delete_group(group)
            except RedisError as exc:
                print(f"Could not delete group {group}!")
                raise typer.Exit(code=1) from exc

    run(execute())


@app.command(name="streams", help="Get a list of available streams")
def streams_command(groups: bool = typer.Option(False, help="List all groups")):
    """Command for getting a list of streams from Redis.

    Args:
        groups: List all groups of a stream or not? Default is False.
    """

    @inject.autoparams()
    async def execute(redis: Redis):
        try:
            async for stream in redis.scan_iter(type_="STREAM"):
                print(stream.decode("utf-8"))
                if groups:
                    tree = await _create_groups_tree(RedisStream(redis, stream))
                    print(tree)
        except RedisError as ex:
            print("Could not retrieve streams!")
            raise typer.Exit(code=1) from ex

    run(execute())


@app.command(name="stream", help="Get information about a stream")
def stream_command(  # noqa
    name: str = typer.Option(..., help="The name of the stream"),
    messages: bool = typer.Option(False, help="List all messages"),
):
    """Command for getting information about a stream.

    Args:
        name: The name of the stream.
        messages: List all messages or not? Default is False.
    """

    async def create_message_tree(stream: RedisStream) -> Tree:
        tree = Tree("Messages:")
        last_id = "0-0"
        while True:
            message = await stream.read(last_id)
            if message is None:
                break
            last_id = message.id

            leaf = tree.add(f"[bold]{message.id}[/bold]")
            if "meta" in message.data:
                if "name" in message.data["meta"]:
                    text = (
                        f"[green][bold]{message.data['meta']['name']}[/bold][/green]:"
                    )
                else:
                    text = ""
                if "date" in message.data["meta"]:
                    text += f" {message.data['meta']['date']}"
                if len(text) > 0:
                    leaf = leaf.add(text)
            leaf.add(str(message.data["data"]))
        return tree

    @inject.autoparams()
    async def execute(redis: Redis):
        """Closure for handling the async code."""
        stream = RedisStream(redis, name)
        info = await stream.info()
        if info is None:
            print(f"Stream [bold red]{stream.name}[/bold red] does not exist!")
            raise typer.Exit(code=1) from None

        print(f"Stream: [bold]{stream.name}[/bold]")
        print(f"Number of messages: [bold]{info.length}[/bold]")
        print(f"First entry: [bold]{info.first_entry}[/bold]")
        print(f"Last entry: [bold]{info.last_entry}[/bold]")

        print(await _create_groups_tree(stream))

        if not messages:
            return

        if info.length > 100:
            if not typer.confirm(
                f"You are about to browse {info.length} messages. Are you sure?"
            ):
                return

        try:
            tree = await create_message_tree(RedisStream(redis, name))
            print(tree)
        except RedisError:
            print("Could not retrieve messages!")
            raise typer.Exit(code=1) from None

    run(execute())
