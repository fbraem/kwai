"""Module for testing the user recovery entity."""
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.users.user import UserEntity


def test_expired_user_recovery():
    user_recovery = UserRecoveryEntity(
        user=UserEntity(
            email=EmailAddress("jigoro.kano@kwai.com"),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
        expiration=LocalTimestamp.create_with_delta(hours=-2),
    )

    assert user_recovery.is_expired
