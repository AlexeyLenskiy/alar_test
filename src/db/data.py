import asyncio
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models, settings
from src.db.settings import Base

# Data table columns
ID = "id"
NAME = "name"

# Sort order
ASC = "asc"
DESC = "desc"


def insert_string(start, stop) -> str:
    return "".join(f"({i}, 'Test{i}'), " for i in range(start, stop + 1))


def insert_data_values(i: int) -> str:
    string1 = insert_string(((i - 1) * 10) + 1, i * 10)
    string2 = insert_string(((3 + i - 1) * 10) + 1, (i + 3) * 10)
    return (string1 + string2)[:-2]


async def init_db():
    try:
        for i in (1, 2, 3):
            async with settings.db_pool as pool:
                pool.execute(f"DROP TABLE IF EXISTS data_{i}")
                pool.execute(
                    f'''
                    CREATE TABLE IF NOT EXISTS data_{i}
                    (id serial PRIMARY KEY, name VARCHAR(255) NOT NULL)
                    '''
                )
                pool.execute(
                    f'''
                    INSERT INTO data_{i}
                    (id, name)
                    VALUES
                    {insert_data_values(i)}
                    '''
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "db_init_failed", "message": f"{e}"})


async def get_data(db: AsyncSession, model: Base, sleep: int = 0) -> list[dict[str, Any]]:
    """
    Returns data from db tables.
    model -- table data model
    sleep -- wait time befor start (default 0)
    """
    try:
        await asyncio.sleep(sleep)
        results = await db.execute(select(model))
        return [{ID: _.id, NAME: _.name} for _ in results.scalars().all()]
    except asyncio.CancelledError:
        return []


def sort_data(
    data: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sorting data by column name and in sort order (default "name", "asc")"""
    return sorted(data, key=lambda k: k[ID])


async def get_sorted_data(
    db: AsyncSession,
    data_models: list[Base] = [models.Data1Model, models.Data2Model, models.Data3Model],
    sleep: int = 0,
    timeout: int = 2,
) -> list[dict[str, Any]]:
    """
    Return data from list of tables, sorted by column values.
    models -- list of table data models
    sleep -- wait time befor start (default 0)
    timeot -- connection timeot (default 2 seconds)
    """
    try:
        result = []
        for model in data_models:
            task = asyncio.create_task(get_data(db, model=model, sleep=sleep))
            data = await asyncio.wait_for(task, timeout=timeout)
            result += data
        return sort_data(result)

    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="TimeoutError")
    except Exception:
        raise
