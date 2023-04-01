"""Module that starts the CLI for kwai."""

import typer

from kwai import cli

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_show_locals=False)
app.add_typer(cli.bus, name="bus", help="Commands for the event bus.")
app.add_typer(cli.db, name="db", help="Commands for the database.")
app.add_typer(cli.identity, name="identity", help="Commands for the identity module.")

if __name__ == "__main__":
    app()
