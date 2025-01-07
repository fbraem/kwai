"""Module for testing the dataclass Entity."""

from dataclasses import dataclass

import pytest

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.club.domain.value_objects import Birthdate

UserIdentifier = IntIdentifier


@dataclass(frozen=True, eq=False, kw_only=True, slots=True)
class UserEntity(DataclassEntity):
    """A sample entity class."""

    name: str
    birthdate: Birthdate


@pytest.fixture
def user_entity() -> UserEntity:
    """Fixture to create a user entity."""
    return UserEntity(
        id=UserIdentifier(1),
        name="Franky",
        birthdate=Birthdate(date=Date.create(1969, 3, 9)),
    )


def test_create(user_entity: UserEntity):
    """Test creating an entity."""
    assert user_entity.id.value == 1, "The id should be 2"
    assert user_entity.name == "Franky", "The name should be 'Franky'"
    assert user_entity.birthdate.date.year == 1969, "Year of birth should be 1969"


def test_change_id_not_allowed(user_entity: UserEntity):
    """Test that changing the id is not allowed."""
    with pytest.raises(ValueError):
        user_entity.set_id(UserIdentifier(2))
