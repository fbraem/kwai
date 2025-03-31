"""Module that defines presenters for the auth api."""

from kwai.api.v1.auth.schemas.revoked_user import RevokedUserDocument
from kwai.api.v1.auth.schemas.user_account import (
    UserAccountDocument,
    UserAccountResource,
    UserAccountsDocument,
)
from kwai.core.domain.presenter import AsyncPresenter, IterableResult, Presenter
from kwai.core.json_api import JsonApiPresenter, Meta
from kwai.modules.identity.users.user_account import UserAccountEntity


class JsonApiUserAccountsPresenter(
    JsonApiPresenter[UserAccountsDocument],
    AsyncPresenter[IterableResult[UserAccountEntity]],
):
    """A presenter that transform an iterable list of user account entities into a JSON:API document."""

    async def present(self, result: IterableResult[UserAccountEntity]) -> None:
        self._document = UserAccountsDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for user_account in result.iterator:
            self._document.merge(
                UserAccountDocument(data=UserAccountResource.create(user_account))
            )


class JsonApiUserAccountPresenter(
    JsonApiPresenter[UserAccountDocument], Presenter[UserAccountEntity]
):
    """A presenter that transforms a user account entity into a JSON:API document."""

    def present(self, result: UserAccountEntity) -> None:
        self._document = UserAccountDocument(data=UserAccountResource.create(result))


class JsonApiRevokedUserPresenter(
    JsonApiPresenter[RevokedUserDocument],
    Presenter[UserAccountEntity],
):
    """A presenter that transform a user account entity into a JSON:API document.

    The document will be a [RevokedUserDocument].
    """

    def present(self, use_case_result: UserAccountEntity) -> None:
        self._document = RevokedUserDocument.create(use_case_result)
