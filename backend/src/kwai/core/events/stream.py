"""Define a Redis stream."""
import json
from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import Any

import redis.exceptions
from redis.asyncio import Redis


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisStreamInfo:
    """Dataclass with information about a redis stream."""

    length: int
    first_entry: str
    last_entry: str


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisGroupInfo:
    """Dataclass with information about a redis stream group."""

    name: str
    consumers: int
    pending: int
    last_delivered_id: str


class RedisMessageException(Exception):
    """Exception raised when the message is not a RedisMessage."""

    def __init__(self, stream_name: str, message_id: str, message: str):
        self._stream_name = stream_name
        self._message_id = message_id
        super().__init__(message)

    @property
    def stream_name(self) -> str:
        """Return the stream of the message."""
        return self._stream_name

    @property
    def message_id(self) -> str:
        """Return the message id of the message that raised this exception."""
        return self._message_id

    def __str__(self):
        """Return a string representation of this exception."""
        return f"({self._stream_name} - {self._message_id}) " + super().__str__()


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisMessage:
    """Dataclass for a message on a stream."""

    stream: str | None = None
    id: str = "*"
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create_from_redis(cls, messages: list) -> "RedisMessage":
        """Create a RedisMessage from messages retrieved from a Redis stream."""
        # A nested list is returned from Redis. For each stream (we only have one here),
        # a list of entries read is returned. Because count was 1, this contains only 1
        # element. An entry is a tuple with the message id and the message content.
        message = messages[0]  # we only have one stream, so use index 0
        stream_name = message[0].decode("utf-8")
        message = message[1]  # This is a list with all returned tuple entries
        message_id = message[0][0].decode("utf-8")
        if b"data" in message[0][1]:
            try:
                json.loads(message[0][1][b"data"])
            except JSONDecodeError as ex:
                raise RedisMessageException(stream_name, message_id, str(ex)) from ex
            return RedisMessage(
                stream=stream_name,
                id=message_id,
                data=json.loads(message[0][1][b"data"]),
            )
        raise RedisMessageException(
            stream_name, message_id, "No data key found in redis message"
        )


class RedisStream:
    """A stream using Redis.

    Attributes:
        _redis: Redis connection.
        _stream_name: Name of the Redis stream.

    A stream will be created when a first group is created or when a first message is
    added.
    """

    def __init__(self, redis_: Redis, stream_name: str):
        self._redis = redis_
        self._stream_name = stream_name

    @property
    def name(self) -> str:
        """Return the name of the stream."""
        return self._stream_name

    async def ack(self, group_name: str, id_: str):
        """Acknowledge the message with the given id for the given group.

        Args:
            group_name: The name of the group.
            id_: The id of the message to acknowledge.
        """
        await self._redis.xack(self._stream_name, group_name, id_)

    async def add(self, message: RedisMessage) -> RedisMessage:
        """Add a new message to the stream.

        Args:
            message: The message to add to the stream.

        Returns:
            The original message. When the id of the message was a *, the id returned
            from redis will be set.

        The data will be serialized to JSON. The field 'data' will be used to store
        this JSON.
        """
        message_id = await self._redis.xadd(
            self._stream_name, {"data": json.dumps(message.data)}, id=message.id
        )
        return RedisMessage(id=message_id.decode("utf-8"), data=message.data)

    async def consume(
        self, group_name: str, consumer_name: str, id_=">", block: int | None = None
    ) -> RedisMessage | None:
        """Consume a message from a stream.

        Args:
            group_name: Name of the group.
            consumer_name: Name of the consumer.
            id_: The id to start from (default is >)
            block: milliseconds to wait for an entry. Use None to not block.
        """
        messages = await self._redis.xreadgroup(
            group_name, consumer_name, {self._stream_name: id_}, 1, block
        )
        if messages is None:
            return
        if len(messages) == 0:
            return

        # Check if there is a message returned for our stream.
        _, stream_messages = messages[0]
        if len(stream_messages) == 0:
            return

        return RedisMessage.create_from_redis(messages)

    async def create_group(self, group_name: str, id_="$") -> bool:
        """Create a group (if it doesn't exist yet).

        Args:
            group_name: The name of the group
            id_: The id used as starting id. Default is $, which means only
                new messages.

        Returns:
            True, when the group is created, False when the group already exists.

        When the stream does not exist yet, it will be created.
        """
        try:
            await self._redis.xgroup_create(self._stream_name, group_name, id_, True)
            return True
        except redis.ResponseError:
            return False

    async def delete(self) -> bool:
        """Delete the stream.

        Returns:
            True when the stream is deleted. False when the stream didn't exist or
            isn't deleted.
        """
        result = await self._redis.delete(self._stream_name)
        return result == 1

    async def delete_entries(self, *ids) -> int:
        """Delete entries from the stream.

        Returns the number of deleted entries.
        """
        return await self._redis.xdel(self._stream_name, *ids)

    async def get_group(self, group_name: str) -> RedisGroupInfo | None:
        """Get the information about a group.

        Returns:
            RedisGroup when the group exist, otherwise None is returned.
        """
        groups = await self.get_groups()
        return groups.get(group_name, None)

    async def get_groups(self) -> dict[str, RedisGroupInfo]:
        """Get all groups of the stream.

        Returns:
            A list of groups.
        """
        result = {}
        groups = await self._redis.xinfo_groups(self._stream_name)
        for group in groups:
            group_name = group["name"].decode("utf-8")
            result[group_name] = RedisGroupInfo(
                name=group_name,
                consumers=group["consumers"],
                pending=group["pending"],
                last_delivered_id=group["last-delivered-id"].decode("utf-8"),
            )

        return result

    async def first_entry_id(self) -> str:
        """Return the id of the first entry.

        An empty string will be returned when there is no entry on the stream.
        """
        result = await self.info()
        if result is None:
            return ""
        return result.first_entry

    async def info(self) -> RedisStreamInfo | None:
        """Return information about the stream.

        Returns:
            A tuple with length, first-entry-id and last-entry-id. None is returned
            when the stream does not exist.
        """
        try:
            result = await self._redis.xinfo_stream(self._stream_name)
            return RedisStreamInfo(
                length=result["length"],
                first_entry=result["first-entry"][0].decode("utf-8"),
                last_entry=result["last-entry"][0].decode("utf-8"),
            )
        except redis.exceptions.ResponseError:
            return None

    async def last_entry_id(self) -> str:
        """Return the id of the last entry.

        An empty string will be returned when there is no entry on the stream.
        """
        result = await self.info()
        if result is None:
            return ""
        return result.last_entry

    async def length(self):
        """Return the number of entries on the stream.

        0 will be returned when the stream does not exist.
        """
        result = await self.info()
        if result is None:
            return 0
        return result.length

    async def read(
        self, last_id: str = "$", block: int | None = None
    ) -> RedisMessage | None:
        """Read an entry from the stream.

        Args:
            last_id: only entries with an id greater than this id will be returned.
                The default is $, which means to return only new entries.
            block: milliseconds to wait for an entry. Use None to not block.

        Returns:
            None when no entry is read. A tuple with the id and data of the entry
            when an entry is read.
        """
        messages = await self._redis.xread({self._stream_name: last_id}, 1, block)
        if messages is None:  # No message read
            return
        if len(messages) == 0:
            return

        return RedisMessage.create_from_redis(messages)
