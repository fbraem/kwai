"""Module for testing the access token entity."""
from datetime import datetime

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


def test_create():
    """Test creation of an access token."""
    account = UserAccountEntity(
        password=Password.create_from_string("Test1234"),
        user=UserEntity(
            uuid=UniqueId.generate(),
            name=Name(first_name="Jigoro", last_name="Kano"),
            email=EmailAddress("jigoro.kano@kwai.com"),
        ),
    )
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        user_account=account,
    )

    assert token.revoked is False, "A new token should not be revoked."
