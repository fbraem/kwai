"""Module for testing the EmailAddress value object."""

import pytest

from kwai.core.domain.value_objects.email_address import (
    EmailAddress,
    InvalidEmailException,
)


def test_email_address():
    """Test a valid email address."""
    email = EmailAddress("jigoro.kano@kwai.com")
    assert email is not None


def test_invalid_email_address():
    """Test an invalid email address."""
    with pytest.raises(InvalidEmailException):
        EmailAddress("invalid")
