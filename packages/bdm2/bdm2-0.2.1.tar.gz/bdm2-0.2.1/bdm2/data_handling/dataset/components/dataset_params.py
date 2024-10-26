from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
import yaml
from loguru import logger

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter, FilterChild
from bdm2.utils.schemas.models.ClientSettingsManager import ClientSettings
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.brddb_actual_client_info_storage import \
    BrdDBActualClientsInfoStorage


# from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import (
#     ActualClientsInfoStorage,
#     PostgresActualClientsInfoStorage,
# )


from bdm2.utils.schemas.models.storages.actual_clients_info_storage.utils.utils import (
    generate_actual_client_settings,
)
from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorageColumnsNew

# from bdm2.utils.schemas.models.storages.devices.devices_storage import (
#     DevicesStorageColumnsNew,
#     DevicesStorage,
# )

from bdm2.utils.schemas.models.storages.devices.brddb_api_devices_storage import (
    BrddbAPIDevicesStorage
)
# from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import (
#     PostgresDevicesStorage,
# )
from bdm2.utils.schemas.models.storages.target_weights.brddb_api_target_weights_storage import (
    BrdDbApiTargetWeightsStorage,
)
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsColumnsNew
#     TargetWeightsStorage,
# )


@dataclass
class CollectingParams:
    input_test_cycle_houses_file_path: str
    features_to_collect: List[str]
    # age_column_name: str = 'daynum'
    input_combinations_file_path: str = None
    manual_weights_postfix_col: str = "manual_weights_postfix"
    engine_postfix_col: str = "engine_postfix"
    results_postfix_col: str = "results_postfix"
    client_id_col: str = "client_id"

    # always add volume_norm_corr as it is used in target density calculation
    target_density_required_features: List[str] = field(
        default_factory=lambda: ["volume_norm_corr"]
    )
    target_weight_col: Optional[str] = (
        "adjusted_weight"  # if None, will not match target weigh
    )
    target_density_col: Optional[str] = (
        "target_density"  # if None, will not calculate target density
    )

    @property
    def test_filters(self):
        if (
                self.input_test_cycle_houses_file_path is not None
                and self.input_test_cycle_houses_file_path != ""
        ):
            return [
                Filter(**x)
                for x in yaml.safe_load(open(Path(self.input_test_cycle_houses_file_path)))
            ]

    @staticmethod
    def init_test_devices(
            devices_storage: BrddbAPIDevicesStorage,
            test_filters: List[Filter],
            output_format: Optional[DevicesStorageColumnsNew] = None,
    ) -> pd.DataFrame:
        if output_format is None:
            output_format = DevicesStorageColumnsNew()

        test_devices = pd.DataFrame(columns=output_format.get_columns())
        if len(test_filters) > 0:
            for f in test_filters:
                if f.isempty():
                    continue
                tmp_devices = devices_storage.get_devices(
                    filters=f, output_format=output_format
                )
                test_devices = pd.concat([test_devices, tmp_devices], ignore_index=True)
        test_devices = test_devices.drop_duplicates(subset=list(test_devices.columns))
        return test_devices


class TrainSetManagerChild:
    def __init__(
            self,
            config_path: Optional[str] = None,
            config: Optional[Dict] = None,
            actual_info_storage: Optional[BrdDBActualClientsInfoStorage] = None,
    ):
        self.actual_info_storage = (
                actual_info_storage or self._initialize_default_info_storage()
        )
        if config:
            self.config = self.parse_config(config, self.actual_info_storage)
        elif config_path:
            self.config = self.load_config(config_path)
        else:
            raise ValueError("Either config_path or config must be provided")

    def _initialize_default_info_storage(self) -> BrdDBActualClientsInfoStorage:
        logger.info(
            "No actual_info_storage provided. Using PostgresActualClientsInfoStorage."
        )
        return BrdDBActualClientsInfoStorage()

    def parse_config(
            self,
            config: Dict,
            actual_info_storage: Optional[BrdDBActualClientsInfoStorage] = None,
    ) -> Dict[str, ClientSettings]:
        new_config = {}

        for key, settings in config.items():
            filter_settings = settings.get("filter_settings")
            client_settings = settings.get("client_settings")

            if not filter_settings:
                logger.error(f"Filter settings not defined in config for '{key}'.")
                continue

            filter_obj = FilterChild(kwargs=filter_settings)

            if not client_settings:
                logger.error(f"Client settings not defined in config for '{key}'.")
                continue

            try:
                cs = (
                    generate_actual_client_settings(
                        filters=filter_obj,
                        **client_settings,
                        actual_info_storage=actual_info_storage,
                    )
                    if actual_info_storage
                    else ClientSettings(filters=filter_obj, **client_settings)
                )
                new_config[key] = cs
            except Exception as e:
                logger.exception(
                    f"Failed to initialize ClientSettings for '{key}': {e}"
                )

        return new_config

    def load_config(self, config_path: str) -> Dict[str, ClientSettings]:
        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
            return self.parse_config(config, self.actual_info_storage)
        except FileNotFoundError:
            logger.error(f"Configuration file not found at path: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file at path: {config_path} - {e}")
            raise


@dataclass
class PostprocessingParams:
    # extrapolate_volumes: bool = True
    # use_autoencoder_interpolation: bool = True
    # do_post_processing: bool = True

    column_group_first: str = "farm"
    # correction_coef: str = "density_correction_coef_mean" # !!! moved to function input as argument
    target_weight_colname: str = "adjusted_weight"

    # use correction_coef
    calc_target_density: bool = True
    # use_shape_corr_coef_in_target_density: bool = True
    target_density_colname: str = "target_density"


class DataPostprocess:
    def __init__(
            self,
            config: PostprocessingParams = PostprocessingParams(),
            weights_storage: Optional[BrdDbApiTargetWeightsStorage] = None,
    ):

        self.config = config
        self.weights_storage = weights_storage
        if self.weights_storage is None:
            self.weights_storage = BrdDbApiTargetWeightsStorage(
                device_storage=BrddbAPIDevicesStorage(), units=WEIGHTS_UNITS["kg"]
            )

    def get_target_density(
            self, df: pd.DataFrame, weight_colname: str, volume_norm_corr_colname: str
    ) -> pd.Series:
        """
        Define target density

        """
        output_s = df[weight_colname] / df[volume_norm_corr_colname]
        return output_s

    def match_targets_and_target_density(
            self,
            extrapolated_df: pd.DataFrame,
            volume_column: Optional[str],
            weights_postfix_colname: str,
            age_column: Optional[str] = None,
            target_weight_col: Optional[str] = None,
            target_density_col: Optional[str] = None,
    ):
        """
        Will be matched Likely_target weights

        :param extrapolated_df:
        :param volume_column:
        :param weights_postfix_colname:
        :return:
        @param extrapolated_df:
        @param volume_column:
        @param weights_postfix_colname:
        @param target_density_col:
        @param target_weight_col:
        @param age_column:
        """

        if extrapolated_df.empty:
            return extrapolated_df

        if target_weight_col is None:
            target_weight_col = self.config.target_weight_colname
        if target_density_col is None:
            target_density_col = self.config.target_density_colname

        indexes = [c for c in extrapolated_df.index.names if c is not None]

        loc_df = extrapolated_df.copy()
        if len(indexes):
            loc_df.reset_index(inplace=True)

        output_format = TargetWeightsColumnsNew(
            weight_value=target_weight_col,
            weights_postfix="likely_weight_postfix",
            age=age_column,
        )
        match_columns = output_format.house_index.get_columns() + [output_format.age]
        columns_to_match = [
            output_format.weight.weight,
            output_format.weight_src.src_name,
            output_format.weight_src.postfix,
        ]

        logger.info(
            f"Gettig target weights from {self.weights_storage.__class__.__name__}"
        )
        df_output = None

        for (farm, weights_postfix), group_df in loc_df.groupby(
                [output_format.farm, weights_postfix_colname]
        ):

            filters = Filter(farms=[farm])

            weights_df = self.weights_storage.get_target_weights(
                src_name="Likely_targets",
                weights_postfix=weights_postfix,
                filters=filters,
            )

            doc_weights = self.weights_storage.get_target_weights(
                src_name="DOC", weights_postfix="", filters=filters
            )

            weights_df.rename(
                columns={"manual_weights_postfix": output_format.weight_src.postfix}, inplace=True
            )

            if any(weights_df.duplicated()) or any(doc_weights.duplicated()):
                logger.warning(
                    f"get_target_weights() "
                    f"for {farm} returned duplicates. Duplicated will be dropped."
                )
                weights_df.drop_duplicates(subset=weights_df.columns, inplace=True)
                doc_weights.drop_duplicates(subset=weights_df.columns, inplace=True)

            for c in columns_to_match:
                if c in group_df.columns:
                    group_df = group_df.drop(columns=[c])


            # weights_df.rename(columns={"weight": "adjusted_weight"}, inplace=True)
            doc_weights.rename(columns={"weight": "doc_weight",
                                        "daynum": "age",
                                        "adjusted_weight": "doc_weight"
                                        }, inplace=True)
            weights_df.rename(columns={"daynum": "age"}, inplace=True)
            # weights_df = weights_df.loc[~(weights_df.age == 0)]
            group_df = pd.merge(
                group_df,
                weights_df[match_columns + columns_to_match],
                on=match_columns,
                how="left",
            )
            # except age column
            group_df = pd.merge(
                group_df,
                doc_weights[match_columns[:-1] + ["doc_weight"]],
                on=match_columns[:-1],
                how="left",
            )

            # df_m = pd.merge(df, doc_weights[
            #     doc_weights_format.house_index.get_columns() + [doc_weights_format.weight_value]],
            #                 on=device_storage.output_default_format.house_index.get_columns(), how='left')
            if df_output is None:
                df_output = group_df
            else:
                df_output = pd.concat([df_output, group_df], ignore_index=True)

        df_output = output_format.convert_df_types(df_output)

        df_output[target_density_col] = self.get_target_density(
            df=df_output,
            weight_colname=target_weight_col,
            volume_norm_corr_colname=volume_column,
        )

        if any(df_output.duplicated()):
            df_output.drop_duplicates(subset=df_output.columns, inplace=True)
        if len(indexes):
            df_output.set_index(indexes, inplace=True)
        return df_output
