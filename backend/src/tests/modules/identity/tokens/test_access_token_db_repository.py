"""Module with tests for the access token database repository."""

import pytest

from kwai.modules.identity.tokens.access_token_repository import (
    AccessTokenNotFoundException,
    AccessTokenRepository,
)


pytestmark = pytest.mark.db


async def test_create(make_access_token_in_db):
    """Test the creation of an access_token."""
    access_token = await make_access_token_in_db()
    assert access_token is not None, "There should be an access token entity"


async def test_get_by_token_identifier(
    access_token_repo: AccessTokenRepository,
    make_access_token_in_db,
):
    """Test get_by_token_identifier."""
    access_token = await make_access_token_in_db()
    token = await access_token_repo.get_by_identifier(access_token.identifier)
    assert token, "There should be a refresh token"


async def test_query(
    access_token_repo: AccessTokenRepository,
):
    """Test query."""
    tokens = [token async for token in access_token_repo.get_all(limit=10)]
    assert len(tokens) > 0, "There should be at least 1 token"


async def test_delete(
    access_token_repo: AccessTokenRepository, make_access_token_in_db
):
    """Test delete."""
    access_token = await make_access_token_in_db()
    await access_token_repo.delete(access_token)

    with pytest.raises(AccessTokenNotFoundException):
        await access_token_repo.get_by_identifier(access_token.identifier)
