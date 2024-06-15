"""Module that defines the schemas for the teams API."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.schemas.resources import TeamResourceIdentifier
from kwai.api.v1.club.schemas.country import CountryDocument, CountryResource
from kwai.api.v1.club.schemas.resources import (
    CountryResourceIdentifier,
    MemberResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.domain.team_member import MemberEntity


class TeamMemberAttributes(BaseModel):
    """Attributes for a team member."""

    first_name: str
    last_name: str
    license_number: str
    license_end_date: str
    gender: int
    birthdate: str


class TeamMemberRelationships(BaseModel):
    """Relationships for a team member JSON:API resource."""

    nationality: Relationship[CountryResourceIdentifier]


class TeamMemberResource(
    MemberResourceIdentifier,
    ResourceData[TeamMemberAttributes, TeamMemberRelationships],
):
    """A JSON:API resource for a team member."""


TeamMemberInclude = Annotated[CountryResource, Field(discriminator="type")]


class TeamMemberDocument(Document[TeamMemberResource, TeamMemberInclude]):
    """A JSON:API document for one or more team members."""

    @classmethod
    def create(cls, team_member: MemberEntity) -> Self:
        """Create a team member document."""
        nationality_document = CountryDocument.create(team_member.nationality)

        team_member_resource = TeamMemberResource(
            id=str(team_member.uuid),
            attributes=TeamMemberAttributes(
                first_name=team_member.name.first_name,
                last_name=team_member.name.last_name,
                license_number=team_member.license.number,
                license_end_date=str(team_member.license.end_date),
                gender=team_member.gender,
                birthdate=str(team_member.birthdate),
            ),
        )
        team_member_resource.relationships = TeamMemberRelationships(
            nationality=Relationship[CountryResourceIdentifier](
                data=CountryResourceIdentifier(id=nationality_document.resource.id),
            )
        )

        return cls(data=team_member_resource, included={nationality_document.resource})


class TeamAttributes(BaseModel):
    """Attributes for the team JSON:API resource."""

    name: str
    active: bool
    remark: str


class TeamRelationships(BaseModel):
    """Relationships for a team JSON:API resource."""

    members: Relationship[MemberResourceIdentifier]


class TeamResource(
    TeamResourceIdentifier, ResourceData[TeamAttributes, TeamRelationships]
):
    """A JSON:API resource for a team."""


TeamInclude = Annotated[
    TeamMemberResource | CountryResource, Field(discriminator="type")
]


class TeamDocument(Document[TeamResource, TeamInclude]):
    """A JSON:API document for one or more teams."""

    @classmethod
    def create(cls, team: TeamEntity) -> Self:
        """Create a team document from a team entity."""
        team_member_document = TeamMemberDocument(data=[], included=set())
        for team_member in team.members:
            team_member_document.merge(TeamMemberDocument.create(team_member))

        team_resource = TeamResource(
            id=str(team.id),
            attributes=TeamAttributes(
                name=team.name, active=team.is_active, remark=team.remark
            ),
            relationships=TeamRelationships(
                members=Relationship[MemberResourceIdentifier](
                    data=team_member_document.resources
                )
            ),
        )

        included: set[TeamInclude] = set(team_member_document.resources)
        included = included.union(team_member_document.included)

        return TeamDocument(data=team_resource, included=included)
