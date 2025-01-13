"""Module for handling arguments for starting a uvicorn application."""

import argparse

from argparse import Namespace


def create_args(prog: str, default_port: int = 8000) -> Namespace:
    """Parse and create cli arguments."""
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument(
        "--reload",
        action=argparse.BooleanOptionalAction,
        help="Watch for code changes or not",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="The host of the server."
    )
    parser.add_argument(
        "--port", type=int, default=default_port, help="The port of the server."
    )
    return parser.parse_args()
