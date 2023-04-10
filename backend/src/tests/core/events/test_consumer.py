"""Tests for the Redis Consumer."""
import asyncio

import pytest

from kwai.core.events.consumer import RedisConsumer
from kwai.core.events.stream import RedisMessage, RedisStream


@pytest.mark.asyncio
async def test_consumer(stream: RedisStream):
    """Test the consumer."""
    await stream.create_group("kwai_test_consumer_group")
    await stream.add(RedisMessage(data={"text": "Hello consumer!"}))

    def out(message: RedisMessage) -> bool:  # pylint: disable=unused-argument
        out.counter = getattr(out, "counter", 0) + 1
        return True

    consumer = RedisConsumer(stream, "kwai_test_consumer_group", out)
    task = asyncio.create_task(consumer.consume("kwai_test_consumer"))
    await stream.add(RedisMessage(data={"text": "Hello runnable consumer!"}))
    try:
        await asyncio.wait_for(task, 4)
    except asyncio.TimeoutError:
        pass

    # noinspection PyUnresolvedReferences
    assert out.counter == 2, "The callback should be called twice"

    consumer.cancel()
