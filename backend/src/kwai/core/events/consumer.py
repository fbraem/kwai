"""Module that implements a consumer for a redis stream."""
import asyncio
import inspect
from asyncio import Event
from typing import Callable, Awaitable

from kwai.core.events.stream import RedisStream, RedisMessage


class RedisConsumer:
    """A consumer for a Redis stream.

    Attributes:
        _stream: The stream to consume.
        _group_name: The name of the group.
        _callback: The callback to call when a message is consumed.
        _is_stopping: An event to stop the consumer.
    """

    def __init__(
        self,
        stream: RedisStream,
        group_name: str,
        callback: Callable[[RedisMessage], bool | Awaitable[bool]],
    ):
        self._stream = stream
        self._group_name = group_name
        self._callback = callback
        self._is_stopping = Event()

    async def consume(self, consumer_name: str, id_: str = ">"):
        """Consume messages from a stream.

        Args:
            consumer_name: The name of the consumer.
            id_: The id to start consuming (default is >).
        """
        await self._stream.create_group(self._group_name)

        while True:
            try:
                message = await self._stream.consume(
                    self._group_name, consumer_name, id_
                )
                if message:
                    try:
                        await self._trigger_callback(message)
                    except Exception as ex:  # pylint: disable=broad-exception-caught
                        print(f"Exception: {ex}")
                        # avoid a break of the loop
                        continue
            except asyncio.CancelledError:
                # happens on shutdown, ignore
                return
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(f"Exception: {ex}")
                continue
            finally:
                if self._is_stopping.is_set():
                    return  # pylint: disable=lost-exception
                await asyncio.sleep(1)

    def cancel(self):
        """Cancel the consumer."""
        self._is_stopping.set()

    async def _trigger_callback(self, message: RedisMessage):
        if inspect.iscoroutinefunction(self._callback):
            result = await self._callback(message)
        else:
            result = self._callback(message)
        if result:
            await self._stream.ack(self._group_name, message.id)