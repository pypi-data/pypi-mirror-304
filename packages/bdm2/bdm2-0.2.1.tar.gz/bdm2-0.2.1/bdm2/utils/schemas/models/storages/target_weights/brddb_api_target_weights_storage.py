import copy
import logging
import warnings
from dataclasses import dataclass
from typing import Optional, Union

import numpy as np
import pandas as pd

from bdm2.data_handling.generated_data.checks.interpolation_outliers_search.components.common import colorstr
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.weights_structure import WeightColumns




from brddb.models.postgres.weights import ChickenWeights

from bdm2.utils.schemas.models.storages.actual_clients_info_storage.brddb_actual_client_info_storage import \
    BrdDBActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.brddbapi_client.brddb_client import brddb_client
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsColumnsNew, \
    TargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import ActualPostfixError

# from src.storages.devices.devices_storage import DevicesStorage



warnings.simplefilter(action="ignore", category=FutureWarning)
logger = logging.getLogger("pipeline_runner")


@dataclass
class TargetWeightsInputColumns(ColumnsStruct):
    """
    Chicken_weights table columns.
    Used for converting input data to PostgresSQL ChickenWeights table

    """

    cycle_house_id: str = ChickenWeights.cycle_house_id.key
    src_id: str = ChickenWeights.source_id.key

    age: str = ChickenWeights.age.key
    weight_value: str = ChickenWeights.weight.key
    confidence: str = ChickenWeights.confidence.key

    updated: str = ChickenWeights.updated.key
    comment: str = ChickenWeights.comment.key

    @property
    def weight(self) -> WeightColumns:
        return WeightColumns(
            weight=self.weight_value,
            age=self.age,
            confidence=self.confidence,
        )

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        df_output = df.copy()
        try:
            df_output[self.cycle_house_id] = df_output[self.cycle_house_id].astype(int)
            df_output[self.src_id] = df_output[self.src_id].astype(int)
            df_output[self.age] = df_output[self.age].astype(int)
            df_output[self.weight_value] = df_output[self.weight_value].astype(float)
            df_output[self.confidence] = df_output[self.confidence].astype(float)
            df_output[self.updated] = pd.to_datetime(df_output[self.updated])
            return df_output
        except Exception as e:
            logger.exception(
                colorstr(
                    "red",
                    f"TargetWeightsInputColumns:convert_df_types: could not convert:{e}",
                ),
            )
            return df.copy()


@dataclass
class PostgresTargetWeightsColumns(TargetWeightsColumnsNew, TargetWeightsInputColumns):
    """"""

    id: str = ChickenWeights.id.key


class BrdDbApiTargetWeightsStorage(TargetWeightsStorage):
    """
    Chicken weights storage on Postgres API BRDDB_API

    """

    def __init__(
        self,
        device_storage,
        units: str,
        actual_info_storage: BrdDBActualClientsInfoStorage,
    ):
        TargetWeightsStorage.__init__(
            self,
            units,
            actual_info_storage=actual_info_storage,
        )
        self.device_storage = device_storage
        self.devices_format = device_storage.output_default_format

        self._inner_format = PostgresTargetWeightsColumns(
            id="id",
            farm="farm",
            cycle="cycle",
            house="house",
            age="age",
            weight_value="weight",
            # confidence="confidence",
            src_id="weight_src_id",
            weights_src_name="weight_src",
            weights_postfix="weight_src_postfix",
        )

    def get_target_weights(
        self,
        src_name: str,
        weights_postfix: Optional[str],
        filters: Filter,
        output_df_format: Optional[TargetWeightsColumnsNew] = None,
    ) -> pd.DataFrame:
        """
        Get weights for ACTUAL weghts postfix for specified src_name

        :param src_name: should be in
        :param weights_postfix:
        :param filters: define devices scope to get weights
        :param output_df_format:
        :return:
        """
        weights_df_output = brddb_client.get_actual_targets_by_src_types(
            src_type=src_name,
        ).rename(
            columns={
                "weight_source_type_name": "src_name",
                "postfix": "manual_weights_postfix",
                "weight": "adjusted_weight",
                "age": "daynum",
            },
        )
        weights_df_output["adjusted_weight"] = weights_df_output[
            "adjusted_weight"
        ].apply(lambda x: np.round(x, 4))
        cycle_houses_df = brddb_client.get_cycle_houses_table().rename(
            columns={"id": "cycle_house_id", "cycle_house_name": "cycle"},
        )
        houses_df = brddb_client.get_houses_table().rename(
            columns={"id": "house_id", "name": "house"},
        )
        farms_df = brddb_client.get_farms_table().rename(
            columns={"id": "farm_id", "farm_name": "farm"},
        )

        output = (
            weights_df_output.merge(
                cycle_houses_df[["cycle", "cycle_house_id", "house_id"]],
                on="cycle_house_id",
            )
            .merge(houses_df[["house", "house_id", "farm_id"]], on="house_id")
            .merge(farms_df[["farm", "farm_id"]], on="farm_id")
        )

        return output

    @property
    def inner_format(self) -> ColumnsStruct:
        return copy.deepcopy(self._inner_format)

    def output_default_format(self) -> ColumnsStruct:
        raise NotImplementedError

    def convert_to_input_format(self):
        raise NotImplementedError

    def update_target_weights(
        self,
        weights_df: pd.DataFrame,
        input_df_format: TargetWeightsColumnsNew,
        need_commit: bool = True,
    ):
        raise NotImplementedError

    def delete_target_weights(
        self,
        src_name: str,
        weights_postfix: Union[str, None],
        filters: Filter,
        need_commit: bool = True,
    ) -> int:
        """
        After use session.commit()

        """
        raise NotImplementedError
