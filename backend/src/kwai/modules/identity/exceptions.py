"""Module that defines common identity exceptions."""


class AuthenticationException(Exception):
    """Raised when authentication is not allowed."""


class NotAllowedException(Exception):
    """Raised when an action is not allowed."""
