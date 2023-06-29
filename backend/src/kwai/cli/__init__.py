"""Package that defines all commands for the CLI of kwai."""
from .bus import app as bus
from .db import app as db
from .identity import app as identity

__all__ = ["bus", "db", "identity"]
