"""Module for the use case "Update Page"."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.portal.applications.application import ApplicationIdentifier
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.page_command import PageCommand
from kwai.modules.portal.pages.page import PageEntity, PageIdentifier
from kwai.modules.portal.pages.page_repository import PageRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdatePageCommand(PageCommand):
    """Input for the "Update Page" use case."""

    id: int


class UpdatePage:
    """Use case for updating a page."""

    def __init__(
        self,
        repo: PageRepository,
        application_repo: ApplicationRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: A repository for updating pages.
            application_repo: A repository for getting the application.
            owner: The owner of the page.
        """
        self._repo = repo
        self._application_repo = application_repo
        self._owner = owner

    async def execute(self, command: UpdatePageCommand) -> PageEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            PageNotFoundException: When the page does not exist.
            ApplicationNotFoundException: When the application does not exist.
        """
        page = await self._repo.get_by_id(PageIdentifier(command.id))
        application = await self._application_repo.get_by_id(
            ApplicationIdentifier(command.application)
        )

        page = Entity.replace(
            page,
            enabled=command.enabled,
            application=application,
            texts=[
                LocaleText(
                    locale=Locale(text.locale),
                    format=DocumentFormat(text.format),
                    title=text.locale,
                    content=text.content,
                    summary=text.summary,
                    author=self._owner,
                )
                for text in command.texts
            ],
            priority=command.priority,
            remark=command.remark,
            traceable_time=page.traceable_time.mark_for_update(),
        )

        await self._repo.update(page)

        return page
