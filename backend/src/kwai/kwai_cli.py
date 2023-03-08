"""Module that starts the CLI for kwai."""

import typer

from kwai import cli

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_show_locals=False)
app.add_typer(cli.identity, name="identity", help="Commands for the identity module.")
app.add_typer(cli.db, name="db", help="Commands to test the kwai environment.")

if __name__ == "__main__":
    app()
