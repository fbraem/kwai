"""Module for testing the user domain."""
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import User


def test_create():
    user = User(
        uuid=UniqueId.generate(),
        name=Name(first_name="Jigoro", last_name="Kano"),
        email=EmailAddress("jigoro.kano@kwai.com"),
    )

    assert str(user.name) == "Jigoro Kano", "The name of the user is Jigoro Kano"
