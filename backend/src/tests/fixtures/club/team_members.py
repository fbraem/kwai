"""Module for defining factory fixtures for team members."""

import pytest
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.teams.domain.team_member import TeamMemberEntity


@pytest.fixture
def make_team_member(make_member):
    """A factory fixture for a team member."""

    def _make_team_member(member: MemberEntity | None = None) -> TeamMemberEntity:
        member = member or make_member()
        return TeamMemberEntity(
            id_=member.id,
            uuid=member.uuid,
            name=member.name,
            license=member.license,
            birthdate=member.person.birthdate,
            nationality=member.person.nationality,
            gender=member.person.gender,
        )

    return _make_team_member
