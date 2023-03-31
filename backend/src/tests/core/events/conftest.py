"""Define common fixtures for Redis."""

import pytest
from redis.asyncio import Redis

from kwai.core.events.stream import RedisStream
from kwai.core.settings import get_settings


@pytest.fixture(scope="session")
async def redis() -> Redis:
    """Fixture for a redis instance."""
    settings = get_settings()
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
    )
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
