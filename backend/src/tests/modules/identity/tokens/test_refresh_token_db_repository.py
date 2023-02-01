"""Module for testing the refresh token database repository."""
import pytest

from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository

pytestmark = pytest.mark.integration


def test_create(
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test the create method."""
    assert not refresh_token.id.is_empty(), "There should be a refresh token entity"


def test_get_by_token_identifier(
    refresh_token_repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test get_by_token_identifier."""
    token = refresh_token_repo.get_by_token_identifier(refresh_token.identifier)
    assert token, "There should be a refresh token"


def test_query(
    refresh_token_repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
):
    """Test query."""
    tokens = list(refresh_token_repo.get_all(limit=10))
    assert len(tokens) > 0, "There should be at least 1 token"
