from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import yaml
from loguru import logger

from bdm2.constants.global_setup.data import (
    house_match_columns,
    standards_match_columns,
)
from bdm2.constants.global_setup.data_columns import volume_norm_corr_mean
from bdm2.constants.global_setup.env import AWS_ACCESS_KEY, AWS_SECRET_KEY
from bdm2.data_handling.dataset.collect_and_prepare_data import CollectAndPrepareData
from bdm2.data_handling.dataset.components.dataset_params import (
    CollectingParams,
    TrainSetManagerChild,
    DataPostprocess,
)
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
# from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import (
#     PostgresActualClientsInfoStorage,
# )
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.brddb_actual_client_info_storage import \
    BrdDBActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.devices_storage import (
    DevicesStorageColumnsNew,
)
from bdm2.utils.schemas.models.storages.devices.brddb_api_devices_storage import (
    BrddbAPIDevicesStorage,
)
from bdm2.utils.schemas.models.storages.target_weights.brddb_api_target_weights_storage import (
    BrdDbApiTargetWeightsStorage,
)


class DatasetCollector:
    def __init__(
            self,
            collecting_config_path: Optional[str] = None,
            input_combinations_config: Optional[Dict] = None,
    ):
        self.collecting_config_path = collecting_config_path
        self.input_combinations_config = input_combinations_config
        self.input_combinations_file_path = None

        if self.collecting_config_path:
            self.collecting_settings = CollectingParams(
                **yaml.load(open(self.collecting_config_path), yaml.Loader)
            )
            self.input_combinations_file_path = (
                self.collecting_settings.input_combinations_file_path
            )
        else:
            raise ValueError(
                "Either collecting_config_path or collecting_config must be provided"
            )

    @property
    def actual_info_storage(self):
        return BrdDBActualClientsInfoStorage()

    @property
    def devices_storage(self):
        return BrddbAPIDevicesStorage()

    @property
    def weights_storage(self):
        return BrdDbApiTargetWeightsStorage(
            device_storage=self.devices_storage, units="kg",
            actual_info_storage=self.actual_info_storage
        )

    @property
    def devices_format(self):
        return DevicesStorageColumnsNew()

    @staticmethod
    def split_train_validation(
            df,
            split_train_validation_gb,
            split_train_validation_percent: float = 0.1,
            split_train_validation_shuffle: bool = True,
    ):
        validation_data_indexes = []
        train_data_indexes = []

        assert all(
            [c in df.reset_index().columns for c in split_train_validation_gb]
        ), f"not all split_train_validation_gb are in df in split_train_validation()"

        for (gb_label), subset in df.groupby(split_train_validation_gb):
            unique_indexes = list(subset.index.unique())
            if split_train_validation_shuffle:
                np.random.shuffle(unique_indexes)

            n_to_valid = int(
                np.ceil(len(unique_indexes) * split_train_validation_percent)
            )  # subset.index.unique()*0.1
            if len(unique_indexes) > 1:
                tr = unique_indexes[n_to_valid:]
                v = unique_indexes[:n_to_valid]
                validation_data_indexes.extend(v)
                train_data_indexes.extend(tr)
            else:
                tr = unique_indexes
                v = []
                train_data_indexes.extend(tr)
            logger.info(
                f"for {gb_label}: \ttrain - {len(set(tr))}, \tvalidation - {len(set(v))}"
            )
        validation_data_indexes = list(set(validation_data_indexes))
        train_data_indexes = list(set(train_data_indexes))

        return validation_data_indexes, train_data_indexes

    def set_train_test_flags(
            self,
            df: pd.DataFrame,
            test_filters: List[Filter],
            extra_split_train_test_gb: List[str],
            split_train_validation_percent: float,
            split_train_validation_shuffle: bool,
            flag_col: str = "train_flag",
    ) -> pd.DataFrame:
        """
        Set train test flag to input df

        :param df: collected DataFrame
        :param test_filters: list of filters, that define devices of test scope
        :param flag_col: column name to output flag

        Extra splitting will be performed for extra_split_train_test_gb groups,
        which does not have devices in test scope.
        for splitting :func:`split_train_validation` will be used

        :param extra_split_train_test_gb:  group to be split on train test
        :param split_train_validation_percent: percent of houses, that will be set as test.
        :param split_train_validation_shuffle: shuffle devices inside group before choosing test houses
        :return: pd.DataFrame
        """
        loc_df = df.copy()
        initial_indexes = [i for i in loc_df.index.names if i is not None]
        if len(initial_indexes) > 0:
            loc_df.reset_index(inplace=True)
        loc_df[flag_col] = 1
        for f in test_filters:
            filtered_df = f.filter_res_df_csv(loc_df, age_col="daynum")
            loc_df.loc[filtered_df.index, flag_col] = 0

        df_output = pd.DataFrame()
        if loc_df.empty:
            return loc_df
        for label, group in loc_df.groupby(extra_split_train_test_gb):
            if any(group[flag_col] == 0):
                logger.info(f"Test for {label} was defined manualy")
                df_output = pd.concat([df_output, group])
                continue

            test_index, train_index = self.split_train_validation(
                group.reset_index().set_index(house_match_columns),
                split_train_validation_gb=extra_split_train_test_gb,
                split_train_validation_percent=split_train_validation_percent,
                split_train_validation_shuffle=split_train_validation_shuffle,
            )
            group.loc[
                group.reset_index()
                .set_index(house_match_columns)
                .index.isin(test_index),
                flag_col,
            ] = 0
            df_output = pd.concat([df_output, group])
        if len(initial_indexes):
            df_output = df_output.set_index(initial_indexes)
        df_output = df_output.sort_index()
        return df_output

    @staticmethod
    def extract_first_part(value):
        return value.split('-')[0]

    def apply_farm_coeffs(self, collected_df: pd.DataFrame):

        print("apply mass corr. coeffs by farm")
        collected_df['farm_code'] = collected_df['cycle_house_code'].apply(self.extract_first_part)

        def center_df(
                row: pd.Series, coeff: dict, farm_col: str, age_col: str, mass_col: str
        ):
            farm = row[farm_col]
            age = row[age_col]
            weight = row[mass_col]

            if farm not in coeff.columns:
                farm = 'default'

            coeff = coeff[farm].loc[age]

            return weight / (coeff + 1)

        # add targets, doc and calc target density
        coeff = ''
        from bdm2.utils.s3.connector import S3Handler
        conn_s3 = S3Handler(access_key=AWS_ACCESS_KEY,
                            secret_key=AWS_SECRET_KEY,
                            region_name="us-east-1")
        # #birdoo-datasets
        # # base-dataset
        s3_datasets_root = conn_s3.root_bucket.Bucket("birdoo-datasets")
        # s3_base_dataset_root = conn_s3.root_bucket.Bucket("base-dataset")

        dataset_obj = list(
            s3_datasets_root.objects.filter(Prefix="configs/coeff_by_farm_combined.csv"))
        dataset_key = dataset_obj[0].key
        obj = s3_datasets_root.Object(dataset_key)
        response = obj.get()
        coef_data = response['Body'].read()
        import io
        coef_dict = pd.read_csv(io.BytesIO(coef_data), sep=";")
        collected_df['mass_corr_mean_farm_coeffs'] = collected_df.apply(
            center_df,
            axis=1,  # Задаем ось (строки)
            coeff=coef_dict,
            farm_col='farm_code',
            age_col='age',
            mass_col='mass_corr_mean'
        )
        collected_df.rename(columns={"mass_corr_mean": "mass_corr_mean_no_farm_coeffs",
                                     "mass_corr_mean_farm_coeffs": "mass_corr_mean"},
                            inplace=True)

        return collected_df

    def run(self):
        try:
            if self.input_combinations_file_path:
                local_train_set = TrainSetManagerChild(
                    config_path=self.input_combinations_file_path,
                    actual_info_storage=self.actual_info_storage,
                ).config
            else:
                local_train_set = TrainSetManagerChild(
                    config=self.input_combinations_config,
                    actual_info_storage=self.actual_info_storage,
                ).config
            data_collector = CollectAndPrepareData(
                local_train_set,
                self.collecting_settings,
                # age_column_name=coll_params.age_column_name,
                working_features=self.collecting_settings.features_to_collect,
            )
            # collect data using input features and client settings
            # aggr. by age
            # add standard pawlin columns
            collected_df = data_collector.run()
            # todo add farm centering
            collected_df = self.apply_farm_coeffs(collected_df)
            data_postprocesssor = DataPostprocess(weights_storage=self.weights_storage)

            # Match likely|doc weights and calc target density
            working_df = data_postprocesssor.match_targets_and_target_density(
                collected_df,
                volume_column=volume_norm_corr_mean,
                weights_postfix_colname="manual_weights_postfix",
                age_column="age",
            )

            # add test|train splitting flags
            working_df = self.set_train_test_flags(
                df=working_df,
                test_filters=self.collecting_settings.test_filters,
                extra_split_train_test_gb=standards_match_columns,
                split_train_validation_percent=0.15,
                split_train_validation_shuffle=False,
                flag_col="train_flag",
            )
        except Exception as e:
            logger.exception(e)
            raise e

        if "age" in working_df.columns.tolist():
            working_df.rename(columns={"age": "daynum"}, inplace=True)
        return working_df


if __name__ == "__main__":
    config_file_path = "configs/fish_base_dag_config.yaml"
    collector = DatasetCollector(collecting_config_path=config_file_path)
    dataset = collector.run()
    logger.info(len(dataset))
