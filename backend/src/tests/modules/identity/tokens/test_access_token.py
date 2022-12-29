"""Module for testing the access token entity."""
from datetime import datetime

from kwai.core.domain.value_objects import UniqueId, Name, EmailAddress
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.tokens.access_token import AccessToken
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users import User, UserEntity


def test_create():
    user = User(
        uuid=UniqueId.generate(),
        name=Name(first_name="Jigoro", last_name="Kano"),
        email=EmailAddress("jigoro.kano@kwai.com"),
    )
    token = AccessToken(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        user=UserEntity(id=1, domain=user),
    )

    assert token.revoked is False, "A new token should not be revoked."
