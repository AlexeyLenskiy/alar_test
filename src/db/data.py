import asyncio
from fastapi import HTTPException
from src.db import settings
from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.settings import Base

def insert_data_values(i: int) -> str:
    values = ""
    range_1 = [(i - 1) * 10, i * 10]
    range_2 = [(i + 2) * 10, (i + 3) * 10]
    for _ in [range_1, range_2]:
        for i in range(_[0], _[1]):
            values += f"({i + 1}, 'Test{i + 1}'), "
    return values[:-2]


async def init_db() -> None:
    async with settings.db_pool as pool:
        for i in (1, 2, 3):
            await pool.execute(f"DROP TABLE IF EXISTS data_{i}")
            await pool.execute(f'''CREATE TABLE IF NOT EXISTS data_{i} (id serial PRIMARY KEY, name VARCHAR(255) NOT NULL)''')
            await pool.execute(
                    f'''
                    INSERT INTO data_{i}
                    (id, name)
                    VALUES 
                    {insert_data_values(i)}
                    '''
                )


async def get_data(db: AsyncSession, model: Base, sleep: int = 0) -> (Sequence | list):
    """
    Returns data from db tables. 
    model -- table data model
    sleep -- wait time befor start (default 0)
    """
    try:
        await asyncio.sleep(sleep)
        results = await db.execute(select(model))
        return results.scalars().all()
    except asyncio.CancelledError:
        return []
        

async def get_sorted_data(
        db: AsyncSession, 
        models: list[Base], 
        sort_column: str = "id",
        order: str = "asc", 
    ) -> list[dict]:
    """
    Return data from list of tables, sorted by.
    models -- list of table data models
    sort_column -- name of column sorted by
    order -- sort order, "asc" or "desc" (default "asc")
    """
    result = []
    try:
        for model in models:
            task = asyncio.create_task(get_data(db, model=model))
            data = await asyncio.wait_for(task, timeout=2)
            result += [model.__dict__ for model in data]
        data = sorted(result, key=lambda k: k[sort_column])
        
        if order == "desc":
            data.reverse()
        return data
    
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="TimeoutError")
    except Exception:
        raise
