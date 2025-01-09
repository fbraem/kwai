"""Module for defining factory fixtures for the user entities."""

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def make_user():
    """Factory fixture for creating a user entity."""

    def _make_user(
        uuid: UniqueId | None = None,
        name: Name | None = None,
        email: EmailAddress | None = None,
    ) -> UserEntity:
        return UserEntity(
            uuid=uuid,
            name=name or Name(first_name="Jigoro", last_name="Kano"),
            email=email or EmailAddress("jigoro.kano@kwai.com"),
        )

    return _make_user


@pytest.fixture
def make_user_account(make_user):
    """Factory fixture for creating a user account for testing."""

    def _make_user_account(
        password: Password | None = None, user: UserEntity | None = None
    ) -> UserAccountEntity:
        return UserAccountEntity(
            password=password or Password.create_from_string("Test1234"),
            user=user or make_user(),
        )

    return _make_user_account
