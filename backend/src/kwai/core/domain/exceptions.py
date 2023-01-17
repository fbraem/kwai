"""Module that defines domain exceptions."""


class UnprocessableException(Exception):
    """Raised when a process can't be executed due to the state of the domain."""
