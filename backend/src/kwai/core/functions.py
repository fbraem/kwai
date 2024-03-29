"""Module that defines some common functions."""
from typing import Any, AsyncIterator, Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def async_groupby(
    it: AsyncIterator[T], key: Callable[[T], R]
) -> AsyncIterator[tuple[Any, list[T]]]:
    """An async groupby."""
    try:
        row = await anext(it)
    except StopAsyncIteration:
        return

    group: list[T] = [row]
    current_key = key(row)

    # Process all other rows
    async for row in it:
        new_key = key(row)
        if new_key != current_key:
            yield current_key, group
            group = [row]
            current_key = new_key
        else:
            group.append(row)

    yield current_key, group
