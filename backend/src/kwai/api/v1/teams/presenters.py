"""Module for defining presenters of the teams api."""

from kwai.api.v1.teams.schemas import TeamDocument, TeamMemberDocument
from kwai.core.domain.presenter import AsyncPresenter, IterableResult, Presenter
from kwai.core.json_api import JsonApiPresenter, Meta
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.domain.team_member import TeamMember


class JsonApiTeamPresenter(JsonApiPresenter[TeamDocument], Presenter[TeamEntity]):
    """A presenter that transform a team entity into a JSON:API document."""

    def present(self, team: TeamEntity) -> None:
        self._document = TeamDocument.create(team)


class JsonApiTeamsPresenter(
    JsonApiPresenter[TeamDocument], AsyncPresenter[IterableResult[TeamEntity]]
):
    """A presenter that transforms an iterator of teams into a JSON:API document."""

    async def present(self, result: IterableResult[TeamEntity]) -> None:
        self._document = TeamDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for team in result.iterator:
            team_document = TeamDocument.create(team)
            self._document.merge(team_document)


class JsonApiTeamMembersPresenter(
    JsonApiPresenter[TeamMemberDocument], Presenter[TeamEntity]
):
    """A presenter that transforms team members into a JSON:API document."""

    def present(self, use_case_result: TeamEntity) -> None:
        self._document = TeamMemberDocument(
            meta=Meta(count=len(use_case_result.members)),
            data=[],
        )
        for member in use_case_result.members:
            team_member_document = TeamMemberDocument.create(member)
            self._document.merge(team_member_document)


class JsonApiTeamMemberPresenter(
    JsonApiPresenter[TeamMemberDocument], Presenter[TeamMember]
):
    """A presenter that transforms a team member into a JSON:API document."""

    def present(self, use_case_result: TeamMember) -> None:
        self._document = TeamMemberDocument.create(use_case_result)
