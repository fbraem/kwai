"""Module for defining the use case "Create Page"."""
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.portal.applications.application import ApplicationIdentifier
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.page_command import PageCommand
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_repository import PageRepository

CreatePageCommand = PageCommand


class CreatePage:
    """Use case "Create Page"."""

    def __init__(
        self,
        repo: PageRepository,
        application_repo: ApplicationRepository,
        owner: Owner,
    ):
        """Initialize the use case.

        Args:
            repo: The repository for creating a page.
            owner: The user that owns the page.
            application_repo: The repository for getting the application.
        """
        self._repo = repo
        self._application_repo = application_repo
        self._owner = owner

    async def execute(self, command: CreatePageCommand) -> PageEntity:
        """Executes the use case.

        Args:
            command: the input for the use case.

        Raises:
            ApplicationNotFoundException: Raised when the application does not exist.
        """
        application = await self._application_repo.get_by_id(
            ApplicationIdentifier(command.application)
        )
        page = PageEntity(
            enabled=command.enabled,
            application=application,
            texts=[
                LocaleText(
                    locale=Locale(text.locale),
                    format=DocumentFormat(text.format),
                    title=text.title,
                    content=text.content,
                    summary=text.summary,
                    author=self._owner,
                )
                for text in command.texts
            ],
            priority=command.priority,
            remark=command.remark,
        )
        return await self._repo.create(page)
