"""Module for testing the access token entity."""
from datetime import datetime

from kwai.core.domain.value_objects import UniqueId, Name, EmailAddress
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users import User, UserAccountEntity, UserAccount


def test_create():
    account = UserAccount(
        password=Password.create_from_string("Test1234"),
        user=User(
            uuid=UniqueId.generate(),
            name=Name(first_name="Jigoro", last_name="Kano"),
            email=EmailAddress("jigoro.kano@kwai.com"),
        ),
    )
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        user_account=UserAccountEntity(id=1, domain=account),
    )

    assert token.revoked is False, "A new token should not be revoked."


def test_get_attr():
    entity = UserAccountEntity(
        id=1,
        domain=UserAccount(
            password=Password.create_from_string("Test1234"),
            user=User(
                uuid=UniqueId.generate(),
                name=Name(first_name="Jigoro", last_name="Kano"),
                email=EmailAddress("jigoro.kano@kwai.com"),
            ),
        ),
    )

    assert entity.user.name.first_name == "Jigoro", "The firstname should be Jigoro"
