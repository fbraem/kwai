"""Module for testing the user recovery entity."""

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.users.user import UserEntity


def test_expired_user_recovery():
    """Test expire of a user recovery."""
    user_recovery = UserRecoveryEntity(
        user=UserEntity(
            email=EmailAddress("jigoro.kano@kwai.com"),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
        expiration=Timestamp.create_with_delta(hours=-2),
    )

    assert user_recovery.is_expired


def test_confirm_user_recovery():
    """Test confirming a user recovery."""
    user_recovery = UserRecoveryEntity(
        user=UserEntity(
            email=EmailAddress("jigoro.kano@kwai.com"),
            name=Name(first_name="Jigoro", last_name="Kano"),
        )
    )
    user_recovery = user_recovery.confirm()

    assert user_recovery.confirmed is True, "The user recovery should be confirmed."
