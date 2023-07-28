"""Module with tests for the access token database repository."""
import pytest

from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository

pytestmark = pytest.mark.db


def test_create(
    access_token: AccessTokenEntity,
):
    """Test the creation of an access_token."""
    assert access_token.id, "There should be an access token entity"


@pytest.mark.asyncio
async def test_get_by_token_identifier(
    access_token_repo: AccessTokenRepository,
    access_token: AccessTokenEntity,
):
    """Test get_by_token_identifier."""
    token = await access_token_repo.get_by_identifier(access_token.identifier)
    assert token, "There should be a refresh token"


@pytest.mark.asyncio
async def test_query(
    access_token_repo: AccessTokenRepository,
):
    """Test query."""
    tokens = [token async for token in access_token_repo.get_all(limit=10)]
    assert len(tokens) > 0, "There should be at least 1 token"
