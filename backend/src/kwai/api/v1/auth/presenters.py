"""Module that defines presenters for the auth api."""

from kwai.api.v1.auth.schemas.user_account import UserAccountDocument
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.core.json_api import JsonApiPresenter, Meta
from kwai.modules.identity.users.user_account import UserAccountEntity


class JsonApiUserAccountsPresenter(
    JsonApiPresenter[UserAccountDocument],
    AsyncPresenter[IterableResult[UserAccountEntity]],
):
    """A presenter that transform a user account entity into a JSON:API document."""

    async def present(self, result: IterableResult[UserAccountEntity]) -> None:
        self._document = UserAccountDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for user_account in result.iterator:
            user_account_document = UserAccountDocument.create(user_account)
            self._document.merge(user_account_document)
