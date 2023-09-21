from pytest import mark
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from src.db import models
from src.db.data import (
    get_sorted_data,
    get_data,
    sort_data
)


class MockDataModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name


async def mock_execute(_):
    class MockResult:
        def scalars(self):
            return self

        def all(self):
            return [MockDataModel(i, f"Test{i}") for i in range(1, 11)]

    return MockResult()


@pytest.mark.asyncio
@patch.object(AsyncSession, 'execute', AsyncMock(side_effect=mock_execute))
async def test_get_data():
    data = await get_data(AsyncSession(), models.Data1Model)
    assert len(data) == 10
    assert data == [{"id": i, "name": f"Test{i}"} for i in range(1, 11)]


def test_sort_data() -> None:
    assert sort_data(
        data=[{"id": i, "name": f"Test{i}"} for i in (1, 7, 0, 5, 2, 3, 6, 9, 4, 8, 11, 10)]
    ) == [{"id": i, "name": f"Test{i}"} for i in range(0, 12)]


@pytest.mark.asyncio
@mark.parametrize("sleep", [0.001, 0.7, 1.9])
@patch.object(AsyncSession, 'execute', AsyncMock(side_effect=mock_execute))
async def test_get_sorted_data_delay_less_then_timeout(sleep) -> None:
    result = await get_sorted_data(AsyncSession(), sleep=sleep, timeout=2)
    assert len(result) == 30


@pytest.mark.asyncio
@mark.parametrize("sleep", [2, 2.001, 3])
@patch.object(AsyncSession, 'execute', AsyncMock(side_effect=mock_execute))
async def test_get_sorted_data_connection_timeout_error_result(sleep) -> None:
    assert await get_sorted_data(AsyncSession(), sleep=sleep, timeout=2) == []
