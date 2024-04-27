"""Module for testing the functions in functions.py."""

from kwai.core.functions import async_groupby, generate_filenames


async def test_async_groupby():
    """Test async_groupby method."""

    async def _generate_group():
        yield "A", 1
        yield "A", 2
        yield "B", 3
        yield "C", 4
        yield "C", 5

    it = async_groupby(_generate_group(), lambda x: x[0])
    groups = {key: group async for key, group in it}

    assert groups["A"] == [("A", 1), ("A", 2)]
    assert groups["B"] == [("B", 3)]
    assert groups["C"] == [("C", 4), ("C", 5)]


def test_generate_filenames():
    """Test generate_filenames."""
    filename_generator = generate_filenames("test_", ".csv")

    assert next(filename_generator) == "test_001.csv"
    assert next(filename_generator) == "test_002.csv"
    assert next(filename_generator) == "test_003.csv"


def test_generate_filenames_with_shorter_suffix():
    """Test generate_filenames."""
    filename_generator = generate_filenames("test_", ".csv", 2)

    assert next(filename_generator) == "test_01.csv"
    assert next(filename_generator) == "test_02.csv"
    assert next(filename_generator) == "test_03.csv"
