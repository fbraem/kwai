"""Define common fixtures for Redis."""

import pytest

from redis.asyncio import Redis

from kwai.core.events.stream import RedisStream


@pytest.fixture(scope="module")
async def stream(redis: Redis) -> RedisStream:
    """Fixture for a redis stream.

    The stream will be deleted after the tests.
    """
    stream = RedisStream(redis, "kwai_test")
    yield stream
    await stream.delete()
