"""Tests for the Redis streams."""

import pytest

from kwai.core.events.stream import RedisMessage, RedisStream


pytestmark = pytest.mark.bus


async def test_add(stream: RedisStream):
    """Test adding a message to a stream."""
    message = await stream.add(RedisMessage(data={"text": "Hello World!"}))
    assert message.id != "*", "There should be a message id"


async def test_read(stream: RedisStream):
    """Test reading a message from a stream."""
    message = await stream.read(last_id="0")
    assert message is not None, "There should be a message"
    assert "text" in message.data, "There should be a text key in the message data"
    assert message.data["text"] == "Hello World!", (
        "There should be 'Hello World!' in the message content"
    )


async def test_info(stream: RedisStream):
    """Test the info method."""
    info = await stream.info()
    assert info is not None, "There should be a result"


async def test_create_group(stream: RedisStream):
    """Test creating a group."""
    result = await stream.create_group("kwai_test_group")
    assert result is True, "The group should be created"


async def test_get_groups(stream: RedisStream):
    """Test getting all groups of a stream."""
    groups = await stream.get_groups()
    assert groups is not None, "There should be a result"
    assert "kwai_test_group" in groups, "kwai_test_group should exist"


async def test_get_group(stream: RedisStream):
    """Test getting one group of a stream."""
    group = await stream.get_group("kwai_test_group")
    assert group is not None, "There should be a group"
    assert group.name == "kwai_test_group", "There should be a kwai_test_group"


async def test_consume(stream: RedisStream):
    """Test adding a message to a stream."""
    await stream.add(RedisMessage(data={"text": "Hello Consuming World!"}))
    message = await stream.consume("kwai_test_group", "kwai_test_group.c1")
    assert message is not None, "There should be a message"
