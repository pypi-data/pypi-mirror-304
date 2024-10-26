#  Copyright (c) Anna Sosnovskaya

"""
Storage of actual clients' info.

Right now actual information is grouped by client, breed_type, gender.
So It means, that unique components are specified for each client, breed, gender devices group.
Engines are also mostly prepared for specified client, breed, gender group

For each client, breed_type, gender specified next actual features:

    * actual **engine_config** - release engine version with components
    * actual **results_postfix** - results obtained with actual engine_config
    * actual **target weights postfix**  - group of validated target weights
    * actual **statistics** - statistics (mean, std, etc.) by features
    * actual **standard weights** - statistics (mean, std, etc.) by target weights

"""

from abc import abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import (
    ColumnsStruct,
)
from bdm2.utils.schemas.models.data_structures.device_data_struct import (
    ClientBreedGenderColumns,
)
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import StorageBase
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import (
    WEIGHTS_SRC_TYPE,
    WrongWeightsSourceType,
)


@dataclass
class Combination:
    """
    struct for combination initialization
    """

    client: str
    breed_type: str
    gender: str

    def __str__(self):
        return f"{self.client} {self.breed_type} {self.gender}"


@dataclass
class CombinationColumns(ColumnsStruct):
    """
    Struct for columns names in df that are responsible for client breed gender
    """

    client: str
    breed_type: str
    gender: str


@dataclass
class ActualClientsInfoColumns(ColumnsStruct):
    """
    Struct for storing data format of ActualClientsInfoStorage.

    Main columns (can be used as index):
        :client: client name
        :breed_type: breed_type name
        :gender: gender name

    Actual info columns :
        :engine_config_name: engine postfix. used in :ref:`MainConfig<main_config.MainConfig>`
        :results_postfix: breed_type name
        :target_weights_postfix: gender name
        :piwfha_weights_postfix: gender name

    .. note::
        DOC, Farmers, SLT do not have actual postfix, as do not have postfixes at all. It is raw data

    Actual data columns :
        :statistics: statistics values in json format
        :standard_weights: standard_weights values in json format

    """

    # Clients' Hierarchy
    client: str = field(default="client", init=True)
    breed_type: str = field(default="breed_type", init=True)
    gender: str = field(default="gender", init=True)

    engine_config_name: str = field(default="engine_config_name", init=True)
    results_postfix: str = field(default="results_postfix", init=True)
    target_weights_postfix: str = field(default="target_weights_postfix", init=True)
    piwfha_weights_postfix: str = field(default="piwfha_weights_postfix", init=True)
    likely_weights_postfix: str = field(default="likely_weights_postfix", init=True)

    statistics: str = field(default="statistics", init=True)
    standard_weights: str = field(default="standard_weights", init=True)

    @property
    def index_columns(self):
        return [self.client, self.breed_type, self.gender]

    @property
    def cl_br_g_columns(self) -> ClientBreedGenderColumns:
        return ClientBreedGenderColumns(
            client=self.client, breed_type=self.breed_type, gender=self.gender
        )

    @property
    def combination_columns(self) -> CombinationColumns:
        return CombinationColumns(
            client=self.client, breed_type=self.breed_type, gender=self.gender
        )


class ActualClientsInfoStorage(StorageBase):
    def __init__(self):
        self.default_cl_br_g = ("DEFAULT", "BreedType", "Gender")

    @property
    def output_default_format(self) -> ActualClientsInfoColumns:
        """
        return default ActualClientsInfo format

        :return:
        """
        return ActualClientsInfoColumns()

    @property
    def inner_as_default_format(self) -> ActualClientsInfoColumns:
        output = {}
        loc_inner_format = self.inner_format
        for atr in ActualClientsInfoColumns.__annotations__:
            output[atr] = loc_inner_format.__dict__[atr]
        return ActualClientsInfoColumns(**output)

    @property
    @abstractmethod
    def inner_format(self) -> ActualClientsInfoColumns:
        """
        return INNER  format

        :return:
        """

    def get_actual_weights_postfix(
            self,
            weights_src_name: str,
            client: str,
            breed_type: Optional[str] = None,
            gender: Optional[str] = None,
            logger=build_logger(Path(__file__), save_log=False)) -> Optional[str]:
        """
        Return ACTUAL weights_postfix for specifies weights_src_name and client.

            * DOC, Farmers, SLT do not have actual postfix. weights_postfix = ""
            * PIWFHA, Manuals, Targets, Likely, Likely_targets actual postfix is from storage of actual postfixes

        :param weights_src_name:
        :param client: client name
        :param breed_type: not used now, actual weights postfixes are unique by client now
        :param gender: not used now, actual weights postfixes are unique by client now
        :return: if found, weights postfix (str), Else None

        :raises WrongWeightsSourceType: if weights_src_name not in WEIGHTS_SRC_TYPE
        """

        if weights_src_name not in WEIGHTS_SRC_TYPE.values():
            raise WrongWeightsSourceType(
                f"get_actual_weights_postfix: {weights_src_name} is not available"
            )

        if weights_src_name == WEIGHTS_SRC_TYPE["Mahender"]:
            logger.info(
                "red",
                "WARNING! Mahender weights are deprecated, Farmers will be used instead",
            )
            weights_src_name = WEIGHTS_SRC_TYPE["Farmers"]

        # DOC, SLT, Farmers do not have weights postfix (as always raw information)
        if weights_src_name in [
            WEIGHTS_SRC_TYPE["DOC"],
            WEIGHTS_SRC_TYPE["Farmers"],
            WEIGHTS_SRC_TYPE["SLT"],
        ]:
            weights_postfix = ""
            return weights_postfix

        elif weights_src_name == WEIGHTS_SRC_TYPE["PIWFHA"]:
            weights_postfix = self.get_actual_piwfha_weights_postfix(
                client=client, breed_type=breed_type, gender=gender
            )
            return None if pd.isnull(weights_postfix) else weights_postfix

        elif weights_src_name in [
            WEIGHTS_SRC_TYPE["Manuals"],  # old
            WEIGHTS_SRC_TYPE["Targets"],  # new
            WEIGHTS_SRC_TYPE["Likely"],  # old
            WEIGHTS_SRC_TYPE["Likely_targets"],  # new
        ]:

            weights_postfix = self.get_actual_target_weights_postfix(
                client=client, breed_type=breed_type, gender=gender
            )
            return None if pd.isnull(weights_postfix) else weights_postfix

        else:
            raise WrongWeightsSourceType(
                f"get_actual_weights_postfix: {weights_src_name} is not available"
            )

    @abstractmethod
    def get_actual_target_weights_postfix(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[str]:
        """
        Return target postfix (str) for specified client, breed_type, gender.
        Can be used to obtain Targets and Likely_targets weights
        If not found - return None

        :param client:
        :param breed_type:
        :param gender:
        :return:
        """

    @abstractmethod
    def get_actual_piwfha_weights_postfix(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[str]:
        """
        Return PIWFHA postfix (str) for specified client, breed_type, gender.
        Can be used to obtain PIWFHA weights
        If not found - return None

        :param client:
        :param breed_type:
        :param gender:
        :return:
        """

    @abstractmethod
    def get_actual_engine(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> (Optional[str], Optional[str]):
        """
        Return actual_engine name and actual results postfix for specified client, breed_type, gender
        If not found - return None, None

        :param client:
        :param breed_type:
        :param gender:
        :return: engine_postfix, results_postfix
        """

    @abstractmethod
    def get_actual_statistics(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[pd.DataFrame]:
        """
        Return statistics for specified client, breed_type, gender as df (with age as index and features column)
        If not found - return None

        :param client:
        :param breed_type:
        :param gender:
        :return:
        """

    @abstractmethod
    def get_default_statistics(self) -> Optional[pd.DataFrame]:
        """
        Return statistics for specified client, breed_type, gender as df (with age as index and features column)
        If not found - return None

        client:
        breed_type:
        gender:
        :return:
        """

    @abstractmethod
    def get_default_weights_standard(self) -> Optional[pd.DataFrame]:
        """
        Return default standard weights as df (with age as index and Weights column)
        If not found - return None

        client:
        breed_type:
        gender:
        :return:
        """

    @abstractmethod
    def get_actual_weights_standard(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[pd.DataFrame]:
        """
        Return standard weights for specified client, breed_type, gender as df (with age as index and Weights column)
        If not found - return None

        :param client:
        :param breed_type:
        :param gender:
        :return:
        """

    @abstractmethod
    def get(
            self, filters: Filter, output_format: Optional[ActualClientsInfoColumns] = None
    ) -> pd.DataFrame:
        """
        return full df of actual clients' info, that matches filter

        :param filters: filter for specifying devices scope
        :param output_format: column names of output data
        :return: actual client's info df
        """

    @abstractmethod
    def delete(self, filters: Filter):
        """
        Delete info from storage

        :param filters: filter for specifying house scope
        """

    @abstractmethod
    def update(self, df: pd.DataFrame, src_format: ActualClientsInfoColumns):
        """
        Update actual clients' info in storage.

        :param df: actual clients' info data to be updated, has to have src_format columns
        :param src_format: column's names to be used fir updating
        :return: None
        """
