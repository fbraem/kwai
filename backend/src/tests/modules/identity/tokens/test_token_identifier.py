"""Module for testing TokenIdentifier."""
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


def test_generate():
    """Test generate."""
    token_id = TokenIdentifier.generate()
    assert len(str(token_id)) == 80, "The generated token should contain 80 characters."
