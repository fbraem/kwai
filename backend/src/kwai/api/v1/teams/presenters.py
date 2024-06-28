"""Module for defining presenters of the teams api."""

from kwai.api.v1.teams.schemas import TeamDocument
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.core.json_api import JsonApiPresenter, Meta
from kwai.modules.teams.domain.team import TeamEntity


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
