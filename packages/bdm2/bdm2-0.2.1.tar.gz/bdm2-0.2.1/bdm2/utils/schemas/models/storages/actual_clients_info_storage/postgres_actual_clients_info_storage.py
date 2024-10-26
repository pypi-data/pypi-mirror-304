#  Copyright (c) Anna Sosnovskaya

"""
Postgres Storage of actual clients' info.


"""

import copy
import datetime
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from brddb.models.postgres import (
    ActualClientsInfoTable,
    Clients,
    BreedTypes,
    Genders,
    EngineConfigs,
    Engines,
)
from brddb.utils.common import colorstr
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, aliased

from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.get_and_add_methods import add_filters
from bdm2.utils.schemas.components.sqlhelpers.helpers import (
    compile_query,
    upsert_entity,
)
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.storages.actual_clients_info_storage import (
    ActualClientsInfoColumns,
)
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.actual_clients_info_storage import (
    ActualClientsInfoStorage,
)
from bdm2.utils.schemas.models.storages.house_performance_storage import (
    WeightSources,
    WeightSourceTypes,
)
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import (
    WrongWeightsSourceType,
    WEIGHTS_SRC_TYPE,
)


@dataclass
class PostgresInputActualClientsInfoColumns(ColumnsStruct):
    """
    Postgres actual client info columns. Contains mostly ids.

    ActualClientsInfoColumns can be converted to PostgresInputActualClientsInfoColumns in
    PostgresActualClientsInfoStorage.update()

    """

    client_id: str = ActualClientsInfoTable.client_id.key
    breed_type_id: str = ActualClientsInfoTable.breed_type_id.key
    gender_id: str = ActualClientsInfoTable.gender_id.key
    engine_config_id: str = ActualClientsInfoTable.engine_config_id.key
    piwfha_weights_postfix_id: str = ActualClientsInfoTable.piwfha_weights_src_id.key
    target_weights_postfix_id: str = ActualClientsInfoTable.target_weights_src_id.key
    likely_weights_postfix_id: str = ActualClientsInfoTable.likely_target_weights_src_id.key

    # the same as in  ActualClientsInfoColumns
    standard_weights: str = ActualClientsInfoTable.standard_weights.key
    statistics: str = ActualClientsInfoTable.statistics.key

    @property
    def index_columns(self):
        return [self.client_id, self.breed_type_id, self.gender_id]


@dataclass
class PostgresActualClientsInfoColumns(ActualClientsInfoColumns, PostgresInputActualClientsInfoColumns):
    """
    Postgres 'get' actual client info columns (specified for Postgres storage).

    Contains as ActualClientsInfoColumns, so PostgresInputActualClientsInfoColumns

    """

    def __post_init__(self):
        self.engine_config_name = "engine"
        self.results_postfix = "results_postfix"
        self.target_weights_postfix = "target_weights_postfix"
        self.piwfha_weights_postfix = "PIWFHA_weights_postfix"
        self.likely_weights_postfix = "likely_weights_postfix"


class PostgresActualClientsInfoStorage(ActualClientsInfoStorage):
    """
    Actual clients' info storage in postgres

    """

    def __init__(self):

        ActualClientsInfoStorage.__init__(self)
        self.session = sessionmaker(bind=postgres_engine)()
        self._inner_format = PostgresActualClientsInfoColumns()
        self.last_update = datetime.datetime.now()
        self.actual_info = self.get(Filter(), output_format=self._inner_format)
        self.update_period = 60  # minutes

        self.age_column = "age"  # used for standard loading
        self.standard_required_columns = [self.age_column, "Weights"]
        self.statistics_required_columns = [self.age_column]
        self.logger = build_logger(Path(__file__), save_log=False)

    def update_actual_info(self):

        now = datetime.datetime.now()
        if (now - self.last_update).total_seconds() / 60 > self.update_period:
            self.actual_info = self.get(Filter(), output_format=self._inner_format)
            self.last_update = datetime.datetime.now()
            self.logger.info(colorstr("blue", "PostgresActualClientsInfoStorage was updated"))

    @property
    def inner_format(self) -> ActualClientsInfoColumns:
        return PostgresActualClientsInfoColumns(**copy.deepcopy(self._inner_format.__dict__))

    def get_actual_target_weights_postfix(
        self,
        client: str,
        breed_type: Optional[str],
        gender: Optional[str],
        output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> Optional[str]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group((client, breed_type, gender))
            assert len(g[self._inner_format.target_weights_postfix].unique()) == 1
            return g[self._inner_format.target_weights_postfix].iloc[0]
        except Exception as e:
            self.logger.info(
                colorstr(
                    "red",
                    f'WARNING! No actual_target_weights for {(client, breed_type, gender)}"\n{e}',
                )
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
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group((client, breed_type, gender))
            assert len(g[self._inner_format.piwfha_weights_postfix].unique()) == 1
            return g[self._inner_format.piwfha_weights_postfix].iloc[0]
        except Exception as e:
            self.logger.info(
                colorstr(
                    "red",
                    f"WARNING! No piwfha_weights_postfix for {(client, breed_type, gender)}\n{e}",
                )
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
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group((client, breed_type, gender))
            assert len(g) == 1
            return (
                g[self._inner_format.engine_config_name].iloc[0],
                g[self._inner_format.results_postfix].iloc[0],
            )
        except Exception as e:
            self.logger.info(
                colorstr(
                    "red",
                    f"WARNING! No get_actual_engine for {(client, breed_type, gender)}:\n{e}",
                )
            )
        return None, None

    def get(self, filters: Filter, output_format: Optional[ActualClientsInfoColumns] = None) -> pd.DataFrame:

        if output_format is None:
            output_format = self.output_default_format

        TargetsWeightSources = aliased(WeightSources)
        PiwfhaWeightSources = aliased(WeightSources)
        LikelyWeightSources = aliased(WeightSources)

        query = (
            self.session.query(
                ActualClientsInfoTable.client_id.label(self._inner_format.client_id),
                Clients.name.label(self._inner_format.client),
                BreedTypes.id.label(self._inner_format.breed_type_id),
                BreedTypes.name.label(self._inner_format.breed_type),
                Genders.id.label(self._inner_format.gender_id),
                Genders.name.label(self._inner_format.gender),
                EngineConfigs.id.label(self._inner_format.engine_config_id),
                EngineConfigs.name.label(self._inner_format.engine_config_name),
                EngineConfigs.results_postfix.label(self._inner_format.results_postfix),
                TargetsWeightSources.id.label(self._inner_format.target_weights_postfix_id),
                TargetsWeightSources.postfix.label(self._inner_format.target_weights_postfix),
                PiwfhaWeightSources.id.label(self._inner_format.piwfha_weights_postfix_id),
                PiwfhaWeightSources.postfix.label(self._inner_format.piwfha_weights_postfix),
                LikelyWeightSources.id.label(self._inner_format.likely_weights_postfix_id),
                LikelyWeightSources.postfix.label(self._inner_format.likely_weights_postfix),
                ActualClientsInfoTable.standard_weights.label(self._inner_format.standard_weights),
                ActualClientsInfoTable.statistics.label(self._inner_format.statistics),
            )
            .join(Clients, ActualClientsInfoTable.client_id == Clients.id)
            .join(BreedTypes, ActualClientsInfoTable.breed_type_id == BreedTypes.id)
            .join(Genders, ActualClientsInfoTable.gender_id == Genders.id)
            .join(
                EngineConfigs,
                ActualClientsInfoTable.engine_config_id == EngineConfigs.id,
                isouter=True,
            )
            .join(
                TargetsWeightSources,
                ActualClientsInfoTable.target_weights_src_id == TargetsWeightSources.id,
                isouter=True,
            )
            .join(
                PiwfhaWeightSources,
                ActualClientsInfoTable.piwfha_weights_src_id == PiwfhaWeightSources.id,
                isouter=True,
            )
            .join(
                LikelyWeightSources,
                ActualClientsInfoTable.likely_target_weights_src_id == LikelyWeightSources.id,
                isouter=True,
            )
        )

        query = add_filters(query, filters=filters)
        max_retries = 3
        retry_delay = 5  # seconds
        print("here")
        for attempt in range(max_retries):
            try:
                with postgres_engine.connect().execution_options(timeout=10) as connection:
                    result = connection.execute(query.statement)
                    rows = [row for row in result.mappings()]
                    output = pd.DataFrame(rows)
                break
            except OperationalError as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Attempt {attempt + 1} failed: {e}. No more retries left.")
                    raise
        if output_format is not None:
            output = self.convert_to_output_format(output, output_format=output_format)

        return output

    def get_default_statistics(self) -> Optional[pd.DataFrame]:
        return self.get_actual_statistics(*self.default_cl_br_g)

    def get_actual_statistics(self, client: str, breed_type: Optional[str], gender: Optional[str]) -> Optional[pd.DataFrame]:

        self.update_actual_info()
        try:
            g = self.actual_info.groupby(
                [
                    self._inner_format.client,
                    self._inner_format.breed_type,
                    self._inner_format.gender,
                ]
            ).get_group((client, breed_type, gender))
            assert len(g) == 1
            assert not pd.isnull(g[self._inner_format.statistics].iloc[0])
            standard = pd.read_json(g[self._inner_format.statistics].iloc[0])
            if "ExpID" in standard.columns:
                standard.rename(columns={"ExpID": self.age_column}, inplace=True)
            standard.set_index(self.age_column, inplace=True)
            return standard
        except Exception as e:
            self.logger.info(
                colorstr(
                    "red",
                    f"WARNING! No actual_statistics for {client} {breed_type} {gender}\n{e}",
                )
            )
        return None

    def get_default_weights_standard(self) -> Optional[pd.DataFrame]:
        return self.get_actual_weights_standard(*self.default_cl_br_g)

    def get_actual_weights_standard(self, client: str, breed_type: Optional[str], gender: Optional[str]) -> Optional[pd.DataFrame]:

        self.update_actual_info()
        try:
            g = self.actual_info.groupby(
                [
                    self._inner_format.client,
                    self._inner_format.breed_type,
                    self._inner_format.gender,
                ]
            ).get_group((client, breed_type, gender))
            assert len(g) == 1
            assert not pd.isnull(g[self._inner_format.standard_weights].iloc[0])
            standard = pd.read_json(g[self._inner_format.standard_weights].iloc[0]).set_index("age")
            return standard
        except Exception as e:
            self.logger.info(colorstr("red", f"WARNING! No actual_weights_standard for {client}\n{e}"))
        return None

    def delete(self, filters: Filter):
        """
        TODO: Delete info from storage

        :param filters: filter for specifying house scope
        """
        pass

    def get_id_by_name(self, name: str, entity):
        rows = self.session.execute(self.session.query(entity).where(entity.name == name)).scalars().all()
        if len(rows) == 0:
            raise ValueError(colorstr("red" f"{name} NOT FOUND in {entity.__tablename__} table"))
        return rows[0].id

    def update_weights_src(self, src_type_name: str, weights_postfix: str):
        try:
            src_type_id = self.get_id_by_name(src_type_name, WeightSourceTypes)
        except Exception as e:
            raise WrongWeightsSourceType(f"Could not find {src_type_name} in Postgres")

        entity = WeightSources(source_type_id=src_type_id, postfix=weights_postfix)
        upsert_id = upsert_entity(self.session, entity)
        return upsert_id

    def update(self, df: pd.DataFrame, src_format: ActualClientsInfoColumns):
        """
        Redefine all necessary ids (client_id,breed_type_id,gender_id,engine_config_id,
        target_weights_src_id, piwfha_weights_src_id) und upsert data to database

        :param df: actual clients' info data to be updated, has to have src_format columns
        :param src_format: column's names to be used fir updating
        :return: None
        """

        for _, row in df.iterrows():

            # TO DANGEROUS MODE
            # update has two modes:
            #     1. If isinstance(src_format, PostgresInputActualClientsInfoColumns), will update df fully
            #        (with all id columns not to be changed)
            #
            #     .. warning:
            #         Changing only ActualClientsInfoColumns in df with PostgresInputActualClientsInfoColumns format,
            #         can lead to mismatches, as ids will be used for old
            #
            # if isinstance(src_format, PostgresInputActualClientsInfoColumns):
            #
            #     try:
            #         entity_dict = {}
            #         for c in src_format.get_columns():
            #             if c in PostgresInputActualClientsInfoColumns.__dict__.values():
            #                 entity_dict[c] = row[c]
            #         entity = ActualClientsInfoTable(**entity_dict)
            #         upsert_entity(self.session, entity, update_on_conflict=True, update_nones=True)
            #         self.session.commit()
            #         self.logger.info(colorstr('blue',
            #                        f"{tuple(row[src_format.index_columns])} entity was updated with ids FROM INPUT DF"))
            #     except Exception as e:
            #         self.logger.info(colorstr('red', f"{tuple(row[src_format.index_columns])}: {e}"))

            try:
                entity = ActualClientsInfoTable()
                entity.client_id = self.get_id_by_name(row[src_format.client], Clients)

                entity.breed_type_id = self.get_id_by_name(row[src_format.breed_type], BreedTypes)
                entity.gender_id = self.get_id_by_name(row[src_format.gender], Genders)

                try:
                    if not pd.isnull(src_format.engine_config_name):
                        engine_v = row[src_format.engine_config_name].split("_")[1][1:]
                        engine_id = self.get_id_by_name(engine_v, Engines)
                        engine_entity = EngineConfigs(
                            engine_id=engine_id,
                            name=row[src_format.engine_config_name],
                            results_postfix=row[src_format.results_postfix],
                        )
                        #
                        #
                        this_engine = row[src_format.engine_config_name]
                        engine_config = self.session.query(EngineConfigs).filter(EngineConfigs.name == this_engine).first()

                        q = (
                            self.session.query(ActualClientsInfoTable)
                            .join(Clients, Clients.id == ActualClientsInfoTable.client_id)
                            .join(Genders, Genders.id == ActualClientsInfoTable.gender_id)
                            .join(
                                BreedTypes,
                                BreedTypes.id == ActualClientsInfoTable.breed_type_id,
                            )
                            .filter(Clients.name == row[src_format.client])
                            .filter(Genders.name == row[src_format.gender])
                            .filter(BreedTypes.name == row[src_format.breed_type])
                        )
                        act_info = self.session.execute(q).scalars().first()
                        entity.engine_config_id = upsert_entity(self.session, engine_entity, update_on_conflict=True)

                        # statistics = pd.read_json(row['standard_weights'])  #pd.read_json(row['standard_weights'])
                        # statistics.to_excel(r'C:\Users\pawlin\Downloads\statistics.xlsx', index= False)
                        # self.session.commit()

                # update_files
                except Exception as e:
                    self.logger.info(e)

                if not pd.isnull(row[src_format.target_weights_postfix]):
                    entity.target_weights_src_id = self.update_weights_src(
                        WEIGHTS_SRC_TYPE["Targets"],
                        row[src_format.target_weights_postfix],
                    )

                if not pd.isnull(row[src_format.piwfha_weights_postfix]):
                    entity.piwfha_weights_src_id = self.update_weights_src(
                        WEIGHTS_SRC_TYPE["PIWFHA"],
                        row[src_format.piwfha_weights_postfix],
                    )
                # check statistics
                if not pd.isnull(row[src_format.statistics]):
                    statistics = pd.read_json(row[src_format.statistics])
                    if statistics is not None:
                        if all([c in statistics.columns for c in self.statistics_required_columns]):
                            entity.statistics = row[src_format.statistics]
                        else:
                            warnings.warn(
                                f"Statistics has wrong format. Not all required columns ({self.statistics_required_columns})are in statistics"
                            )
                    else:
                        entity.statistics = statistics

                # check standard
                if not pd.isnull(row[src_format.standard_weights]):
                    standard_weights = pd.read_json(row[src_format.standard_weights])
                    if standard_weights is not None:
                        if all([c in standard_weights.columns for c in self.standard_required_columns]):
                            entity.standard_weights = row[src_format.standard_weights]
                        else:
                            warnings.warn(
                                f"Standard has wrong format. "
                                f"Not all required columns ({self.standard_required_columns})are in statistics"
                            )
                    else:
                        entity.standard_weights = standard_weights

                # UPSERT
                upsert_entity(self.session, entity, update_on_conflict=True, update_nones=True)
                self.session.commit()
                self.logger.info(
                    colorstr(
                        "blue",
                        f"{tuple(row[src_format.index_columns])} entity was updated",
                    )
                )
            except Exception as e:
                self.logger.info(colorstr("red", f"{tuple(row[src_format.index_columns])}: {e}"))
