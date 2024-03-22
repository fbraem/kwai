"""Module for testing the Password value object."""

from kwai.core.domain.value_objects.password import Password


def test_password():
    """Test password."""
    password = Password.create_from_string("TEST/1234")
    assert password.verify("TEST/1234"), "The password should be correct"
