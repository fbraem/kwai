"""Module that starts the CLI for kwai."""

import typer

from kwai.cli import commands, dependencies

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_show_locals=False)
app.add_typer(commands.bus, name="bus", help="Commands for the event bus.")
app.add_typer(commands.db, name="db", help="Commands for the database.")
app.add_typer(
    commands.identity, name="identity", help="Commands for the identity module."
)

if __name__ == "__main__":
    dependencies.configure()

    app()
