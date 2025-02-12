"""Module for testing the refresh token database repository."""

import pytest

from kwai.modules.identity.tokens.refresh_token_repository import (
    RefreshTokenNotFoundException,
    RefreshTokenRepository,
)


pytestmark = pytest.mark.db


async def test_create(make_refresh_token_in_db):
    """Test the create method."""
    refresh_token = await make_refresh_token_in_db()
    assert refresh_token is not None, "There should be a refresh token entity"


async def test_get_by_token_identifier(
    refresh_token_repo: RefreshTokenRepository, make_refresh_token_in_db
):
    """Test get_by_token_identifier."""
    refresh_token = await make_refresh_token_in_db()
    token = await refresh_token_repo.get_by_token_identifier(refresh_token.identifier)
    assert token, "There should be a refresh token"


async def test_query(
    refresh_token_repo: RefreshTokenRepository,
    make_refresh_token_in_db,
):
    """Test query."""
    await make_refresh_token_in_db()
    tokens = [token async for token in refresh_token_repo.get_all(limit=10)]
    assert len(tokens) > 0, "There should be at least 1 token"


async def test_delete(
    refresh_token_repo: RefreshTokenRepository, make_refresh_token_in_db
):
    """Test delete."""
    refresh_token = await make_refresh_token_in_db()
    await refresh_token_repo.delete(refresh_token)

    with pytest.raises(RefreshTokenNotFoundException):
        await refresh_token_repo.get_by_token_identifier(refresh_token.identifier)
