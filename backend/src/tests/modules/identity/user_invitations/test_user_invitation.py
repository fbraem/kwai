"""Module for testing the user invitation entity."""


def test_create(make_user_invitation) -> None:
    """Test creation of a user invitation."""
    user_invitation = make_user_invitation()
    assert user_invitation.is_expired is False, (
        "The user invitation should not be expired"
    )
    assert user_invitation.confirmed is False, (
        "The user invitation should not be confirmed"
    )
    assert user_invitation.mailed is False, "The user invitation should not be sent"


def test_confirmed(make_user_invitation):
    """Test confirmation of a user invitation."""
    user_invitation = make_user_invitation().confirm()
    assert user_invitation.confirmed, "The user invitation should be confirmed"


def test_revoke(make_user_invitation):
    """Test revoking of a user invitation."""
    user_invitation = make_user_invitation().revoke()
    assert user_invitation.revoked, "The user invitation should be revoked"
