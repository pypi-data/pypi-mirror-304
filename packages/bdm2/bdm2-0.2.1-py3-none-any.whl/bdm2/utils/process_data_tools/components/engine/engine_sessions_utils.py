import datetime
import os
from pathlib import Path
from typing import Union

import pandas as pd

from bdm2.constants.global_setup.data import sess_folder_date_format
from bdm2.logger import build_logger


def is_evening_session(datetime_obj, evening_time: str = "") -> bool:
    if evening_time != "":
        evening_hours, evening_minutes, evening_second = evening_time.split("-")
        if int(evening_hours) <= int(datetime_obj.hour):
            return True
    return False


def get_datetime_from_sess(sess_name) -> datetime.datetime:
    """
    Return timestamp of sess name.

    :param sess_name: name of session folder with format output_%y_%m_%d_%H_%M_%S
    :return: datetime.datetime of session
    """
    sess_basename = os.path.basename(sess_name)
    _, y, m, d, H, M, S = sess_basename.split("_")[
                          : len(sess_folder_date_format.split("_"))
                          ]
    return datetime.datetime(int(y), int(m), int(d), int(H), int(M), int(S))


def get_age_from_sess_folder(
        sess_name, cycle_start_day: str = "", evening_time: str = ""
):
    """
    Return Cycle day using

    :param sess_name: name of session folder with format output_%y_%m_%d_%H_%M_%S
    :param cycle_start_day: cycle start day with format %y.%m.%d
    :param evening_time: evening time with format %H-%M-%S
    :return: daynum
    """

    logger = build_logger(Path(__file__), save_log=False)
    sess_basename = os.path.basename(sess_name)
    try:
        sess_datetime = get_datetime_from_sess(sess_basename)
    except Exception as e:
        logger.info(e)
        return -1

    age_pos = sess_basename.find("_age_")
    if age_pos >= 0:
        age = int(
            sess_basename[age_pos + len("_age_"):]
            .split("_")[0]
            .split(".")[0]
            .split(" ")[0]
            .split("-")[0]
        )
        extraday = is_evening_session(sess_datetime, evening_time)
        age += (int)(extraday)
    else:
        age = get_age_from_datetime(sess_datetime, cycle_start_day, evening_time)
    return age


def get_age_from_datetime(datetime_obj, cycle_start_day, evening_time: str = "") -> int:
    logger = build_logger(Path(__file__), save_log=False)
    if isinstance(cycle_start_day, str):
        try:
            start_date = cycle_start_day_to_datetime(cycle_start_day)

        except Exception as e:
            logger.info(f"get_age_from_datetime: {e}")
            logger.info(f"Could not parse cycle_start_day {cycle_start_day}")
            return -1

    elif isinstance(cycle_start_day, datetime.date):
        try:
            start_date = datetime.datetime(
                year=cycle_start_day.year,
                month=cycle_start_day.month,
                day=cycle_start_day.day,
            )

        except Exception as e:
            logger.info(f"get_age_from_datetime: {e}")
            logger.info(f"Could not parse cycle_start_day {cycle_start_day}")
            return -1
    elif not isinstance(cycle_start_day, datetime.datetime):
        logger.info(f"get_age_from_datetime error")
        logger.info(f"Could not parse cycle_start_day {cycle_start_day}")
        return -1
    try:
        age = (datetime_obj - start_date).days
        extraday = is_evening_session(datetime_obj, evening_time)
        return age + int(extraday)
    except Exception as e:
        logger.info(e)
    return -1


def get_datetime_for_age(
        device: pd.Series, age: int, cycle_start_day_column: str = "cycle_start_day"
) -> datetime.datetime:
    start_cycle_datetime = cycle_start_day_to_datetime(device[cycle_start_day_column])
    start_cycle_datetime = start_cycle_datetime + datetime.timedelta(days=age)
    return start_cycle_datetime


def get_datetime_for_age_simple(
        cycle_start_date: Union[datetime.datetime, str], age: int
) -> datetime.datetime:
    if isinstance(cycle_start_date, str):
        cycle_start_date = cycle_start_day_to_datetime(cycle_start_date)
    start_cycle_datetime = cycle_start_date + datetime.timedelta(days=age)
    return start_cycle_datetime


def cycle_start_day_to_datetime(
        cycle_start_day_str: Union[str, datetime.datetime, datetime.date, None]
) -> Union[datetime.datetime, None]:
    if cycle_start_day_str is None:
        return None
    if isinstance(cycle_start_day_str, datetime.datetime):
        return cycle_start_day_str
    if isinstance(cycle_start_day_str, datetime.date):
        return datetime.datetime.combine(cycle_start_day_str, datetime.time())
    if "." in cycle_start_day_str:
        try:
            sd, sm, sy = cycle_start_day_str.split(".")
            dt = datetime.datetime(int(sy), int(sm), int(sd))
            return dt
        except:
            sy, sm, sd = cycle_start_day_str.split(".")
            dt = datetime.datetime(int(sy), int(sm), int(sd))
            return dt

    elif "-" in cycle_start_day_str:
        try:
            sd, sm, sy = cycle_start_day_str.split("-")
            dt = datetime.datetime(int(sy), int(sm), int(sd))
            return dt
        except:
            sy, sm, sd = cycle_start_day_str.split("-")
            dt = datetime.datetime(int(sy), int(sm), int(sd))
            return dt
    return None
