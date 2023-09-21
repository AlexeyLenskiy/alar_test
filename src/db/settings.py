from typing import Any, Generator
import asyncpg
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Asyncpg
db_pool = asyncpg.create_pool(
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
    database=os.getenv("DBNAME"),
    host=os.getenv("DBHOST"),
    port=os.getenv("DBPORT"),
    command_timeout=60,
)

# SQLAlchemy
SQLALCHEMY_URL = (
    f'postgresql+asyncpg://{os.getenv("DBUSER")}:{os.getenv("DBPASSWORD")}'
    f'@{os.getenv("DBHOST")}:{os.getenv("DBPORT")}'
    f'/{os.getenv("DBNAME")}'
)
engine = create_async_engine(SQLALCHEMY_URL)
SessionLocal = async_sessionmaker(engine)
Base = declarative_base()

async def get_db() -> Generator[Any | None, Any, Any]:
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()