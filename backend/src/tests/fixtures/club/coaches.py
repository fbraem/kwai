"""Module for defining fixtures for coaches."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.club.domain.coach import CoachEntity
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.repositories.coach_db_repository import CoachDbRepository


@pytest.fixture
def make_coach(make_member):
    """A factory fixture for a coach."""

    def _make_coach(
        member: MemberEntity | None = None,
        active: bool = True,
    ) -> CoachEntity:
        member = member or make_member()
        return CoachEntity(member=member or make_member(), active=active)

    return _make_coach


@pytest.fixture
def make_coach_in_db(
    request, event_loop, database: Database, make_coach, make_member_in_db
):
    """A factory fixture for a coach in a database."""

    async def _make_coach_in_db(
        coach: CoachEntity | None = None, member: MemberEntity | None = None
    ):
        member = member or await make_member_in_db()
        coach = coach or make_coach(member=member)
        repo = CoachDbRepository(database)
        async with UnitOfWork(database):
            coach = await repo.create(coach)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(coach)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return coach

    return _make_coach_in_db
