"""Define common fixtures for Redis."""

import pytest
from redis.asyncio import Redis

from kwai.core.events.redis.stream import RedisStream


@pytest.fixture(scope="session")
async def redis() -> Redis:
    """Fixture for a redis instance."""
    redis = Redis(host="api.kwai.com")
    yield redis
    await redis.close()


@pytest.fixture(scope="session")
async def stream(redis: Redis) -> RedisStream:
    """Fixture for a redis stream.

    The stream will be deleted after the tests.
    """
    stream = RedisStream(redis, "kwai_test")
    yield stream
    await stream.delete()
