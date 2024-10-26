import time
from typing import List

import pandas as pd
import psycopg2
from loguru import logger

from bdm2.utils.schemas.connection import POSTGRE_SQL_CREDS
from bdm2.utils.schemas.connection import get_clickhouse_client


def connect(retries=10, delay=1):
    """
    Establishes a connection to the PostgreSQL database with a retry mechanism.

    :param retries: Number of retry attempts if the connection fails.
    :param delay: Delay between retries in seconds.

    :return: cursor, connection
    """
    attempt = 0
    while attempt < retries:
        try:
            connection = psycopg2.connect(
                user=POSTGRE_SQL_CREDS.user,
                password=POSTGRE_SQL_CREDS.password,
                host=POSTGRE_SQL_CREDS.host,
                port=POSTGRE_SQL_CREDS.port,
                database=POSTGRE_SQL_CREDS.db_name,
            )
            cursor = connection.cursor()
            return cursor, connection

        except psycopg2.OperationalError as e:
            attempt += 1
            logger.error(f"Connection attempt {attempt} failed: {e}")

            if attempt == retries:
                logger.error("Max retries reached. Unable to connect to the database.")
                raise e

            logger.info(f"Retrying connection in {delay} seconds...")
            time.sleep(delay)


# генерация строки для psyopg-sql команд
def generate_psyopg_row_from_list(some_list):
    if len(some_list) == 0:
        return ""
    line = ""
    for i in some_list:
        line += "', '" + str(i)

    line = line[3:]
    line += "'"
    return line


def get_cycle_house_codes(client_name: str, breed_name: str, gender: str) -> list:
    """
    :param client_name - name of client
    :param breed_name - name of breed
    :param gender - name of gender

    :return:
    list with all available cycle_house_codes for this
    combination in moment of request

    """
    cursor, connection = connect()

    select_query = f"""
    SELECT 
        distinct cycle_house_code 
        from public.devices_view dv
    where dv.client_name = '{client_name}' and dv.breed_type  = '{breed_name}' and dv.gender = '{gender}'
    """

    COLS = ["cycle_house_code"]

    cursor.execute(select_query)
    publisher_records = cursor.fetchall()
    df = pd.DataFrame(publisher_records, columns=COLS)
    res = [i.pop() for i in df.values.tolist()]

    cursor.close()
    return res


def get_additional_info(cycle_house_codes_list: List[str]) -> pd.DataFrame:
    """
    :param cycle_house_codes_list - cycle house codes, gotten from click-house

    :return:
    df[COLS] for merge it with main work DataFrame after

    """
    cursor, connection = connect()
    cycle_house_codes_row = generate_psyopg_row_from_list(cycle_house_codes_list)

    select_query = f"""
    SELECT 
        cycle_house_code,
        client_name as client,
        breed_type,
        gender,
        farm_name as farm,
        cycle_house_name as cycle,
        house_name as house,
        device_name,
        device_code as device
        from public.devices_view dv
    where dv.cycle_house_code in ({cycle_house_codes_row})
    """

    COLS = [
        "cycle_house_code",
        "client",
        "breed_type",
        "gender",
        "farm",
        "cycle",
        "house",
        "device_name",
        "device",
    ]

    cursor.execute(select_query)
    publisher_records = cursor.fetchall()
    df = pd.DataFrame(publisher_records, columns=COLS)

    cursor.close()
    return df


def get_raw_features(
        engine_name: str,
        cycle_house_list: List[str],
        features_list: List[str],
        batch_size: int = 30  # Define the size of each batch to process
) -> pd.DataFrame:
    """
    Retrieves raw features from ClickHouse in batches for the given engine name and cycle house list.

    :param engine_name: The name of the engine.
    :param cycle_house_list: List of cycle house codes.
    :param features_list: List of feature names.
    :param batch_size: The number of records to process in each batch.

    :return: DataFrame containing the result.
    """
    attempt = 0
    delay = 1
    retries = 5
    final_df = pd.DataFrame()

    while attempt < retries:
        try:
            clickhouse_client = get_clickhouse_client()
            features_row = generate_psyopg_row_from_list(features_list)

            total_cycle_houses = len(cycle_house_list)
            logger.debug(f"Total cycle_houses: {total_cycle_houses}")
            num_batches = (total_cycle_houses // batch_size) + (1 if total_cycle_houses % batch_size != 0 else 0)

            for batch_num in range(num_batches):
                start_index = batch_num * batch_size
                end_index = min(start_index + batch_size, total_cycle_houses)

                batch_cycle_house_list = cycle_house_list[start_index:end_index]
                logger.debug(f"{batch_cycle_house_list}")
                batch_cycle_house_row = generate_psyopg_row_from_list(batch_cycle_house_list)

                script = f"""
                    SELECT 
                        cycle_house_code,
                        device,
                        age,
                        session,
                        feature_name, 
                        feature_stat_name, 
                        value
                    FROM actual_results ar 
                    WHERE engine_name = '{engine_name}' 
                        AND cycle_house_code IN ({batch_cycle_house_row}) 
                        AND feature_name IN ({features_row})
                """

                result = clickhouse_client.query(script)
                batch_df = pd.DataFrame(result.result_rows, columns=result.column_names)

                # Append the batch DataFrame to the final DataFrame
                final_df = pd.concat([final_df, batch_df], ignore_index=True)

            # Exit loop if the operation succeeds
            return final_df

        except Exception as e:
            attempt += 1
            logger.error(f"Connection attempt {attempt} failed: {e}")

            if attempt == retries:
                logger.error("Max retries reached. Unable to connect to the database.")
                raise e

            # Wait before retrying
            logger.info(f"Retrying connection in {delay} seconds...")
            time.sleep(delay)

    # If all retries fail, return an empty DataFrame
    return pd.DataFrame()


def get_actual_likely_posfix(client_name: str, breed_name: str, gender: str):
    cursor, connection = connect()
    script = f"""
    SELECT 
    target_weights_postfix

    FROM actual_clients_info_storage aci 
    where aci.client = '{client_name}' and aci.breed_type = '{breed_name}' and aci.gender = '{gender}'
    """

    cursor.execute(script)
    publisher_records = cursor.fetchone()

    cursor.close()
    return publisher_records[0]


# TODO: получать инфу о юзабельности и неюзабельности, проставлять usable_for_train флаг


def get_usable_for_train_flags(cycle_house_code_list, devices_names_list):
    cursor, connection = connect()
    cycle_house_row = generate_psyopg_row_from_list(cycle_house_code_list)
    devices_names_row = generate_psyopg_row_from_list(devices_names_list)

    get_device_info_sql_query = f"""
    select usable_for_train,
    cycle_house_code,
    device_code as device
    from devices_view 
    where cycle_house_code in ({cycle_house_row})
    and device_code in ({devices_names_row}) """

    cursor.execute(get_device_info_sql_query)
    publisher_records = cursor.fetchall()
    cols = ["usable_for_train", "cycle_house_code", "device"]

    df_usable = pd.DataFrame(publisher_records, columns=cols)

    cursor.close()
    if connection:
        cursor.close()
        connection.close()

    return df_usable
