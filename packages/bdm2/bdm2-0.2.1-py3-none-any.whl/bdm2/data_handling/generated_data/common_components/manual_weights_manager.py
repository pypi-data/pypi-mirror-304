import copy
import os
from typing import Optional

import numpy as np
import pandas as pd

from bdm2.constants.global_setup.data import house_match_columns, device_match_columns
from bdm2.constants.global_setup.data_columns import breed_type_column, gender_column
from bdm2.constants.global_setup.server_paths import manual_weights_dir
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage



# from main_config import GlobalConfig

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.utils import load_weights_from_csv


def check_if_all_kg(weights: pd.Series) -> bool:
    default_standard = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Thailand\CP_ROSS_std_Weight.csv"
    assert os.path.exists(default_standard), f"default standard weight does not exist.\nCheck: {default_standard}"

    standard_weights_in_kg = load_weights_from_csv(default_standard)['Weights']
    return all((weights / standard_weights_in_kg).dropna() < 100)


def convert_to_kg(weights: pd.Series,
                  standard_weights_in_kg: Optional[pd.Series] = None  # TODO: DEPRECATE. MORE SIMPLE APPROACH APPLIED
                  ) -> pd.Series:
    """
    Check if any of weights are in g and convert them to kg

    :param weights: pd.Series with age as index
    :param standard_weights_in_kg: data with standard weights in kg TODO: DEPRECATE. MORE SIMPLE APPROACH APPLIED
    :return: converted weights with the same indexes
    """

    if not weights.empty:

        rows_in_grams = weights > 10  #(weights / standard_weights_in_kg.loc[weights.index]) > 100
        weights_in_kg = weights.copy()
        weights_in_kg.loc[rows_in_grams] /= 1000
        return weights_in_kg


def convert_to_g(weights: pd.Series,
                  standard_weights_in_kg: Optional[pd.Series] = None  # TODO: DEPRECATE. MORE SIMPLE APPROACH APPLIED
                 ) -> pd.Series:
    """
    Check if any of weights are in kg and convert them to g
    :param weights: pd.Series with age as index
    :return: converted weights with the same indexes
    """
    # if standard_weights_in_kg is None:
    #     default_standard = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Thailand\CP_ROSS_std_Weight.csv"  # in kg
    #     assert os.path.exists(default_standard), f"default standard weight does not exist.\nCheck: {default_standard}"
    #     standard_weights_in_kg = BirdooUtils.load_weights_from_csv(default_standard)['Weights']

    rows_in_kg = weights < 10
    # rows_in_kg = (weights / standard_weights_in_kg.loc[weights.index]) < 100
    weights_in_g = weights.copy()
    weights_in_g[rows_in_kg] *= 1000
    return weights_in_g


def get_adjusted_weights_folder(client: str, manual_postfix: str) -> str:
    """
    Return full path to folder with adjusted (likely) weights
    :param client: client name (farm)
    :param manual_postfix: format "_manual"
    :return: full path to folder with adjusted (likely) weights
    """
    return os.path.join(manual_weights_dir, f"{client}\\Adjusted{manual_postfix}")


def get_manual_weights_filename(client: str, manual_postfix: str) -> str:
    """
    Return full dir of manual weights file with manual_postfix weights
    :param client: client name (farm)
    :param manual_postfix: format "_manual"
    :return: full path to folder with adjusted (likely) weights
    """
    return os.path.join(manual_weights_dir, f"{client}\\Manual_measure_{client}{manual_postfix}.xlsx")


def get_all_adjusted_weights(client: str,
                             manual_postfix: str,
                             filters: Filter = None,
                             units='kg', weight_postfix_column_name="weights_postfix") -> pd.DataFrame:
    assert units in ['kg', 'g']

    adjusted_weights_folder = get_adjusted_weights_folder(client, manual_postfix)
    if not os.path.exists(adjusted_weights_folder):
        print(f"{adjusted_weights_folder} is not exist")
        return pd.DataFrame()

    files = [x for x in os.listdir(adjusted_weights_folder) if
             x.endswith(".csv") and x.startswith("adjusted_std_weights")]

    output_df = pd.DataFrame()
    try:
        for file_item in files:
            # print(f)
            str_parts = file_item.split(".")[-2].split("_")

            farm = str_parts[-3]
            cycle = str_parts[-2]
            house = str_parts[-1]
            device = pd.Series([farm, cycle, house], index=['farm', 'cycle', 'house'])
            if not filters.check_device(device):
                continue

            adj_weights = load_weights_from_csv(os.path.join(adjusted_weights_folder, file_item))
            if (adj_weights is None) or adj_weights.empty:
                continue

            adj_weights = adj_weights.reset_index()
            adj_weights.columns = ["daynum", "weight"]

            adj_weights["farm"] = farm
            adj_weights["cycle"] = cycle
            adj_weights["house"] = house
            output_df = pd.concat([output_df, adj_weights], ignore_index=True)

        if not output_df.empty:
            if units == 'kg':
                output_df['weight'] = convert_to_kg(output_df.set_index('daynum')['weight']).values
            elif units == 'g':
                output_df['weight'] = convert_to_g(output_df.set_index('daynum')['weight']).values

            devices = PostgresDevicesStorage().get_devices(filters=filters).groupby(house_match_columns, as_index=False).first()
            #BirdooUtils.load_devices_from_csv(GlobalConfig.device_csv) \
                # .groupby(house_match_columns, as_index=False).first()

            device_valuable_columns = house_match_columns + [breed_type_column,
                                                             gender_column]

            output_df = pd.merge(output_df,
                                 devices[device_valuable_columns],
                                 on=house_match_columns)
            output_df = output_df.set_index(device_valuable_columns).reset_index()

            if filters is not None:
                output_df = filters.filter_devices(output_df)

        assert output_df[house_match_columns + ['daynum']].duplicated().sum() == 0

    except AssertionError as e:
        print("output_df has duplicates")
        output_df = output_df[output_df[not device_match_columns + ['daynum']].duplicated()]
    except Exception as e:
        print(e)

    output_df[weight_postfix_column_name] = manual_postfix
    return output_df


def get_all_manual_weights(client: str, manual_postfix: str, filters: Filter = None,
                           units='kg', weight_postfix_column_name="weights_postfix") -> pd.DataFrame:
    assert units in ['kg', 'g']
    output_df = pd.DataFrame(columns=["farm","cycle","house","age","weight",weight_postfix_column_name], dtype=float)

    manual_weights_filename = get_manual_weights_filename(client, manual_postfix)
    if not os.path.exists(manual_weights_filename):
        print(f"not found {manual_weights_filename}")
        return output_df

    if filters is None:
        local_filters = Filter()
    else:
        local_filters = copy.copy(filters)

    if len(local_filters.cycles) == 0:
        local_filters.cycles = pd.ExcelFile(manual_weights_filename, engine='openpyxl').sheet_names
        local_filters.cycles.sort()

    for cycle_item in local_filters.cycles:
        print("Reading {} {}".format(manual_weights_filename, cycle_item))
        try:
            weights = pd.read_excel(manual_weights_filename, sheet_name=cycle_item, engine='openpyxl', index_col=1)
            weights = weights[[c for c in weights.columns if "Unnamed" not in c]]
            weights = weights.dropna(axis=0, how="all")

        except Exception:
            print("No {} sheet".format(cycle_item))
            continue

        for house_item in weights.columns:
            if "Unnamed" in house_item:
                continue

            if (house_item not in local_filters.houses) and (len(local_filters.houses) != 0):
                continue

            for age_item in weights[house_item].index:
                if pd.isna(weights[house_item][age_item]):
                    continue
                if not local_filters.check_age(age_item):
                    continue

                s = pd.Series(dtype=object)
                s["farm"] = client
                s["cycle"] = cycle_item
                s["house"] = house_item
                s["age"] = age_item
                s["weight"] = weights[house_item][age_item]
                output_df.loc[len(output_df), s.index] = s.copy()
                # output_df = output_df.append(s, ignore_index=True)

    if not output_df.empty:
        if units == 'kg':
            output_df['weight'] = convert_to_kg(output_df.set_index('age')['weight']).values
        elif units == 'g':
            output_df['weight'] = convert_to_g(output_df.set_index('age')['weight']).values

    devices = PostgresDevicesStorage().get_devices(filters=local_filters).groupby(house_match_columns, as_index=False).first()
    device_valuable_columns = house_match_columns + [breed_type_column,
                                                     gender_column]
    output_df = pd.merge(output_df,
                         devices[device_valuable_columns],
                         on=["farm", "cycle", "house"])
    output_df = output_df.set_index(device_valuable_columns).reset_index()
    if local_filters is not None:
        output_df = local_filters.filter_devices(output_df)

    output_df[weight_postfix_column_name] = manual_postfix
    return output_df


def save_manual_data(df: pd.DataFrame, save_fname: str, round: int = -1, units='g'):
    assert units in ['kg', 'g']

    writer = pd.ExcelWriter(save_fname, engine='xlsxwriter')
    # df_copy = df.copy()
    n_cycles_added = 0
    for c, c_group in df.groupby("cycle"):
        c_group_c = c_group.copy()
        if units == 'kg':
            c_group_c['weight'] = convert_to_kg(c_group_c.set_index('age')['weight']).values
        elif units == 'g':
            c_group_c['weight'] = convert_to_g(c_group_c.set_index('age')['weight']).values
        if round >= 0:
            c_group_c['weight'] = c_group_c['weight'].round(round).values
        if not os.path.exists(os.path.dirname(save_fname)):
            os.makedirs(os.path.dirname(save_fname))
        try:
            c_group_pivot = c_group.pivot(index="age", columns="house", values="weight")

        except Exception as e:
            print(e)
            print(f'Could not create pivot table for {c}. Check device table. '
                  f'It could be, that there are house duplicates!')
            continue
        try:
            cols = np.array(sorted(c_group_pivot.columns, key=lambda x: (int)(x.split(' ')[-1])))
        except Exception as e:
            cols = c_group_pivot.columns

        c_group_pivot = c_group_pivot[cols].reset_index(drop=False)
        c_group_pivot = c_group_pivot
        c_group_pivot.to_excel(writer, c)
        n_cycles_added += 1

    writer.close()
    if n_cycles_added == 0:
        os.remove(save_fname)
    pass


def generate_fname_for_adjusted_weights(farm: str, cycle: str, house: str):
    return f"adjusted_std_weights_{farm}_{cycle}_{house}.csv"


def save_adjusted_weights(weights: pd.Series, save_fname: str, round: int = -1, units='kg'):
    assert units in ['kg', 'g']

    if not os.path.exists(os.path.dirname(save_fname)) and os.path.dirname(save_fname) != '':
        os.makedirs(os.path.dirname(save_fname))
    if units == 'kg':
        weights_copy = convert_to_kg(weights)
    elif units == 'g':
        weights_copy = convert_to_g(weights)
    else:
        weights_copy = weights.copy()

    if round >= 0:
        weights_copy = weights_copy.round(round)
    weights_copy.to_csv(save_fname, sep=";", header=False)
    pass


def match_adjusted_weights(client: str,
                           df: pd.DataFrame,
                           manual_postfix: str,
                           filters: Filter,
                           new_col_name: str = "adjusted_weight",
                           match_age_col: str = 'age',
                           units='kg',
                           from_db: bool = False
                           ) -> pd.DataFrame:
    assert units in ['kg', 'g']
    match_columns = house_match_columns + [match_age_col]
    if any([(x not in df.columns.values) for x in match_columns]):
        print("Not all required columns are in df")
        print("Required columns: {}".format(match_columns))
        return df

    if new_col_name in df.columns:
        df = df.drop(new_col_name, axis='columns')

    if from_db:
        print(f'Weights src for {client}{manual_postfix}: db')
        try:
            raise Exception('NOT AVALIABLE')
            # adj_manual_weight = get_all_adjusted_weights_from_db(manual_postfix, filters, units=units)
            # adj_manual_weight = adj_manual_weight.rename(columns={'age': match_age_col, "weight": new_col_name})
        except Exception as e:
            print(e)
            print(f'Weights src for {client}{manual_postfix}: excel')
            adj_manual_weight = get_all_adjusted_weights(client, manual_postfix, filters, units=units)
            adj_manual_weight = adj_manual_weight.rename(columns={'daynum': match_age_col, "weight": new_col_name})
    else:
        print(f'Weights src for {client}{manual_postfix}: excel')
        adj_manual_weight = get_all_adjusted_weights(client, manual_postfix, filters, units=units)
        adj_manual_weight = adj_manual_weight.rename(columns={'daynum': match_age_col, "weight": new_col_name})

    if adj_manual_weight.empty:
        print(f"NO likely weights were found for {client}, {filters.generate_label()}")
        return df
    # adj_manual_weight = adj_manual_weight.rename(columns={'daynum': match_age_col, "weight": new_col_name})

    adj_manual_weight = adj_manual_weight[match_columns + [new_col_name]]
    adj_manual_weight = adj_manual_weight.drop_duplicates(subset=match_columns)

    res_df = pd.merge(df, adj_manual_weight, how='left', on=match_columns)
    return res_df
