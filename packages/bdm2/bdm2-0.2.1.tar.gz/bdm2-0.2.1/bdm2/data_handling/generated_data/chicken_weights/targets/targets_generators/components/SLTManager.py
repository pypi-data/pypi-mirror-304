import copy
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from bdm2.constants.global_setup.data import house_match_columns, default_flock_name
from bdm2.constants.global_setup.server_paths import slt_dir, device_csv
from bdm2.data_handling.generated_data import manual_weights_manager
from bdm2.data_handling.generated_data.standard.components import standards_manager
from typing import List, Optional

from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.devices.devices_utils import load_devices_from_csv
from bdm2.utils.process_data_tools.components.engine.engine_sessions_utils import get_datetime_for_age, \
    get_age_from_datetime


def get_slt_timetable_filename(client: str, filename_postfix: str = "") -> str:
    slt_info_dir = r"\\datasets\chikens\MHDR_Chicken\sources\SLUT"
    slt_filename = ""
    if client == "Thailand":
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}_corr.xlsx"
    if client == "Japan":
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}.xlsx"
    if client == "Cargill-NG":
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}.xlsx"
    if client == "BRF":
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}.xlsx"
    if client == "KXPHPSM":
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}.xlsx"
    else:
        slt_filename = slt_info_dir + f"\\{client}\\SLUT_timetable_{client}.xlsx"
    slt_filename = slt_filename.replace('.xlsx', f'{filename_postfix}.xlsx')
    return slt_filename


def get_piwfha_filename(client: str, filename_postfix: str = "") -> str:
    """
    generate PIWFHA filename for specified farm.

    .. warning::
        client is actually farm!!!!

    :param client: is actually farm!!!!
    :param filename_postfix: weights postfix
    :return: full path to file
    """
    slt_info_dir = slt_dir  # r"\\datasets\chikens\MHDR_Chicken\sources\SLUT"
    slt_filename = slt_info_dir + f"\\{client}\\{client}_PIWFA{filename_postfix}.csv"
    # slt_filename = slt_filename.replace('.csv', f'{filename_postfix}.csv')
    return slt_filename


def get_SLT_data(filters: Filter):
    devices = load_devices_from_csv(device_csv)
    devices = filters.filter_devices(devices)

    output_df = pd.DataFrame()
    for farm in devices['farm'].unique():

        tmp_piwfha = load_piwfha_table(farm, filters)
        if tmp_piwfha.empty:
            tmp_slt = load_slt_table(farm, filters)
        else:
            tmp_slt = pd.DataFrame()
        if not tmp_slt.empty and not tmp_piwfha.empty:
            match_cols = list(set(tmp_slt.columns).intersection(house_match_columns))
            piwfha_cols_to_add = list(
                set(tmp_piwfha.columns).difference(set(match_cols)).difference(set(tmp_slt.columns)))
            tmp = pd.merge(tmp_slt, tmp_piwfha[match_cols + piwfha_cols_to_add], on=match_cols, how='outer')
        elif tmp_piwfha.empty:
            print("PIWFHA is empty")
            tmp = tmp_slt
        elif tmp_slt.empty:
            print("SLT is empty")
            tmp = tmp_piwfha
        else:
            tmp = pd.DataFrame()

        output_df = pd.concat([output_df, tmp], ignore_index=True)
    return output_df


def load_piwfha_table(farm, filters: Optional[Filter], filename_postfix: str = "",
                      verbose: bool = True) -> pd.DataFrame:
    filename = get_piwfha_filename(farm, filename_postfix)
    if verbose:
        print("     Reading {}".format(filename))
    df_output = pd.DataFrame()
    if not os.path.exists(filename):
        return df_output
    df_output = pd.read_csv(filename, sep=';')
    if filters is not None:
        df_output = filters.filter_res_df_csv(df_output, age_col='slt_age')
    return df_output


def save_piwfha_table(df: pd.DataFrame, save_fname: str):
    df.to_csv(save_fname, sep=';', index=False)


def load_slt_table(farm, filters: Optional[Filter], filename_postfix: str = "", verbose: bool = True) -> pd.DataFrame:
    fname = get_slt_timetable_filename(farm, filename_postfix)

    output_df = pd.DataFrame()

    if not os.path.exists(fname):
        return output_df

    if filters is None:
        local_filters = Filter()
    else:
        local_filters = copy.copy(filters)

    if len(local_filters.cycles) == 0:
        local_filters.cycles = pd.ExcelFile(fname, engine='openpyxl').sheet_names
        local_filters.cycles.sort()
    for c in local_filters.cycles:
        if verbose:
            print("     Reading {} {}".format(fname, c))
        try:
            data = pd.read_excel(fname, sheet_name=c, engine='openpyxl', index_col=0)
            data = data[[c for c in data.columns if "Unnamed" not in c]]
        except Exception:
            print("No {} sheet".format(c))
            continue

        for h in data.columns:
            if "Unnamed" in h:
                continue

            house_name = h.split('.')[0]
            if (house_name not in local_filters.houses) and (len(local_filters.houses) != 0):
                continue

            s = data[h].dropna().copy()
            s["cycle"] = c
            s["house"] = house_name
            output_df = pd.concat([output_df, s.to_frame().T], ignore_index=True)
            # output_df = output_df.append(s, ignore_index=True)
    if output_df.empty:
        return output_df

    devices = load_devices_from_csv(device_csv)
    devices = devices.groupby(house_match_columns, as_index=False).first().drop('device', axis=1)
    output_df['farm'] = farm
    output_df = pd.merge(output_df, devices[house_match_columns], on=["farm", "cycle", "house"],
                         how='left')
    if 'flock' not in output_df.columns:
        output_df['flock'] = default_flock_name
    output_df['flock'] = output_df['flock'].fillna(default_flock_name)
    output_df = output_df.set_index(house_match_columns).reset_index()
    output_df = local_filters.filter_res_df_csv(output_df, age_col='age')
    return output_df


def save_slt_table(df: pd.DataFrame, save_fname: str):
    if not os.path.exists(os.path.dirname(save_fname)):
        os.makedirs(os.path.dirname(save_fname))
    writer = pd.ExcelWriter(save_fname, engine='xlsxwriter')
    try:
        drop_columns = list(set(house_match_columns).difference(['cycle', 'house']))
        df_copy = df.drop(drop_columns, axis=1)
        for c, c_group in df_copy.groupby('cycle'):
            c_group = c_group.drop(['cycle'], axis='columns').set_index("house").T
            cols = c_group.columns.unique()
            try:
                cols = np.array(sorted(cols, key=lambda x: (int)(x.split(' ')[-1])))
            except Exception as e:
                pass
            c_group = c_group[cols]
            c_group.to_excel(writer, c)
    except Exception as e:
        warnings.warn(f"save_slt_table: {e}")
    writer.close()


# def get_slt_timetable(session: Session,
#                       filters: Filter,
#                       weight_types_to_add: List[str]):
#
#     active_tables = [SLTTimetable, CycleHouses, Houses, Farms, Clients]
#     if len(weight_types_to_add):
#         active_tables += [ChickenWeights, WeightSources, WeightSourceTypes]
#
#     query = session.query(*active_tables).join(
#         CycleHouses, SLTTimetable.cycle_house_id == CycleHouses.id).join(
#         Houses, CycleHouses.house_id == Houses.id).join(
#         Farms, Houses.farm_id == Farms.id).join(
#         Clients, Farms.client_id == Clients.id)
#
#     if len(weight_types_to_add):
#         query = query \
#             .join(ChickenWeights,
#                   and_(SLTTimetable.cycle_house_id == ChickenWeights.cycle_house_id,
#                        SLTTimetable.age == ChickenWeights.age)) \
#             .join(WeightSources, ChickenWeights.source_id == WeightSources.id) \
#             .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id)
#     query = query.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
#     query = add_filters(query, filters)
#     if len(weight_types_to_add):
#         query = query.filter(WeightSourceTypes.name.in_(weight_types_to_add))
#     output = pd.read_sql_query(compile_query(query), postgres_engine)
#     return output
#
#
# def update_slt_timetable(session: Session, filters: Filter, weight_types_to_add: List[str]):
#     cycle_id = client_utils.get_cycle_house_id(session, farm_name, cycle_name, house_mane)
#     source_id = 118  # slt source type id
#
#     age = None
#     harvesting_date = None
#     stop_feed_date = None
#     feed_lifting_datetime = None
#     harvesting_start_date = None
#     slt_date = None
#     fasting_start_dt = None
#     fasting_time = None
#     birds_amount = None
#     weight = None
#     comment = None
#
#     slt_timestable_row = SLTTimetable(
#         cycle_house_id=cycle_id,
#         date=harvesting_date,
#         stop_feed_dt=stop_feed_date,
#         lifting_dt=feed_lifting_datetime,
#         harvest_dt=harvesting_start_date,
#         slt_dt=slt_date,
#         fasting_start_dt=fasting_start_dt,
#         fasting_time=fasting_time,
#         age=age,
#         bird_count=birds_amount,
#     )
#
#     chicken_weights_row = ChickenWeights(
#         cycle_house_id=cycle_id,
#         source_id=source_id,
#         age=age,
#         weight=weight,
#         confidence=None,
#         updated=datetime.now(),
#         comment=comment
#     )
#
#     slt_timestable_added_id = upsert_entity(session, slt_timestable_row, update_on_conflict=True)
#     target_weights_added_id = upsert_entity(session, chicken_weights_row, update_on_conflict=True)
#
#
# def delete_update_slt_timetable(session: Session, filters: Filter):
#     old_data = get_slt_timetable(session, filter, ['SLT'])
#     old_data_slt_table_ids = [int(old_data["slt_timetable_id"][i]) for i in range(len(old_data))]
#     old_data_target_weights_ids = [int(old_data["chicken_weights_id"][i]) for i in range(len(old_data))]
#
#     delete_ids_slt_table = session.query(SLTTimetable) \
#         .filter(SLTTimetable.id.in_(old_data_slt_table_ids)) \
#         .delete()
#
#     delete_ids_target_weights = session.query(ChickenWeights) \
#         .filter(ChickenWeights.id.in_(old_data_target_weights_ids)) \
#         .delete()


def generate_slt_table_from_manuals(client: str, manuals_postrfix: str, output_fname: str):
    manual_weights = manual_weights_manager.get_all_manual_weights(client, manuals_postrfix,
                                                                   Filter())

    manual_weights_slt = manual_weights[manual_weights['age'] % 7 != 0]
    manual_weights_slt = manual_weights_slt.rename(columns={"age": "slt_age"})
    devices = load_devices_from_csv(device_csv)
    devices_with_slt_age = pd.merge(devices, manual_weights_slt, how='inner', on=['cycle', 'farm', 'house'])[
        list(devices.columns) + ['slt_age']]

    devices_with_slt_age = devices_with_slt_age.dropna(1, how='all').drop(columns=['google_id']).dropna(0, how='any')

    devices_with_slt_age['date'] = list(
        map(lambda x: get_datetime_for_age(x[1], x[1]['slt_age']), devices_with_slt_age.iterrows()))
    devices_with_slt_age = devices_with_slt_age.groupby(['cycle', 'house'], as_index=False).first()
    save_slt_table(devices_with_slt_age[['cycle', 'house', 'date']], output_fname)
    print("SLUT timetable for {} was saved to {}".format(client, output_fname))
    pass


def match_slt_age(df: pd.DataFrame,
                  df_slt: pd.DataFrame,
                  new_col_name: str = 'slt_age',
                  date_col_name: str = 'date'
                  ) -> pd.DataFrame:
    match_columns = ['cycle', 'house']
    if any(c not in df.columns for c in ['cycle', 'house', 'cycle_start_day']):
        print(f'To matck slt age df should have {match_columns} and cycle_start_day columns')
        return df
    df = pd.merge(df, df_slt[match_columns + [date_col_name]], how='left', on=match_columns)
    try:
        df[new_col_name] = list(
            map(lambda r: get_age_from_datetime(r[1][date_col_name], r[1]['cycle_start_day']),
                df.iterrows()))
    except:
        pass
    return df


def combine_multy_slt_house(df: pd.DataFrame,
                            age_col_name: str,
                            weight_cols_to_adjust: List[str],
                            mode: str = 'min',
                            max_age_diff_influence: int = 7,
                            set_target_age=None,
                            ) -> pd.DataFrame:
    """

    :param df:
    :param age_col_name:
    :param weight_cols_to_adjust:
    :param mode: ['min', 'max', 'set']
        'max': adjust tu max age in df
        'min': adjust tu min age in df
        'set': adjust tu the set_target_age. REQUIRE set_target_age initialization
    :param set_target_age:
    :return:
    """
    if mode == 'set' and set_target_age is None:
        raise ValueError(f"'set' mode requires set_target_age initialization")
    elif len(df) == 1:
        return df

    def get_target_age(mode: str, age_series: pd.Series):
        min_slt_age = age_series.min()
        max_slt_age = age_series.max()

        if mode == 'min':
            return min_slt_age
        elif mode == 'max':
            return max_slt_age
        elif mode == 'set':
            return set_target_age
        else:
            raise ValueError(f"combine_multy_slt_house: WRONG mode value {mode} ")

    def adjust_weight_from_to(weight: float,
                              standard: pd.Series,
                              from_age: int,
                              to_age: int):
        weight_s = pd.Series([weight], index=[from_age])
        w_is_kg = manual_weights_manager.check_if_all_kg(weight_s)
        st_is_kg = manual_weights_manager.check_if_all_kg(standard)
        if w_is_kg and not st_is_kg:
            standard = manual_weights_manager.convert_to_kg(standard)
        if not w_is_kg and st_is_kg:
            standard = manual_weights_manager.convert_to_g(standard)

        adjusted = adjust_standard_to_values(standard,
                                             weight_s,
                                             vis=False,
                                             smooth_window=1,
                                             useFirstStandardValue=True,
                                             useLastStandardValue=False)

        # dif = weight - standard.loc[from_age] # WAS PROBLEM WITH UNITS
        # t2 = standard.loc[to_age] + (dif * to_age / from_age)
        return adjusted[to_age]

    # necessary for obtaining standard weight and interpolation
    farms = df['farm'].unique()
    if len(farms) != 1:
        print(f"house_slt_data has more then 1 unique farm")
        exit(-1)
    farm = farms[0]
    _, standard = standards_manager.get_standard_weights(farm)
    standard = standard['Weights']
    house_slt_data = df.sort_values(age_col_name)

    house_slt_data[f'adj_{age_col_name}'] = get_target_age(mode, house_slt_data[age_col_name])

    house_slt_data[age_col_name] = house_slt_data[age_col_name].astype(int)

    house_slt_data[f'delta_{age_col_name}'] = abs(house_slt_data[age_col_name] - house_slt_data[f'adj_{age_col_name}'])

    for weight_col in weight_cols_to_adjust:
        house_slt_data[f'adj_{weight_col}'] = manual_weights_manager.convert_to_g(
            house_slt_data.set_index(age_col_name)[weight_col]).values
        house_slt_data[f'adj_{weight_col}'] = list(
            map(
                lambda x: adjust_weight_from_to(x[1][f'adj_{weight_col}'],
                                                standard,
                                                int(x[1][age_col_name]),
                                                int(x[1][f'adj_{age_col_name}'])),
                house_slt_data.iterrows()
            )
        )
        # pass

    house_slt_s_output = house_slt_data.iloc[0].copy()
    house_slt_df_output = pd.DataFrame()
    if ('birds_count' in house_slt_data.columns) and all([not pd.isnull(x) for x in house_slt_data['birds_count']]):
        house_slt_s_output['birds_count'] = house_slt_data['birds_count'].sum()
        for weight_col in weight_cols_to_adjust:
            try:
                house_slt_s_output[weight_col] = (house_slt_data[f'adj_{weight_col}'] * house_slt_data[
                    'birds_count']).sum() / house_slt_data['birds_count'].sum()
            except Exception as e:
                print(f"Problems with {weight_col} to get mean: {e}")
    else:

        tmp_house_slt_df = house_slt_data.copy()
        # Looking for groups to combine
        while True:
            # =========================================
            # define impact weights from delta age and birds count
            tmp_house_slt_df['impact_weights'] = 1 - tmp_house_slt_df[f'delta_{age_col_name}'] / max_age_diff_influence
            birds_count = np.nan
            if ('birds_count' in tmp_house_slt_df.columns) and all(
                    [not pd.isnull(x) for x in tmp_house_slt_df['birds_count']]):
                birds_count = tmp_house_slt_df['birds_count'].sum()
                tmp_house_slt_df['impact_weights'] *= tmp_house_slt_df['birds_count'].sum() / birds_count

            # =========================================
            # get data with not zero impact to combine
            df_to_combine = tmp_house_slt_df.loc[tmp_house_slt_df['impact_weights'] > 0].copy()

            combined_s = df_to_combine.iloc[0].copy()
            combined_s['birds_count'] = birds_count
            combined_s['n_slt_days'] = len(df_to_combine)
            combined_s[f'{age_col_name}'] = get_target_age(mode, df_to_combine[age_col_name])

            # If only one data to combine, add full
            for weight_col in weight_cols_to_adjust:
                try:
                    combined_s[weight_col] = (df_to_combine[f'adj_{weight_col}'] *
                                              df_to_combine[f'impact_weights']).sum() / df_to_combine[
                                                 f'impact_weights'].sum()

                except Exception as e:
                    print(f"Problems with {weight_col} to get mean: {e}")
            # =========================================
            # add combined_data to output df
            if len(house_slt_df_output):
                house_slt_df_output.loc[len(house_slt_df_output)] = combined_s
            else:
                house_slt_df_output = combined_s.to_frame(0).T

            # =========================================
            # get data for next iter
            tmp_house_slt_df = tmp_house_slt_df.loc[tmp_house_slt_df['impact_weights'] <= 0]
            tmp_house_slt_df[f'adj_{age_col_name}'] = get_target_age(mode, tmp_house_slt_df[age_col_name])
            tmp_house_slt_df[f'delta_{age_col_name}'] = abs(
                tmp_house_slt_df[f'{age_col_name}'] - tmp_house_slt_df[f'adj_{age_col_name}'])

            if len(tmp_house_slt_df) == 0:
                break
            else:
                continue

    return house_slt_df_output
