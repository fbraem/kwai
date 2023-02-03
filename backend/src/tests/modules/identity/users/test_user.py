"""Module for testing the user domain."""
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.users.user import UserEntity


def test_create():
    """Test user constructor."""
    user = UserEntity(
        name=Name(first_name="Jigoro", last_name="Kano"),
        email=EmailAddress("jigoro.kano@kwai.com"),
    )

    assert str(user.name) == "Jigoro Kano", "The name of the user is Jigoro Kano"
