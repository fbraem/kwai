"""Module that starts the CLI for kwai."""

import typer

from kwai import cli

app = typer.Typer(pretty_exceptions_short=True, pretty_exceptions_show_locals=False)
app.add_typer(cli.identity, name="identity")

if __name__ == "__main__":
    app()
