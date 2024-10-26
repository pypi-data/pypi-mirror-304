import copy
import datetime
import time
import warnings
from abc import abstractmethod, ABC
from typing import Optional, Dict

import pandas as pd
from brddb.models.postgres import (
    WeightSources,
    ActualClientsInfoTable,
    Clients,
    BreedTypes,
    Genders,
    EngineConfigs,
    WeightSourceTypes,
    Engines,
)
from loguru import logger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, aliased

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.columns import (
    ColumnsStruct,
    ActualClientsInfoColumns,
    PostgresActualClientsInfoColumns,
)
from bdm2.utils.schemas.components.get_and_add_methods import add_filters
from bdm2.utils.schemas.components.sqlhelpers.helpers import (
    compile_query,
    upsert_entity,
)
from bdm2.utils.schemas.connection import postgres_engine


def get_rename_dict(src: ColumnsStruct, target: ColumnsStruct) -> Dict[str, str]:
    """
    Generate rename dict for 2 instances of the same ColumnsStruct objects
    .. note::
        utils type can be a child on target type

    :param src:
    :param target:
    :return:
    """

    assert isinstance(src, type(target)) or isinstance(target, type(src)), ValueError(
        f"from_columns and from_columns has to have the same baser class"
    )

    rename_dict = {}
    attributes_1 = src.__dict__
    attributes_2 = target.__dict__
    for attr in attributes_1:
        if attr in attributes_2:
            if isinstance(attributes_1[attr], str):
                rename_dict[attributes_1[attr]] = attributes_2[attr]
            elif isinstance(attributes_1[attr], ColumnsStruct):
                rename_dict.update(
                    get_rename_dict(attributes_1[attr], attributes_2[attr])
                )
            else:
                logger.info(
                    f"!! Warning !! Wrong format for attribute {attr}. Could be only str or ColumnsStruct"
                )

    return rename_dict


class StorageBase(ABC):
    """
    Storage base class
    """

    @staticmethod
    def check_format(df: pd.DataFrame, format: ColumnsStruct) -> bool:
        """"""
        absent_columns = list(set(format.get_columns()).difference(df.columns))
        return len(absent_columns) == 0

    @property
    @abstractmethod
    def output_default_format(self) -> ColumnsStruct:
        """
        Return default union format.
        So if we have one abstract class for some Storage, that have ColumnsStruct interface,
        all children of this class should be able to return parent ColumnsStruct interface with this function

        :return:
        """

    @property
    @abstractmethod
    def inner_format(self) -> ColumnsStruct:
        """
        return INNER  format

        :return:
        """

    @staticmethod
    def convert_formats(
            df: pd.DataFrame,
            input_format: ColumnsStruct,
            output_format: ColumnsStruct,
            save_extra_columns: bool = False,
    ):
        if save_extra_columns:
            df_full = pd.DataFrame(columns=df.columns)
        else:
            df_full = pd.DataFrame(columns=input_format.get_columns())
        columns = list(set(df.columns).intersection(df_full.columns))
        df_full[columns] = df[columns].copy(deep=True)

        rename_dict = get_rename_dict(input_format, output_format)
        df_full = df_full.rename(columns=rename_dict)

        df_output = pd.DataFrame(columns=output_format.get_columns())
        df_output[df_full.columns] = df_full.copy(deep=True)
        df_output = output_format.convert_df_types(df_output)
        return df_output

    def convert_to_output_format(
            self, df: pd.DataFrame, output_format: ColumnsStruct
    ) -> pd.DataFrame:
        """
        Convert df with input format to target format

        :param df: raw weights df from storage
        :param output_format: Define columns structure of output df
        :return:
        """
        # logger.info(colorstr('black', f'Converting df to output_format table format'))
        loc_inner_format = self.inner_format
        df_converted = self.convert_formats(
            df, input_format=loc_inner_format, output_format=output_format
        )

        return df_converted[output_format.get_columns()]


class WrongWeightsSourceType(Exception):
    """
    Occurred when weight source type is not available (not in WEIGHTS_SRC_TYPE.values)

    """

    pass


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
    ) -> Optional[str]:
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

        """

    @abstractmethod
    def get_default_weights_standard(self) -> Optional[pd.DataFrame]:
        """
        Return default standard weights as df (with age as index and Weights column)
        If not found - return None

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

    def update_actual_info(self):
        now = datetime.datetime.now()
        if (now - self.last_update).total_seconds() / 60 > self.update_period:
            self.actual_info = self.get(Filter(), output_format=self._inner_format)
            self.last_update = datetime.datetime.now()

            logger.info("blue", "PostgresActualClientsInfoStorage was updated")

    @property
    def inner_format(self) -> ActualClientsInfoColumns:
        return PostgresActualClientsInfoColumns(
            **copy.deepcopy(self._inner_format.__dict__)
        )

    def get_actual_target_weights_postfix(
            self,
            client: str,
            breed_type: Optional[str],
            gender: Optional[str],
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> Optional[str]:
        self.update_actual_info()
        try:
            g = self.actual_info.groupby(self._inner_format.index_columns).get_group(
                (client, breed_type, gender)
            )
            assert len(g[self._inner_format.target_weights_postfix].unique()) == 1
            return g[self._inner_format.target_weights_postfix].iloc[0]
        except Exception as e:
            logger.info(
                f'WARNING! No actual_target_weights for {(client, breed_type, gender)}"\n{e}'
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
                (client, breed_type, gender)
            )
            assert len(g[self._inner_format.piwfha_weights_postfix].unique()) == 1
            return g[self._inner_format.piwfha_weights_postfix].iloc[0]
        except Exception as e:
            logger.info(
                f"WARNING! No piwfha_weights_postfix for {(client, breed_type, gender)}\n{e}"
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
                (client, breed_type, gender)
            )
            assert len(g) == 1
            return (
                g[self._inner_format.engine_config_name].iloc[0],
                g[self._inner_format.results_postfix].iloc[0],
            )
        except Exception as e:
            logger.info(
                f"WARNING! No get_actual_engine for {(client, breed_type, gender)}:\n{e}"
            )
        return None, None

    def get(
            self,
            filters: Filter = Filter(),
            output_format: Optional[ActualClientsInfoColumns] = None,
    ) -> pd.DataFrame:

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
                TargetsWeightSources.id.label(
                    self._inner_format.target_weights_postfix_id
                ),
                TargetsWeightSources.postfix.label(
                    self._inner_format.target_weights_postfix
                ),
                PiwfhaWeightSources.id.label(
                    self._inner_format.piwfha_weights_postfix_id
                ),
                PiwfhaWeightSources.postfix.label(
                    self._inner_format.piwfha_weights_postfix
                ),
                LikelyWeightSources.id.label(
                    self._inner_format.likely_weights_postfix_id
                ),
                LikelyWeightSources.postfix.label(
                    self._inner_format.likely_weights_postfix
                ),
                ActualClientsInfoTable.standard_weights.label(
                    self._inner_format.standard_weights
                ),
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
                ActualClientsInfoTable.likely_target_weights_src_id
                == LikelyWeightSources.id,
                isouter=True,
            )
        )

        query = add_filters(query, filters=filters)
        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                with postgres_engine.connect() as connection:
                    output = pd.read_sql_query(compile_query(query), connection)
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

    def get_actual_statistics(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[pd.DataFrame]:
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
            logger.info(
                f"WARNING! No actual_statistics for {client} {breed_type} {gender}\n{e}"
            )
        return None

    def get_default_weights_standard(self) -> Optional[pd.DataFrame]:
        return self.get_actual_weights_standard(*self.default_cl_br_g)

    def get_actual_weights_standard(
            self, client: str, breed_type: Optional[str], gender: Optional[str]
    ) -> Optional[pd.DataFrame]:
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
            standard = pd.read_json(
                g[self._inner_format.standard_weights].iloc[0]
            ).set_index("age")
            return standard
        except Exception as e:
            logger.info(f"WARNING! No actual_weights_standard for {client}\n{e}")
        return None

    def delete(self, filters: Filter):
        """
        TODO: Delete info from storage

        :param filters: filter for specifying house scope
        """
        pass

    def get_id_by_name(self, name: str, entity):
        rows = (
            self.session.execute(self.session.query(entity).where(entity.name == name))
            .scalars()
            .all()
        )
        if len(rows) == 0:
            raise ValueError(f"{name} NOT FOUND in {entity.__tablename__} table")
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
            #         logger.info(colorstr('blue',
            #                        f"{tuple(row[src_format.index_columns])} entity was updated with ids FROM INPUT DF"))
            #     except Exception as e:
            #         logger.info(colorstr('red', f"{tuple(row[src_format.index_columns])}: {e}"))

            try:
                entity = ActualClientsInfoTable()
                entity.client_id = self.get_id_by_name(row[src_format.client], Clients)

                entity.breed_type_id = self.get_id_by_name(
                    row[src_format.breed_type], BreedTypes
                )
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
                        engine_config = (
                            self.session.query(EngineConfigs)
                            .filter(EngineConfigs.name == this_engine)
                            .first()
                        )

                        q = (
                            self.session.query(ActualClientsInfoTable)
                            .join(
                                Clients, Clients.id == ActualClientsInfoTable.client_id
                            )
                            .join(
                                Genders, Genders.id == ActualClientsInfoTable.gender_id
                            )
                            .join(
                                BreedTypes,
                                BreedTypes.id == ActualClientsInfoTable.breed_type_id,
                            )
                            .filter(Clients.name == row[src_format.client])
                            .filter(Genders.name == row[src_format.gender])
                            .filter(BreedTypes.name == row[src_format.breed_type])
                        )
                        act_info = self.session.execute(q).scalars().first()
                        entity.engine_config_id = upsert_entity(
                            self.session, engine_entity, update_on_conflict=True
                        )

                        # statistics = pd.read_json(row['standard_weights'])  #pd.read_json(row['standard_weights'])
                        # statistics.to_excel(r'C:\Users\pawlin\Downloads\statistics.xlsx', index= False)
                        # self.session.commit()

                # update_files
                except Exception as e:
                    logger.info(e)

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
                        if all(
                                [
                                    c in statistics.columns
                                    for c in self.statistics_required_columns
                                ]
                        ):
                            entity.statistics = row[src_format.statistics]
                        else:
                            warnings.warn(
                                f"Statistics has wrong format. Not all required columns"
                                f" ({self.statistics_required_columns})are in statistics"
                            )
                    else:
                        entity.statistics = statistics

                # check standard
                if not pd.isnull(row[src_format.standard_weights]):
                    standard_weights = pd.read_json(row[src_format.standard_weights])
                    if standard_weights is not None:
                        if all(
                                [
                                    c in standard_weights.columns
                                    for c in self.standard_required_columns
                                ]
                        ):
                            entity.standard_weights = row[src_format.standard_weights]
                        else:
                            warnings.warn(
                                f"Standard has wrong format. "
                                f"Not all required columns ({self.standard_required_columns})are in statistics"
                            )
                    else:
                        entity.standard_weights = standard_weights

                # UPSERT
                upsert_entity(
                    self.session, entity, update_on_conflict=True, update_nones=True
                )
                self.session.commit()
                logger.info(
                    f"\n\n{tuple(row[src_format.index_columns])} entity was updated"
                )
            except Exception as e:
                logger.info(f"{tuple(row[src_format.index_columns])}: {e}")
