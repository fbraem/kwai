"""This package defines all commands for the CLI of kwai."""
from .db import app as db
from .identity import app as identity

__all__ = ["identity", "db"]
