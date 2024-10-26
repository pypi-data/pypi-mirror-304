#  Copyright (c) Anna Sosnovskaya

"""
As it could be different sources of target weights (local files, relote databases, etc.)
there is a union class for working with chicken weights

"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from brddb.utils.common import colorstr

from bdm2.data_handling.generated_data.manual_weights_manager import (
    convert_to_g,
    convert_to_kg,
)
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.device_data_struct import HouseColumns
from bdm2.utils.schemas.models.data_structures.weights_structure import (
    WeightColumns,
    WeightSrcColumns,
    WEIGHTS_UNITS,
)
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import StorageBase
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.actual_clients_info_storage import (
    ActualClientsInfoStorage,
)
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import (
    ActualPostfixError,
)


@dataclass
class TargetWeightsColumnsNew(ColumnsStruct):
    """
    Struct for storing data format of TargetWeightsStorage. It defines TargetWeightsStorage working data format
    (each attribute is available data for TargetWeightsStorage). It actually stores columns names of input/output data

    It helps to switch between storages easily.

    .. warning::
        Each implementation on TargetWeightsStorage has to be able to work with data, that has current struct' columns names
        self.get_devices() must return data with DevicesStorageColumn column' names
        self.update_devices() must be able to update data with DevicesStorageColumn column' names

    DevicesStorage data has full house' hierarchy information:
        farm -> house -> device

    Weight information:
        weights_src_name -> weights_postfix -> age -> weight_value
    """

    # HouseColumns
    farm: str = "farm"
    cycle: str = "cycle"
    house: str = "house"
    breed_type: str = "breed_type"
    gender: str = "gender"

    # WeightColumns
    age: str = "age"
    weight_value: str = "weight"
    confidence: str = "confidence"

    # WeightSrcColumns
    weights_src_name: str = "src_name"
    weights_postfix: str = "weight_postfix"
    updated: str = "updated"
    comment: str = "comment"

    @property
    def house_index(self) -> HouseColumns:
        return HouseColumns(
            farm=self.farm,
            cycle=self.cycle,
            house=self.house,
        )

    @property
    def weight(self) -> WeightColumns:
        return WeightColumns(
            weight=self.weight_value, age=self.age, confidence=self.confidence
        )

    @property
    def weight_src(self) -> WeightSrcColumns:
        return WeightSrcColumns(
            src_name=self.weights_src_name, postfix=self.weights_postfix
        )

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        df_output = df.copy()
        try:
            df_output = self.weight.convert_df_types(df)
            df_output = self.weight_src.convert_df_types(df_output)
            df_output = self.house_index.convert_df_types(df_output)
            return df_output
        except Exception as e:
            print(
                colorstr(
                    "red",
                    f"TargetWeightsInputColumns:convert_df_types: could not convert\n{e}",
                )
            )
            return df.copy()


class TargetWeightsStorage(StorageBase):
    """
    Class for performing manipulation with all chicken weights. Work with dataframes with TargetWeightsColumnsNew
    columns structure

    """

    def __init__(self, units: str, actual_info_storage: ActualClientsInfoStorage):
        self.actual_info_storage = actual_info_storage

        assert units in WEIGHTS_UNITS
        self._inner_format = TargetWeightsColumnsNew()
        self.units = units
        if self.units == WEIGHTS_UNITS["kg"]:
            self.round = 4
        elif self.units == WEIGHTS_UNITS["g"]:
            self.round = 1

    @property
    def output_default_format(self) -> TargetWeightsColumnsNew:
        return TargetWeightsColumnsNew()
        # output = {}
        # loc_inner_format = self.inner_format
        # for atr in TargetWeightsColumnsNew.__annotations__:
        #     output[atr] = loc_inner_format.__dict__[atr]
        # return TargetWeightsColumnsNew(**output)

    @property
    def inner_as_default_format(self) -> TargetWeightsColumnsNew:
        output = {}
        loc_inner_format = self.inner_format
        for atr in TargetWeightsColumnsNew.__annotations__:
            output[atr] = loc_inner_format.__dict__[atr]
        return TargetWeightsColumnsNew(**output)

    @property
    @abstractmethod
    def inner_format(self) -> TargetWeightsColumnsNew:
        """ """

    def check_weights_postfix(
            self,
            weights_src_name: str,
            weights_postfix: Optional[str],
            client: str,
            breed: str,
            gender: str,
    ):
        """
        Return checked weights_postfix. If weights_postfix defined, then return weights_postfix,
        If weights_postfix is None, return ACTUAL postfix for specified weights_src_name and client
        Function return correspondent to weights_src_name weights postfix in case

        :param weights_src_name:
        :param weights_postfix:
        :param client:
        :return:
        """
        _weights_postfix = weights_postfix
        if _weights_postfix is None:
            _weights_postfix = self.actual_info_storage.get_actual_weights_postfix(
                weights_src_name, client=client, breed_type=breed, gender=gender
            )
            if _weights_postfix is None:
                e = colorstr(
                    "red",
                    f"ERROR! NO actual weights_postfix for {weights_src_name} {(client, breed, gender)}",
                )
                raise ActualPostfixError(e)
            print(
                f"Weights_postfix for {(client, breed, gender)} {weights_src_name} was set as "
                f"actual_target_weights_postfix '{_weights_postfix}'"
            )
        return _weights_postfix

    @staticmethod
    def check_if_duplicates(df: pd.DataFrame, subset: List[str]):
        """
        Check if there any duplicates in df

        :param subset:
        :param df:
        :return: True if there are some duplicated by subset, False - if no duplicates
        """
        duplicates = df.duplicated(subset=subset)
        return len(duplicates) != 0

    def convert_units(
            self,
            df: pd.DataFrame,
            age_column: str,
            weight_column: str,
            standard_weights_in_kg: Optional[pd.Series] = None,
    ) -> pd.DataFrame:
        if df.empty:
            print("WARNING convert_units -> input DF is empty ")
            return df

        if self.units == WEIGHTS_UNITS["kg"]:
            values_to_convert = df.set_index(age_column)[weight_column]
            df[weight_column] = convert_to_kg(
                values_to_convert, standard_weights_in_kg=standard_weights_in_kg
            ).values
        elif self.units == WEIGHTS_UNITS["g"]:
            df[weight_column] = convert_to_g(
                df.set_index(age_column)[weight_column],
                standard_weights_in_kg=standard_weights_in_kg,
            ).values

        return df

    @abstractmethod
    def convert_to_input_format(
            self, df: pd.DataFrame, src_format: TargetWeightsColumnsNew
    ) -> pd.DataFrame:
        """
        Convert df with correspondent src_format to input format
        Matches global data struct

        :param df: weights df
        :param src_format: Define columns structure of df
        :return:
        """

    @abstractmethod
    def get_target_weights(
            self,
            src_name: str,
            weights_postfix: Optional[str],
            filters: Filter,
            output_df_format: Optional[TargetWeightsColumnsNew] = None,
    ) -> pd.DataFrame:
        """
        Return all weights with output_df_format for specified src_name, weights postfix and filters

        :param src_name:
        :param weights_postfix:
        :param filters:
        :param output_df_format:
        :return:
        """

    @abstractmethod
    def update_target_weights(
            self,
            weights_df: pd.DataFrame,
            input_df_format: TargetWeightsColumnsNew,
            **kwargs,
    ):
        """
        Update all info from weights_df

        :param weights_df:
        :param input_df_format:
        :return:
        """

    @abstractmethod
    def delete_target_weights(
            self, src_name: str, weights_postfix: str, filters: Filter, **kwargs
    ) -> int:
        """
        Delete all weights of specified  src_name, weights_postfix, filters.

        .. warning::
            Deleting is performed for the whole house, that matches filters

        :param src_name:
        :param weights_postfix:
        :param filters:
        :return: count of deleted rows
        """

    @staticmethod
    def match_weights(
            df: pd.DataFrame,
            weights_df: pd.DataFrame,
            age_column: str,
            weight_column: str,
            match_columns: List[str],
    ):
        """
        :param df:
        :param weights_df:
        :param age_column:
        :param weight_column:
        :param match_columns: house_index + Optional[age]
        :return:
        """

        weights_df_columns = list(
            {age_column, weight_column}
            .union(match_columns)
            .intersection(weights_df.columns)
        )
        if weight_column in df.columns:
            tmp_df = df.drop(columns=[weight_column])
        else:
            tmp_df = df
        df_output = pd.merge(
            tmp_df,
            weights_df[weights_df_columns],
            on=match_columns,
            suffixes=("_old_data", ""),
            how="left",
        )
        df_output = df_output[[c for c in df_output if not c.endswith("_old_data")]]
        return df_output
