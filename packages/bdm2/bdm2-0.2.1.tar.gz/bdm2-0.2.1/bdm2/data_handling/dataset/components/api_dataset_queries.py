from typing import List

import pandas as pd

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.api_wrapper import APIWrapper
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.endpoints import \
    get_actual_weight_source_info
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


def api_get_cycle_house_codes(client_name: str,
                              breed_name: str,
                              gender: str) -> list:
    api = APIWrapper()
    filters = Filter(clients=[client_name],
                     breed_types=[breed_name],
                     genders=[gender],
                     )

    res = api.get_devices(filters)
    res_list = res['cycle_house_code'].unique().tolist()
    return res_list


def api_get_usable_for_train_flags(df: pd.DataFrame) -> pd.DataFrame:  # cycle_house_code_list,

    api = APIWrapper()
    filters = Filter(clients=[],
                     breed_types=[],
                     genders=[],
                     )

    res = api.get_devices(filters)
    df = df.merge(res[["cycle_house_code",
                       "device",
                       "usable_for_train"]],
                  on=["cycle_house_code", "device"], how='left')

    return df


def api_get_additional_info(piv):
    api = APIWrapper()
    filters = Filter(clients=[],
                     breed_types=[],
                     genders=[],
                     )
    res = api.get_devices(filters)
    COLS = [
        "cycle_house_code",
        "client",
        "breed_type",
        "gender",
        "farm",
        "cycle",
        "house",
        "device_name",
        "device"
    ]

    piv = piv.merge(res[COLS], on=["device",
                                   "cycle_house_code"], how="left")
    piv.rename(columns={"device": "device_code",
                        "device_name": "device"}, inplace=True)
    return piv

