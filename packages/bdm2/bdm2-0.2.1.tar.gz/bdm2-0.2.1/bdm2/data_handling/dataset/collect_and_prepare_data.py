import copy
from typing import List, Dict

import numpy as np
import pandas as pd
from loguru import logger

from bdm2.data_handling.dataset.components.api_dataset_queries import api_get_cycle_house_codes, \
    api_get_usable_for_train_flags, api_get_additional_info
from bdm2.data_handling.dataset.components.dataset_params import CollectingParams
from bdm2.data_handling.dataset.components.dataset_queries import (
    get_cycle_house_codes,
    get_raw_features,
    get_additional_info,
    get_usable_for_train_flags,
)
from bdm2.utils.schemas.models.ClientSettingsManager import ClientSettings


class CollectAndPrepareData:
    """
    Class for collecting aggregated by age data for different ClientSettings from
    click-house + PG.

    Options:
        - parse_combination_from_engine() splits our standard engine name end returns
            combination as separated strings and engine name
        - get_raw_features() gets features from click, using:
                - engine_name
                - cycle_house_list
                - features_list


        - agg_by_age() aggregate data by age
            !!! now in click-table it's already aggregated till session
                so, in code we need to calc:
                        - mean by age for features
                        - sum for count
        - add_additional_info_columns() add standard pawlin columns,
            like pawlin-device-name, client| breed |gender e.t.c.

    """

    def __init__(
        self,
        client_settings: Dict[str, ClientSettings],
        collect_config: CollectingParams,
        working_features: List[str],
    ):

        #: dict of  client_settings to be sources of aggregated results
        self.client_settings: Dict[str, ClientSettings] = client_settings
        #: collecting settings
        self.collect_config: CollectingParams = collect_config
        #: list of features to be collected
        self.working_features: List[str] = working_features

    @staticmethod
    def parse_combination_from_engine(settings):
        try:
            engine_name = settings.main_config.engine_version
            client, breed_type, gender = engine_name.split("_")[2:5]
            breed_type = breed_type.replace("-", " ").replace("_", " ")

            return client, breed_type, gender, engine_name
        except Exception as ex:
            logger.error(f"Can't parse settings with ex: {ex}")
            return None, None, None, None



    @staticmethod
    def calculate_std(df_features, active_grouping):
        logger.info("start recalculating std...")
        # drop small sessions without std
        df_features["unique_sess_key"] = (
            df_features["cycle_house_code"] + df_features["device"] + df_features["age"].astype(str) + df_features["session"]
        )
        min_count_sessions = df_features[(df_features.feature_name == "count") & (df_features["value"] < 30)].unique_sess_key.unique()
        df_features.drop(df_features[df_features.unique_sess_key.isin(min_count_sessions)].index, inplace=True)

        # take all features that has std as stst_name
        # "count" values for features will be used for calculation
        all_features_names = list(set(df_features[df_features.feature_stat_name == "std"].feature_name.tolist()))

        features_dict = {}

        for feature in all_features_names:

            # filter data by current feature and 'count'
            feature_loc = df_features.loc[(df_features.feature_name == feature) | (df_features.feature_name == "count")]

            features_dict.setdefault(f"{feature}_std", [])  # pd.DataFrame(features_dict['max_axis_norm_corr_std'])

            for name, group in feature_loc.groupby(active_grouping):
                group = group.sort_values(by="session")
                # absent of std at all could be only in sess where count = 1
                # we need to drop all age group if all session the same
                if "std" not in group.feature_stat_name.values:
                    logger.info(
                        f"skipped because of no std:"
                        f"cycle_house_code = '{name[0]}' and "
                        f"device = '{name[1]}' AND feature_name = '{feature}' and age = {name[2]}"
                    )
                    continue

                # get std, mean и count arrays
                try:
                    stds = group[group["feature_stat_name"] == "std"].value.values
                    means = group[group["feature_stat_name"] == "mean"].value.values
                    counts = group[group["feature_name"] == "count"].value.values

                    # Step 1: Calculate total count of chicken for all groups
                    n_total = np.sum(counts)

                    # Step 2: Calculate overall (=weighted) mean
                    weighted_means = means * counts
                    mean_overall = np.sum(weighted_means) / n_total

                    # Step 3: Calculate combined variance
                    # Calculate variance for each group
                    var_combined = np.sum(counts * (stds**2)) + np.sum(counts * ((means - mean_overall) ** 2))
                    var_overall = var_combined / n_total

                    # Step 4: Calculate overall std
                    std_overall = np.sqrt(var_overall)

                    new_record = {active_grouping[i]: name[i] for i in range(len(active_grouping))}
                    new_record["value"] = std_overall
                    # features_dict.setdefault(f"{feature}_std", []) # new_record
                    features_dict[f"{feature}_std"].append(new_record)  # new_record
                except Exception as Ex:
                    logger.info(
                        f"cycle_house_code = '{name[0]}' and " f"device = '{name[1]}' AND feature_name = '{feature}' and age = {name[2]}"
                    )
                    logger.exception(Ex)

        output_df = pd.DataFrame(columns=active_grouping)
        for key in features_dict.keys():
            df = pd.DataFrame(features_dict[key]).rename(columns={"value": key})
            if len(output_df) == 0:
                output_df = pd.concat([output_df, df])
            else:
                output_df = output_df.merge(df)

        return output_df

    # @staticmethod
    def agg_by_age(self, df_features):
        # Ensure 'age' column is numeric
        df_features["age"] = pd.to_numeric(df_features["age"], errors="coerce")

        # stds = self.calculate_std(df_features, ['cycle_house_code', 'device', 'age'])
        # after this type calc std, not aggregated could be dropped
        df_features = df_features.loc[~(df_features.feature_stat_name == "std")]

        # Drop rows where 'age' could not be converted to numeric
        df_features = df_features.dropna(subset=["age"])

        # Group by the specified columns and calculate the mean
        df_mean_by_age = (
            df_features.groupby(
                [
                    "cycle_house_code",
                    "device",
                    "age",
                    "feature_name",
                    "feature_stat_name",
                ]
            )
            .mean(numeric_only=True)  # Ensure only numeric columns are averaged
            .reset_index()
        )

        # Create the 'feature' column by combining 'feature_name' and 'feature_stat_name'
        df_mean_by_age["feature"] = df_mean_by_age["feature_name"] + "_" + df_mean_by_age["feature_stat_name"]

        # Pivot the table to get the desired structure
        piv = df_mean_by_age.pivot_table(
            index=["age", "cycle_house_code", "device"],
            columns=["feature"],
            values="value",
        ).reset_index()

        # piv = piv.merge(stds, on=['cycle_house_code', 'device', 'age'])

        # Drop the unnecessary column if it exists
        if "count_sum" in piv.columns:
            piv.drop(columns=["count_sum"], inplace=True)

        # Separate count calculation by summing using not aggr.mean df
        count_df = (
            df_features[df_features["feature_name"] == "count"]
            .pivot_table(
                index=["age", "cycle_house_code", "device"],
                columns=["feature_name"],
                values="value",
                aggfunc="sum",
            )
            .reset_index()
        )

        # Merge the count_df with the pivot table
        piv = piv.merge(count_df, on=["age", "cycle_house_code", "device"], how="left")

        # Rename the 'count_sum' column to 'count'
        if "count_sum" in piv.columns:
            piv.rename(columns={"count_sum": "count"}, inplace=True)

        return piv

    @staticmethod
    def add_additional_info_columns(piv, client_id):
        # additional_info_df = get_additional_info(piv["cycle_house_code"].unique().tolist())
        piv = api_get_additional_info(piv)
        # specific_cols = additional_info_df.columns.tolist()
        # specific_cols.remove("device_name")
        # specific_cols.append("client_id")
        # specific_cols.append("age")
        # piv = piv.merge(additional_info_df, on=["cycle_house_code", "device"])

        piv["client_id"] = client_id
        specific_cols = piv.columns.tolist()
        # piv.drop(columns=["device"], inplace=True)
        # piv.rename(columns={"device_name": "device"}, inplace=True)
        return piv, specific_cols

    def collect_mean_data(self) -> pd.DataFrame:
        inp_features = copy.copy(self.working_features)

        df_output = pd.DataFrame()

        for client_id in self.client_settings:
            try:
                settings = self.client_settings[client_id]
                client, breed_type, gender, engine_name = self.parse_combination_from_engine(settings)
                logger.info(f"identified client: {client}\n" f"identified breed_type: {breed_type}\n" f"identified gender: {gender}")
                logger.info(f"Getting cycle-houses for {client}...")
                c_h_codes = api_get_cycle_house_codes(client_name=client, breed_name=breed_type, gender=gender)
                logger.info(f"Getting raw features for {client}...")
                df_features = get_raw_features(
                    engine_name=engine_name,
                    cycle_house_list=c_h_codes,
                    features_list=inp_features,
                )
                if df_features.empty:
                    logger.warning(f"No features found for {client}... Skipping...")
                    continue
                df_features = api_get_usable_for_train_flags(df_features)
                # df_features = self.add_usable_flags(df=df_features, cycle_house_code_list=c_h_codes)

                _initial_cycle_houses_for_settings = len(c_h_codes)
                _gotten_from_click = len(df_features.cycle_house_code.unique().tolist())

                logger.info(f"full count of cycle-houses for chosen combination: {_initial_cycle_houses_for_settings}")
                logger.info(f"have found features for {_gotten_from_click} cycle-houses")

                piv = self.agg_by_age(df_features)

                usable_map = df_features[["cycle_house_code", "age", "device", "usable_for_train"]].drop_duplicates()

                piv.set_index(["cycle_house_code", "age", "device"], inplace=True)
                usable_map = usable_map.set_index(["cycle_house_code", "age", "device"])["usable_for_train"].to_dict()
                piv["usable_for_train"] = piv.index.map(usable_map)
                piv.reset_index(inplace=True)
                piv, specific_cols = self.add_additional_info_columns(piv, client_id)
                # TODO: сейчас в клике лажовый релабилити, ребята дролжны на своей стороне при записи это разрулить
                # и тошда тут нужно будет поправить обрабокту релабилити колонок,
                # отдельно их агрегировать и конкат например
                # Определение порядка колонок, которые нужно переместить в начало

                remaining_columns = [col for col in piv.columns if col not in specific_cols]

                # Новый порядок колонок
                new_column_order = specific_cols + remaining_columns

                # Создание нового DataFrame с нужным порядком колонок
                piv = piv[new_column_order]

                piv["manual_weights_postfix"] = settings.manual_weights_postfix
                piv["engine_postfix"] = engine_name

                df_output = pd.concat([df_output, piv])

            except Exception as e:
                logger.error(f"Error while collecting data for {client_id}: {e}")
                logger.exception(e)
                continue

        return df_output

    def run(self):
        # collect mean per age measurements for all client_settings
        logger.info("Collecting data")
        df = self.collect_mean_data()
        df = df.drop_duplicates()
        return df
