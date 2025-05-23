"""Module for defining factory fixtures for team members."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.domain.team_member import MemberEntity, TeamMember
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository


@pytest.fixture
def make_team_member(make_member):
    """A factory fixture for a team member."""

    def _make_team_member(member: MemberEntity | None = None) -> TeamMember:
        member = member or make_member()
        return TeamMember(
            active=True,
            member=MemberEntity(
                id_=member.id,
                uuid=member.uuid,
                name=member.name,
                license=member.license,
                birthdate=member.person.birthdate,
                nationality=member.person.nationality,
                gender=member.person.gender,
            ),
            traceable_time=TraceableTime(),
        )

    return _make_team_member


@pytest.fixture
def make_team_member_in_db(
    database: Database, make_team_member, make_member_in_db, make_team_in_db
):
    """A factory fixture for a team member in a database."""

    async def _make_team_member_in_db(
        member: MemberEntity | None = None, team: TeamEntity | None = None
    ) -> TeamMember:
        member = member or make_team_member(await make_member_in_db())
        team = team or await make_team_in_db()
        if team is not None:
            await TeamDbRepository(database).add_team_member(team, member)
        return member

    return _make_team_member_in_db
