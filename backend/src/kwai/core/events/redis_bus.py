"""Module for defining a publisher using Redis."""
import asyncio
import inspect
from typing import Any, Callable

from loguru import logger
from redis.asyncio import Redis

from kwai.core.events.consumer import RedisConsumer
from kwai.core.events.event import Event, EventMeta
from kwai.core.events.publisher import Publisher
from kwai.core.events.stream import RedisMessage, RedisStream
from kwai.core.events.subscriber import Subscriber


class RedisBus(Publisher, Subscriber):
    """An event bus using Redis streams."""

    def __init__(self, redis: Redis):
        self._redis = redis
        self._consumers = []

    async def publish(self, event: Event):
        stream_name = self._get_stream_name(event.meta)
        logger.info(f"Publishing event to {stream_name}")
        stream = RedisStream(self._redis, stream_name)
        await stream.add(RedisMessage(data=event.data))

    def subscribe(
        self, event: type[Event], task: Callable[[dict[str, Any]], Any]
    ) -> None:
        stream_name = self._get_stream_name(event.meta)
        self._consumers.append(
            RedisConsumer(
                RedisStream(self._redis, stream_name),
                task.__qualname__,
                RedisBus._create_event_trigger(event, task),
            )
        )

    @classmethod
    def _create_event_trigger(
        cls, event: type[Event], task: Callable[[dict[str, Any]], Any]
    ):
        """Create an event trigger."""

        async def trigger(message: RedisMessage) -> bool:
            with logger.contextualize(
                stream=RedisBus._get_stream_name(event.meta), message_id=message.id
            ):
                try:
                    if inspect.iscoroutinefunction(task):
                        await task(message.data)
                    else:
                        task(message.data)
                except Exception as ex:
                    logger.warning(f"The handler raised an exception: {ex}")
                    return False
                return True

        return trigger

    async def run(self):
        """Start all consumers.

        For each stream a consumer will be started. This method will wait for all tasks
        to end.
        """
        tasks = []
        for index, consumer in enumerate(self._consumers):
            # noinspection PyAsyncCall
            tasks.append(asyncio.shield(consumer.consume(f"consumer-{index}")))
        await asyncio.gather(*tasks)

    async def cancel(self):
        """Cancel all consumers."""
        for task in self._consumers:
            task.cancel()

    @classmethod
    def _get_stream_name(cls, meta: EventMeta) -> str:
        """Get the stream name for the given event."""
        return f"kwai.{meta.version}.{meta.module}.{meta.name}"
