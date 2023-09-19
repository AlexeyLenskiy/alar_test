import asyncpg
import os



db_pool = asyncpg.create_pool(
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
    database=os.getenv("DBNAME"),
    host=os.getenv("DBHOST"),
    port=os.getenv("DBPORT"),
    command_timeout=10,
)

def insert_data_values(i: int):
    values = ""
    range_1 = [(i - 1) * 10, i * 10]
    range_2 = [(i + 2) * 10, (i + 3) * 10]
    for _ in [range_1, range_2]:
        for i in range(_[0], _[1]):
            values += f"({i + 1}, 'Test{i + 1}'), "
    return values[:-2]


async def init_db() -> None:
    async with db_pool as pool:
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
        
    pool.close()
