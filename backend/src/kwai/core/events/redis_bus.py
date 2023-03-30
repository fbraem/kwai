"""Define a message bus using Redis."""
import asyncio
import inspect
from typing import Any, Callable

from redis import Redis

from kwai.core.events.bus import Bus
from kwai.core.events.consumer import RedisConsumer
from kwai.core.events.event import Event
from kwai.core.events.stream import RedisMessage, RedisStream


class RedisBus(Bus):
    """A message bus using Redis streams.

    The name of the event is mostly <module>.<entity>.<event>. Each module will have
    its own stream.
    """

    def __init__(self, redis: Redis):
        self._redis = redis
        self._events: dict[str, list[Callable[[dict[str, Any]], Any]]] = {}
        self._stream_names = set()
        self._consumers: list[RedisConsumer] = []

    async def publish(self, event: Event):
        """Publish the event.

        The event will be placed on the stream that belongs to the module.
        """
        stream_name = event.meta.name.split(".")[0]
        stream = RedisStream(self._redis, f"kwai.{stream_name}")
        await stream.add(RedisMessage(data=event.data))

    def subscribe(self, event: type[Event], task: Callable[[dict[str, Any]], Any]):
        """Subscribe a callback to an event.

        When an event is retrieved from a stream, the callback will be executed. For
        each stream, a consumer will be started when the bus is running.
        """
        if event.meta.name not in self._events:
            self._events[event.meta.name] = []
        stream_name = event.meta.name.split(".")[0]
        self._stream_names.add(f"kwai.{stream_name}")
        self._events[event.meta.name].append(task)

    async def _trigger_event(self, message: RedisMessage) -> bool:
        """Call all callbacks that are linked to the event."""
        if "meta" not in message.data:
            return False

        event_name = message.data["meta"]["name"]
        callbacks = self._events.get(event_name, [])
        if len(callbacks) == 0:
            print(f'No subscriptions found for event "f{event_name}"')
        for callback in callbacks:
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(message.data)
                else:
                    callback(message.data)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(f"Callback Exception: {ex}")

        return True

    async def run(self):
        """Start all consumers.

        For each stream a consumer will be started. This method will wait for all tasks
        to end.
        """
        tasks = []
        self._consumers = []
        for stream_name in self._stream_names:
            event_consumer = RedisConsumer(
                RedisStream(self._redis, stream_name),
                f"{stream_name}.group",
                self._trigger_event,
            )
            self._consumers.append(event_consumer)
            # noinspection PyAsyncCall
            tasks.append(
                asyncio.shield(event_consumer.consume(f"{stream_name}.consumer"))
            )
        await asyncio.gather(*tasks)

    async def cancel(self):
        """Cancel all consumers."""
        for task in self._consumers:
            task.cancel()
