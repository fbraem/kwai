"""Module for common fixtures used for testing code of the club module."""

import pytest
from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.domain.team import TeamEntity

from tests.fixtures.club.coaches import *  # noqa
from tests.fixtures.club.contacts import *  # noqa
from tests.fixtures.club.countries import *  # noqa
from tests.fixtures.club.members import *  # noqa
from tests.fixtures.club.persons import *  # noqa
from tests.fixtures.teams.team_members import *  # noqa
from tests.fixtures.teams.teams import *  # noqa


class DummyPresenter(Presenter[TeamEntity]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._entity = None

    @property
    def entity(self):
        """Return the entity."""
        return self._entity

    def present(self, use_case_result: TeamEntity) -> None:
        self._entity = use_case_result


@pytest.fixture
def team_presenter() -> DummyPresenter:
    """A fixture for a team presenter."""
    return DummyPresenter()
