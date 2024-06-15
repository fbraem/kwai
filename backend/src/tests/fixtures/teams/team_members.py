"""Module for defining factory fixtures for team members."""

import pytest
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.teams.domain.team_member import MemberEntity, TeamMember


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
