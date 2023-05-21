import asyncpg
from constants import database_access_url

queries_dict = {
     'CHECK_DB_STATUS': 'SELECT 1',
}

class DatabaseClient:

    def __init__(self):
            pass 
    
    async def start_database_connection(self) -> asyncpg.Pool:
        """ Starts Database Connection Pool """
        try:
            pool = await asyncpg.create_pool(database_access_url, max_size=100)
            print(f"[PSQL] | Database Connected: {bool(pool)}")

        except Exception as err:
            print(f"[PSQL] | Database Connection Error: {err}")
    
    async def get_data_from_database(column: str) -> list:
         ...