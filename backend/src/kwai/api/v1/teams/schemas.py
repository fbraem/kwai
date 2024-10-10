"""Module that defines the schemas for the teams API."""

from typing import Annotated, Self

from pydantic import BaseModel, Field

from kwai.api.schemas.resources import TeamResourceIdentifier
from kwai.api.v1.resources import CountryResourceIdentifier
from kwai.api.v1.schemas import CountryDocument, CountryResource
from kwai.api.v1.teams.resources import TeamMemberResourceIdentifier
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.domain.team_member import TeamMember


class TeamMemberAttributes(BaseModel):
    """Attributes for a team member."""

    active: bool
    first_name: str
    last_name: str
    license_number: str
    license_end_date: str
    gender: int
    birthdate: str


class TeamMemberRelationships(BaseModel):
    """Relationships for a team member JSON:API resource."""

    nationality: Relationship[CountryResourceIdentifier]
    team: Relationship[TeamResourceIdentifier] | None = None


class TeamMemberResource(
    TeamMemberResourceIdentifier,
    ResourceData[TeamMemberAttributes, TeamMemberRelationships],
):
    """A JSON:API resource for a team member."""


TeamMemberInclude = Annotated[CountryResource, Field(discriminator="type")]


class TeamMemberDocument(Document[TeamMemberResource, TeamMemberInclude]):
    """A JSON:API document for one or more team members."""

    @classmethod
    def create(cls, team_member: TeamMember, team: TeamEntity | None = None) -> Self:
        """Create a team member document."""
        nationality_document = CountryDocument.create(team_member.member.nationality)

        team_member_resource = TeamMemberResource(
            id=str(team_member.member.uuid),
            attributes=TeamMemberAttributes(
                active=team_member.active,
                first_name=team_member.member.name.first_name,
                last_name=team_member.member.name.last_name,
                license_number=team_member.member.license.number,
                license_end_date=str(team_member.member.license.end_date),
                gender=team_member.member.gender,
                birthdate=str(team_member.member.birthdate),
            ),
            meta=ResourceMeta(
                created_at=str(team_member.traceable_time.created_at),
                updated_at=str(team_member.traceable_time.updated_at),
            ),
        )
        team_member_resource.relationships = TeamMemberRelationships(
            nationality=Relationship[CountryResourceIdentifier](
                data=CountryResourceIdentifier(id=nationality_document.resource.id),
            ),
            team=(
                None
                if team is None
                else Relationship[TeamResourceIdentifier](
                    data=TeamResourceIdentifier(id=team.id)
                )
            ),
        )

        return cls(data=team_member_resource, included={nationality_document.resource})


class TeamAttributes(BaseModel):
    """Attributes for the team JSON:API resource."""

    name: str
    active: bool
    remark: str


class TeamRelationships(BaseModel):
    """Relationships for a team JSON:API resource."""

    team_members: Relationship[TeamMemberResourceIdentifier]


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
        for team_member in team.members.values():
            team_member_document.merge(TeamMemberDocument.create(team_member))

        team_resource = TeamResource(
            id=str(team.id),
            attributes=TeamAttributes(
                name=team.name, active=team.is_active, remark=team.remark
            ),
            relationships=TeamRelationships(
                team_members=Relationship[TeamMemberResourceIdentifier](
                    data=team_member_document.resources
                )
            ),
        )

        included: set[TeamInclude] = set(team_member_document.resources)
        included = included.union(team_member_document.included)

        return TeamDocument(data=team_resource, included=included)
