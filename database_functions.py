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


def get_data_from_database(pool, column) -> list:
    try:
        ret_list = []
        
        conn = event_loop.run_until_complete(pool.acquire())
        query = f"SELECT * FROM vip_car_table"
        rows = event_loop.run_until_complete(conn.fetch(query))
        if column.lower() == 'all':
            for index in range(4):
               vehicle = rows[index]['vehicle']
               arrival = rows[index]['arrival']
               vip_name = rows[index]['vip_name']
               ret_list.append((vehicle, arrival, vip_name))
            return ret_list
        else:

            for index in range(4):
                data = rows[index][column]
                ret_list.append(data)
            return ret_list
    finally:

        event_loop.run_until_complete(pool.release(conn))
        event_loop.run_until_complete(pool.close())
"""
def get_relative_data(pool, license_plate, relative_column):
    try:
        conn = event_loop.run_until_complete(pool.acquire())
        query = f"SELECT * FROM vip_car_table WHERE vehicle = '{license_plate}'"
        rows = event_loop.run_until_complete(conn.fetch(query))
        return rows[0][relative_column]
    except Exception as err:
        print(err)
    finally:

        event_loop.run_until_complete(pool.release(conn))
        event_loop.run_until_complete(pool.close())
"""
list_vip_names = get_data_from_database(start_database_connection(), 'vip_name')
list_license_plates = get_data_from_database(start_database_connection(), 'vehicle')
list_arrival_time = get_data_from_database(start_database_connection(), 'arrival')

list_all_values = get_data_from_database(start_database_connection(), 'all')


#print(list_all_values)

