import asyncio
import inspect
from asyncio import Event
from typing import Callable, Awaitable

from kwai.core.events.redis.stream import RedisStream, RedisMessage


class RedisConsumer:
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
        await self._stream.create_group(self._group_name)

        while True:
            try:
                message = await self._stream.consume(
                    self._group_name, consumer_name, id_
                )
                if message:
                    try:
                        if inspect.iscoroutinefunction(self._callback):
                            if await self._callback(message):
                                await self._stream.ack(self._group_name, message.id)
                        else:
                            if self._callback(message):
                                await self._stream.ack(self._group_name, message.id)
                    except Exception as ex:
                        print(f"Exception: {ex}")
                        # avoid a break of the loop
                        continue
            except asyncio.CancelledError:
                # happens on shutdown, ignore
                return
            except Exception as ex:
                print(f"Exception: {ex}")
                continue
            finally:
                if self._is_stopping.is_set():
                    return
                await asyncio.sleep(1)

    def cancel(self):
        self._is_stopping.set()
