"""Module for testing the dataclass Entity."""

from dataclasses import dataclass
from typing import ClassVar, Type

import pytest

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.club.domain.value_objects import Birthdate


class UserIdentifier(IntIdentifier):
    """An identifier for a user entity."""


@dataclass(frozen=True, eq=False, kw_only=True, slots=True)
class UserEntity(DataclassEntity):
    """A sample entity class."""

    ID: ClassVar[Type] = UserIdentifier

    name: str
    birthdate: Birthdate


def test_new_entity() -> None:
    """Test creating a new entity."""
    entity = UserEntity(
        name="Franky",
        birthdate=Birthdate(date=Date.create(1969, 3, 9)),
    )
    assert entity.id.is_empty(), "The identifier should be empty."


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


def test_shallow_dict(user_entity: UserEntity) -> None:
    """Test creating a shallow dictionary."""
    d = user_entity.shallow_dict()
    assert d == {
        "id": UserIdentifier(1),
        "name": "Franky",
        "birthdate": user_entity.birthdate,
        "traceable_time": user_entity.traceable_time,
    }
