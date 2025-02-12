"""Tests for the entity class."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier


UserIdentifier = IntIdentifier


class KwaiTestUserEntity(Entity[UserIdentifier]):
    """A sample entity class."""

    def __init__(
        self, *, name: str, id_: UserIdentifier | None = None, year_of_birth: int
    ):
        super().__init__(id_ or UserIdentifier(0))
        self._name = name
        self._year_of_birth = year_of_birth

    @property
    def name(self) -> str:
        """Return the name of the user."""
        return self._name

    @property
    def year_of_birth(self) -> int:
        """Return the year of birth."""
        return self._year_of_birth


def test_replace():
    """Test the replace classmethod."""
    user = KwaiTestUserEntity(name="Franky", year_of_birth=1969)
    new_user = Entity.replace(user, id_=UserIdentifier(2), name="Bart")

    assert new_user.id.value == 2, "The id should be 2"
    assert new_user.name == "Bart", "The name should be 'Bart'"
    assert new_user.year_of_birth == 1969, "Year of birth should be 1969"
