"""Module that implements a consumer for a redis stream."""

import asyncio
import inspect

from asyncio import Event
from typing import Awaitable, Callable

from kwai.core.events.stream import RedisMessage, RedisStream


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

    async def consume(self, consumer_name: str, check_backlog: bool = True):
        """Consume messages from a stream.

        Args:
            consumer_name: The name of the consumer.
            check_backlog: When True, all pending messages will be processed first.
        """
        await self._stream.create_group(self._group_name)

        while True:
            if check_backlog:
                id_ = "0-0"
            else:
                id_ = ">"
            try:
                message = await self._stream.consume(
                    self._group_name, consumer_name, id_
                )
                if message:
                    try:
                        await self._trigger_callback(message)
                    except Exception as ex:
                        print(f"Exception: {ex!r}")
                        # avoid a break of the loop
                        continue
                else:
                    check_backlog = False
            except asyncio.CancelledError:
                # happens on shutdown, ignore
                return
            except Exception as ex:
                print(f"Exception: {ex}")
                continue
            finally:
                if self._is_stopping.is_set():
                    return  # noqa
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
