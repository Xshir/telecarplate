import asyncpg
import asyncio
from constants import DATABASE_ACCESS_URL

event_loop = asyncio.get_event_loop()

def start_database_connection() -> asyncpg.Pool:
    """ Starts Database Connection Pool """
    try:
        pool = event_loop.run_until_complete(asyncpg.create_pool(DATABASE_ACCESS_URL, max_size=100))
        print(f"[PSQL] | Database Connected: {bool(pool)}")
        return pool
    except Exception as err:
        print(f"[PSQL] | Database Connection Error: {err}")


def get_data_from_database(column) -> list:
    try:
        ret_list = []
        pool = start_database_connection()
        conn = event_loop.run_until_complete(pool.acquire())
        query = f"SELECT * FROM vip_car_table"
        rows = event_loop.run_until_complete(conn.fetch(query))
        for index in range(3):
            data = rows[index][column]
            ret_list.append(data)
        return ret_list
    finally:

        event_loop.run_until_complete(pool.release(conn))
        event_loop.run_until_complete(pool.close())

def get_relatives_of_license_plate(license_plate, relative_column):
    try:

        pool = start_database_connection()
        conn = event_loop.run_until_complete(pool.acquire())
        query = f"SELECT * FROM vip_car_table WHERE vehicle = '{license_plate}'"
        rows = event_loop.run_until_complete(conn.fetch(query))
        return rows[0][relative_column]
    finally:

        event_loop.run_until_complete(pool.release(conn))
        event_loop.run_until_complete(pool.close())

"""
list_ = get_data_from_database("vehicle")
print(list_)

"""
#print(str(get_relatives_of_license_plate('SBL4567F', 'arrival')))