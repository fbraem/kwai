"""Module that tests the Text value object."""
import dataclasses

import pytest

from kwai.core.domain.value_objects.content import Content, Text
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.unique_id import UniqueId


@pytest.fixture()
def content(locale: str):
    """Create a fixture for Content."""
    return Content(
        locale=locale,
        format="MD",
        title="Test",
        content="Test",
        summary="Test",
        author=Owner(
            id=IntIdentifier(1),
            uuid=UniqueId.generate(),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
    )


@pytest.mark.parametrize("locale", ["nl"])
def test_add_translation(locale, request):
    """Test the add_translation method."""
    content = request.getfixturevalue("content")
    text = Text().add_translation(content)
    assert text.contains_translation(
        locale
    ), f"There should be a translation available for {locale}"


@pytest.mark.parametrize("locale", ["nl"])
def test_remove_translation(locale, request):
    """Test the remove_translation method."""
    content = request.getfixturevalue("content")
    text = Text().add_translation(content).remove_translation(content)
    assert not text.contains_translation(
        locale
    ), f"There should be no translation available for {locale}"


@pytest.mark.parametrize("locale", ["nl"])
def test_replace_translation(locale, request):
    """Test the replace_translation method."""
    content = request.getfixturevalue("content")
    new_content = dataclasses.replace(content, content="Updated")
    text = Text().add_translation(content).replace_translation(new_content)
    assert text.contains_translation(
        locale
    ), f"There should be a translation available for {locale}"
    assert (
        text.get_translation(locale).content == "Updated"
    ), "The text should be updated"
