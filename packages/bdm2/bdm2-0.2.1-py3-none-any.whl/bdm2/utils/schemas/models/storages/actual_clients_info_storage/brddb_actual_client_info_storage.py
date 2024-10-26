import copy
import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from brddb.utils.common import colorstr

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct

from brddb.models.postgres import ActualClientsInfoTable

from bdm2.utils.schemas.models.storages.actual_clients_info_storage import ActualClientsInfoColumns
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.actual_clients_info_storage import \
    ActualClientsInfoStorage

from bdm2.utils.schemas.models.storages.brddbapi_client.brddb_client import brddb_client


@dataclass
class BrdDBInputActualClientsInfoColumns(ColumnsStruct):
    """
    Postgres actual client info columns. Contains mostly ids.

    ActualClientsInfoColumns can be converted to PostgresInputActualClientsInfoColumns in
    BrdDBActualClientsInfoStorage.update()

    """

    client_id: str = ActualClientsInfoTable.client_id.key
    breed_type_id: str = ActualClientsInfoTable.breed_type_id.key
    gender_id: str = ActualClientsInfoTable.gender_id.key
    engine_config_id: str = ActualClientsInfoTable.engine_config_id.key
    piwfha_weights_postfix_id: str = ActualClientsInfoTable.piwfha_weights_src_id.key
    target_weights_postfix_id: str = ActualClientsInfoTable.target_weights_src_id.key
    likely_weights_postfix_id: str = (
        ActualClientsInfoTable.likely_target_weights_src_id.key
    )

    # the same as in  ActualClientsInfoColumns
    standard_weights: str = ActualClientsInfoTable.standard_weights.key
    statistics: str = ActualClientsInfoTable.statistics.key

    @property
    def index_columns(self):
        return [self.client_id, self.breed_type_id, self.gender_id]


@dataclass
class BrdDBActualClientsInfoColumns(
    ActualClientsInfoColumns,
    BrdDBInputActualClientsInfoColumns,
):

    def __post_init__(self):
        self.engine_config_name = "engine"
        self.results_postfix = "results_postfix"
        self.target_weights_postfix = "target_weights_postfix"
        self.piwfha_weights_postfix = "PIWFHA_weights_postfix"
        self.likely_weights_postfix = "likely_weights_postfix"


class BrdDBActualClientsInfoStorage(ActualClientsInfoStorage):
    def __init__(
            self,
            logger: logging.Logger = logging.getLogger("pipeline_runner"),
    ):

        ActualClientsInfoStorage.__init__(self)
        self.logger = logger
        self._inner_format = BrdDBActualClientsInfoColumns()
        self.filter: Filter = Filter()
        self.actual_info = self.get(self.filter, output_format=self._inner_format)

        self.age_column = "age"
        self.standard_required_columns = [self.age_column, "Weights"]
        self.statistics_required_columns = [self.age_column]

    def update_actual_info(self):
        self.get(self.filter, output_format=self._inner_format)

    @property
    def inner_format(self) -> BrdDBActualClientsInfoColumns:
        return BrdDBActualClientsInfoColumns(
            **copy.deepcopy(self._inner_format.__dict__)
        )

    def get_actual_target_weights_postfix(
            self,
            client: str,
            breed_type: str,
            gender: str,
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> Optional[str]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group(
                (client, breed_type, gender),
            )
            assert len(g[self._inner_format.target_weights_postfix].unique()) == 1
            return g[self._inner_format.target_weights_postfix].iloc[0]
        except Exception as e:
            self.logger.warning(
                colorstr(
                    "red",
                    f'WARNING! No actual_target_weights for {(client, breed_type, gender)}"\n{e}',
                ),
            )
        return None

    def get_actual_piwfha_weights_postfix(
            self,
            client: str,
            breed_type: Optional[str],
            gender: Optional[str],
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> Optional[str]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group(
                (client, breed_type, gender),
            )
            assert len(g[self._inner_format.piwfha_weights_postfix].unique()) == 1
            return g[self._inner_format.piwfha_weights_postfix].iloc[0]
        except Exception as e:
            self.logger.warning(
                colorstr(
                    "red",
                    f"WARNING! No piwfha_weights_postfix for {(client, breed_type, gender)}\n{e}",
                ),
            )
        return None

    def get_actual_engine(
            self,
            client: str,
            breed_type: str,
            gender: str,
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> (Optional[str], Optional[str]):
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group(
                (client, breed_type, gender),
            )
            assert len(g) == 1
            return (
                g[self._inner_format.engine_config_name].iloc[0],
                g[self._inner_format.results_postfix].iloc[0],
            )
        except Exception as e:
            self.logger.warning(
                colorstr(
                    "red",
                    f"WARNING! No get_actual_engine for {(client, breed_type, gender)}:\n{e}",
                ),
            )
        return None, None

    def get(
            self,
            filters: Filter= Filter(),
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> pd.DataFrame:
        if output_format is None:
            output_format = self.output_default_format
        output = brddb_client.get_for_postgres_aci_storage()
        output = self.convert_to_output_format(output, output_format=output_format)
        return output

    def get_default_statistics(self) -> Optional[pd.DataFrame]:
        return self.get_actual_statistics(*self.default_cl_br_g)

    def get_actual_statistics(
            self,
            client: str,
            breed_type: Optional[str],
            gender: Optional[str],
    ) -> Optional[pd.DataFrame]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(
                [
                    self._inner_format.client,
                    self._inner_format.breed_type,
                    self._inner_format.gender,
                ],
            ).get_group((client, breed_type, gender))
            assert len(g) == 1
            assert not pd.isnull(g[self._inner_format.statistics].iloc[0])
            standard = pd.read_json(g[self._inner_format.statistics].iloc[0])
            if "ExpID" in standard.columns:
                standard.rename(columns={"ExpID": self.age_column}, inplace=True)
            standard.set_index(self.age_column, inplace=True)
            return standard
        except Exception as e:
            self.logger.exception(
                colorstr(
                    "red",
                    f"WARNING! No actual_statistics for {client} {breed_type} {gender}\n{e}",
                ),
            )
        return None

    def get_default_weights_standard(self) -> Optional[pd.DataFrame]:
        return self.get_actual_weights_standard(*self.default_cl_br_g)

    def get_actual_weights_standard(
            self,
            client: str,
            breed_type: Optional[str],
            gender: Optional[str],
    ) -> Optional[pd.DataFrame]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(
                [
                    self._inner_format.client,
                    self._inner_format.breed_type,
                    self._inner_format.gender,
                ],
            ).get_group((client, breed_type, gender))
            assert len(g) == 1
            assert not pd.isnull(g[self._inner_format.standard_weights].iloc[0])
            standard = pd.read_json(
                g[self._inner_format.standard_weights].iloc[0],
            ).set_index("age")
            return standard
        except Exception as e:
            self.logger.warning(
                colorstr(
                    "red",
                    f"WARNING! No actual_weights_standard for {client}\n{e}",
                ),
            )
        return None

    def delete(self, filters: Filter):
        """
        Delete info from storage

        :param filters: filter for specifying house scope
        """
        raise NotImplementedError

    def get_id_by_name(self, name: str, entity):
        raise NotImplementedError

    def update_weights_src(self, src_type_name: str, weights_postfix: str):
        raise NotImplementedError

    def update(self, df: pd.DataFrame, src_format: ActualClientsInfoColumns):
        """
        Redefine all necessary ids (client_id,breed_type_id,gender_id,engine_config_id,
        target_weights_src_id, piwfha_weights_src_id) und upsert data to database

        :param df: actual clients' info data to be updated, has to have src_format columns
        :param src_format: column's names to be used fir updating
        :return: None
        """
        raise NotImplementedError
