"""Module that implements the 'get authors' use case."""

from dataclasses import dataclass

from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.portal.domain.author import AuthorEntity
from kwai.modules.portal.repositories.author_repository import AuthorRepository


@dataclass(kw_only=True, slots=True, frozen=True)
class GetAuthorsCommand:
    """Input for the use case."""

    limit: int = 0
    offset: int = 0


class GetAuthors:
    """Use case for getting authors."""

    def __init__(
        self,
        author_repo: AuthorRepository,
        presenter: AsyncPresenter[IterableResult[AuthorEntity]],
    ):
        """Initialize the use case.

        Args:
            author_repo: The repository for getting the authors.
            presenter: The presenter for authors.
        """
        self._author_repo = author_repo
        self._presenter = presenter

    async def execute(self, command: GetAuthorsCommand):
        """Execute the use case.

        Args:
            command: Input for the use case.
        """
        query = self._author_repo.create_query()

        await self._presenter.present(
            IterableResult(
                count=await query.count(),
                limit=command.limit,
                offset=command.offset,
                iterator=self._author_repo.get_all(
                    query, limit=command.limit, offset=command.offset
                ),
            )
        )
