"""Tests for the Redis Consumer."""
from asyncio import sleep

import pytest

from kwai.core.events.redis.consumer import RedisConsumer
from kwai.core.events.redis.stream import RedisMessage, RedisStream


@pytest.mark.asyncio
async def test_consumer(stream: RedisStream):
    """Test the consumer."""
    await stream.create_group("kwai_test_group")
    await stream.add(RedisMessage(data={"text": "Hello consumer!"}))

    def out():
        out.counter = getattr(out, "counter", 0) + 1

    consumer = RedisConsumer(stream, "kwai_test_group", out)
    consumer.consume("kwai_test_consumer")

    await stream.add(RedisMessage(data={"text": "Hello runnable consumer!"}))
    await sleep(4)

    # noinspection PyUnresolvedReferences
    assert out.counter == 2, "The callback should be called twice"

    consumer.cancel()
