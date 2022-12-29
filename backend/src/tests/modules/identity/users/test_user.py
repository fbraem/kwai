"""Module for testing the user domain."""
from kwai.core.domain.value_objects import UniqueId, Name, EmailAddress
from kwai.modules.identity.users import User


def test_create():
    user = User(
        uuid=UniqueId.generate(),
        name=Name(first_name="Jigoro", last_name="Kano"),
        email=EmailAddress("jigoro.kano@kwai.com"),
    )

    assert str(user.name) == "Jigoro Kano", "The name of the user is Jigoro Kano"
