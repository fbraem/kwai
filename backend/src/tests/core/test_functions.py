from kwai.core.functions import async_groupby


async def test_async_groupby():
    """Test async_groupby method."""

    async def _generate_group():
        yield "A", 1
        yield "A", 2
        yield "B", 3
        yield "C", 4
        yield "C", 5

    it = async_groupby(_generate_group(), lambda x: x[0])
    async for group in it:
        print(group)
