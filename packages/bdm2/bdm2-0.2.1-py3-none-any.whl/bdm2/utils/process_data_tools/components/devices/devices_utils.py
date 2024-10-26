import os
from pathlib import Path
from typing import List, Optional

import pandas as pd

from bdm2.constants.global_setup.data import device_match_columns
from bdm2.logger import build_logger


# =======================================================
# Loaders
# =======================================================


def load_devices_from_csv(filename) -> Optional[pd.DataFrame]:
    """
    Loading all devices table
    :param filename: full path to Devices.CSV file
    :return: pd.DataFrame
    """
    logger = build_logger(Path(__file__), save_log=False)
    if os.path.exists(filename):
        # TODO: approve changes
        df = pd.read_csv(
            filename, sep=";", index_col=None, header=0, encoding="ISO-8859-1"
        )  # encoding= 'unicode_escape')#warn_bad_lines=True, error_bad_lines=False)
    else:
        return None

    if df[device_match_columns].duplicated().sum() > 0:
        logger.info("PROBLEMS WITH DEVICE FILE. ID DUPLICATES FOUND")
        logger.info(df[device_match_columns][df[device_match_columns].duplicated()])
        df = df.drop_duplicates(subset=device_match_columns, keep="first")
        # return None
    for i, r in df.iterrows():
        try:
            df.loc[i, "cycle_start_day"] = r["cycle_start_day"].replace(".", "-")
        except:
            pass

    df = df[[col for col in df.columns if not col.startswith("Unnamed")]]
    df.dropna(how="all", inplace=True)

    return df


def loadBirdooDevicesMatchingFromXLSX(filename):
    """
    Loading all devices table
    :param filename: full path to Devices.xlsx file
    :return: pd.DataFrame
    """
    logger = build_logger(Path(__file__), save_log=False)
    if os.path.exists(filename):
        df = pd.read_excel(filename, header=0, engine="openpyxl")
        logger.info(f"devices table was loaded from {filename}")
    else:
        return None
    return df


# =======================================================
# Device tools
# =======================================================


def generate_id_from_device(device: pd.Series, cols: List[str],
                            logger=build_logger(Path(__file__), save_log=False)) -> str:
    """
    Generate ID from specified columns
    :param device: pd.Series
    :param cols: list of columns
    :return: str
    @param logger:
    """
    try:
        return ("_".join(device[cols])).replace(" ", "")
    except:
        logger.info("wrong columns")
        return ""


# def add_device_to_csv(farm: str,
#                       cycle: str,
#                       house: str,
#                       device: str,
#                       flock: str = None,
#                       gender: str = None, breed_type: str = None,
#                       cycle_start_day: datetime.date = None,
#                       client: Optional[str] = None,
#                       client_id: Optional[str] = None,
#                       farm_id: Optional[str] = None,
#                       house_id: Optional[str] = None,
#                       cycle_id: Optional[str] = None,
#                       devices_csv=GlobalConfig.device_csv) -> bool:
#     """
#     farm_id = self.cur_path_dict['farm_id'],
#                     house_id = self.cur_path_dict['house_id'],
#                     cycle_id = self.cur_path_dict['cycle_id']
#     """
#     devices = load_devices_from_csv(devices_csv)
#     device_s = pd.Series()
#     device_s['farm'] = farm
#     device_s['cycle'] = cycle
#     if flock is None:
#         device_s['flock'] = GlobalConfig.default_flock_name
#     else:
#         device_s['flock'] = flock
#
#     device_s['house'] = house
#     device_s['device'] = device
#     device_s['gender'] = gender
#     device_s['breed_type'] = breed_type
#     device_s['cycle_start_day'] = cycle_start_day
#     device_s['client'] = client
#
#     # try:
#     device_s['id'] = generate_id_from_device(device_s, ['device', 'house', 'flock', 'cycle'])
#     # except:
#     #     device_s['id'] = None
#     device_s['client_id'] = client_id
#     device_s['farm_id'] = farm_id
#     device_s['house_id'] = house_id
#     device_s['cycle_id'] = cycle_id
#
#     device_s['path'] = "\\".join(device_s[device_match_columns])
#     device_s['server_dir'] = GlobalConfig.current_active_server_data_dir
#     # TODO: if already exist, update (if new features appeared) not skip!!
#     if len(devices[devices['path'] == device_s['path']]):
#         logger.info(f"device is already in device.csv")
#         return False
#     if (device_s[device_match_columns] == devices[GlobalConfig.house_match_columns]).all(axis=1).sum() > 0:
#         logger.info(f'device already in {devices_csv}')
#         return False
#     devices.loc[len(devices), device_s.index] = device_s.copy()
#     devices.to_csv(devices_csv, sep=';', index=False)
#     return True


# =======================================================
# Matching tools
# =======================================================
def match_device_table(
        df: pd.DataFrame, match_by_columns: List[str], columns_to_match: List[str]
) -> pd.DataFrame:
    """
    Match to df any necessary columns from devices.
    if columns_to_match are also in df, update columns in df with columns from GlobalConfig.device_csv

    :param df: must have 'match_by_columns'
    :param match_by_columns: should be as in df so in GlobalConfig.device_csv
    :param columns_to_match: should be in GlobalConfig.device_csv. if [], add all columns from GlobalConfig.device_csv
    :return: merged df
    """

    # devices = load_devices_from_csv(GlobalConfig.device_csv)
    devices = None
    # devices = devices.groupby(match_by_columns).first()
    tmp_df = df.set_index(match_by_columns)
    if len(columns_to_match) == 0:
        tmp_df = pd.merge(
            tmp_df,
            devices,
            right_index=True,
            left_index=True,
            how="left",
            suffixes=("_local_duplicates", ""),
        )
    else:
        tmp_df = pd.merge(
            tmp_df,
            devices[columns_to_match],
            right_index=True,
            left_index=True,
            how="left",
            suffixes=("_local_duplicates", ""),
        )
    tmp_df = tmp_df[
        [col for col in tmp_df.columns if (not col.endswith("_local_duplicates"))]
    ].reset_index()
    return tmp_df
