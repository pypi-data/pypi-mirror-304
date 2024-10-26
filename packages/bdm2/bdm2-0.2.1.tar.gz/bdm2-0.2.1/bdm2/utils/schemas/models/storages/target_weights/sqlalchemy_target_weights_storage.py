import copy
import datetime
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional

import pandas as pd
import sqlalchemy.orm
from brddb.models.postgres import ChickenWeights
from brddb.utils.common import colorstr
from sqlalchemy.orm import sessionmaker

from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.get_and_add_methods import get_cycle_house_id
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.weights_structure import (
    WeightColumns,
)
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.brddb_actual_client_info_storage import \
    BrdDBActualClientsInfoStorage

from bdm2.utils.schemas.models.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage

from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import (
    TargetWeightsStorage,
    TargetWeightsColumnsNew,
)
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import (
    WEIGHTS_SRC_TYPE,
    WrongWeightsSourceType,
    ActualPostfixError,
)
from bdm2.utils.schemas.queries.weights.get_target_weights import (
    get_target_weights,
    get_weight_src_id,
    upsert_weights,
)


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
            weight=self.weight_value, age=self.age, confidence=self.confidence
        )

    def convert_df_types(self, df: pd.DataFrame,
                         logger=build_logger(Path(__file__), save_log=False)) -> pd.DataFrame:
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
            logger.info(
                colorstr(
                    "red",
                    f"TargetWeightsInputColumns:convert_df_types: could not convert:{e}",
                )
            )
            return df.copy()


@dataclass
class PostgresTargetWeightsColumns(TargetWeightsColumnsNew, TargetWeightsInputColumns):
    """"""

    id: str = ChickenWeights.id.key


class PostgresAlchemyTargetWeightsStorage(TargetWeightsStorage):
    """
    Chicken weights storage on cloud (PostgresSQL database)

    """

    def __init__(
            self,
            device_storage: DevicesStorage,
            units: str,
            session: Optional[sqlalchemy.orm.Session] = None,
    ):
        # TargetWeightsStorage.__init__(
        #     self, units, actual_info_storage=BrdDBActualClientsInfoStorage()
        # )
        TargetWeightsStorage.__init__(
            self, units, actual_info_storage=PostgresActualClientsInfoStorage()
        )

        # #
        # if session is None:
        #     session = sessionmaker(bind=postgres_engine)()

        self.session = session
        self.sessionmaker = sessionmaker(bind=postgres_engine)

        self.device_storage = device_storage
        self.devices_format = device_storage.output_default_format

        # Used for update PostgresSQL ChickenWeights table
        self.weights_input_format = TargetWeightsInputColumns()

        #: Defined by DataBase.SQLAlchemyTables.utils.target_weights_utils.get_target_weights(),
        #: which return data with this columns
        self._inner_format = PostgresTargetWeightsColumns(
            id="id",
            farm="farm",
            cycle="cycle",
            house="house",
            age="age",
            weight_value="weight",
            confidence="confidence",
            src_id="weight_src_id",
            weights_src_name="weight_src",
            weights_postfix="weight_src_postfix",
        )

    @property
    def inner_format(self) -> PostgresTargetWeightsColumns:
        return PostgresTargetWeightsColumns(
            **copy.deepcopy(self._inner_format.__dict__)
        )

    def convert_to_input_format(
            self, df: pd.DataFrame, src_format: TargetWeightsColumnsNew,
            logger=build_logger(Path(__file__), save_log=False)
    ) -> pd.DataFrame:
        logger.info(
            colorstr("blue", f"Converting df to PostgresSQL table input format")
        )
        df_output = pd.DataFrame(columns=self.weights_input_format.get_columns())
        session = self.sessionmaker()
        df_full = pd.DataFrame(columns=src_format.get_columns())
        df_full[df.columns] = df

        initial_df_size = len(df)

        # Drop data with unknown type
        df_full = df_full.dropna(subset=src_format.weight_src.get_columns(), axis=0)
        if len(df_full) == 0:
            return df_output

        elif len(df_full) != initial_df_size:
            logger.info(
                colorstr(
                    "red",
                    "Warning! convert_to_input_format: df_full has nan weight_src values",
                )
            )

        # with self.connection.cursor() as cursor:
        for (src_name, src_postfix), src_group in df.groupby(
                src_format.weight_src.get_columns()
        ):
            session_to_update_weight_src = self.sessionmaker()
            src_id = get_weight_src_id(
                session_to_update_weight_src,
                weight_src=src_name,
                weight_src_postfix=src_postfix,
            )
            session_to_update_weight_src.commit()
            session_to_update_weight_src.close()
            logger.info(f"Processing {src_name}{src_postfix}")
            assert (
                    src_id is not None
            ), f"Could not find and add {src_name} {src_postfix} to db"
            for (label), group in src_group.groupby(
                    src_format.house_index.get_columns()
            ):
                device = pd.Series(
                    list(label), index=src_format.house_index.get_columns()
                )
                device_label = " ".join(device)
                ch_id = get_cycle_house_id(
                    session,
                    farm=device["farm"],
                    house=device["house"],
                    cycle=device["cycle"],
                )
                if ch_id is None:
                    logger.info(
                        colorstr(
                            "red",
                            f"No information about {device_label} in cycle_house table (devices storage). "
                            f"Will be skipped",
                        )
                    )
                    continue

                group_to_dump = pd.DataFrame(index=group.index)

                group_to_dump[self.weights_input_format.cycle_house_id] = ch_id
                group_to_dump[self.weights_input_format.src_id] = src_id

                group_to_dump[self.weights_input_format.weight.get_columns()] = group[
                    src_format.weight.get_columns()
                ]
                group_to_dump[self.weights_input_format.updated] = (
                    datetime.datetime.now()
                )
                group_to_dump[self.weights_input_format.comment] = group[
                    src_format.comment
                ].values
                df_output = pd.concat([df_output, group_to_dump], ignore_index=True)
            logger.info("DONE")

        df_output = self.weights_input_format.convert_df_types(df_output)
        session.close()
        return df_output

    def get_target_weights(
            self,
            src_name: str,
            weights_postfix: Optional[str],
            filters: Filter,
            output_df_format: Optional[TargetWeightsColumnsNew] = None,
            logger=build_logger(Path(__file__), save_log=False)
    ) -> pd.DataFrame:
        """
        Get weight (src_name,weights_postfix) from PostgresSQL that matches filters
        If weights_postfix is None, will get weights for ACTUAL weghts postfix for specified src_name

        :param src_name: should be in
        :param weights_postfix:
        :param filters: define devices scope to get weights
        :param output_df_format:
        :return:
        """
        inner_session = False
        if self.session is None:
            self.session = self.sessionmaker()
            inner_session = True
        if output_df_format is None:
            output_df_format = self.output_default_format
        assert src_name in WEIGHTS_SRC_TYPE.values(), WrongWeightsSourceType(
            f"Wrong weights source type {src_name}"
        )

        # define output df
        weights_df_output = pd.DataFrame()
        # define devices scope
        target_devices = self.device_storage.get_houses(
            filters, output_format=self.devices_format
        )

        client_column = self.devices_format.client_name
        breed_column = self.devices_format.breed_type
        gender_column = self.devices_format.gender

        for (client, breed, gender), c_br_g_group in target_devices.groupby(
                [client_column, breed_column, gender_column]
        ):

            try:
                _weights_postfix = self.check_weights_postfix(
                    src_name, weights_postfix, client=client, breed=breed, gender=gender
                )
            except ValueError as e:
                logger.info(
                    colorstr(
                        "red",
                        f"{client} {breed} {gender} will be skipped as could not define weights postfix:\n"
                        f"{e}",
                    )
                )
                continue
            except ActualPostfixError as e:
                logger.info(
                    colorstr(
                        "red",
                        f"{client} {breed} {gender} will be skipped as could not define weights postfix:\n"
                        f"{e}",
                    )
                )
                continue
            cl_filters = self.device_storage.generate_filter_from_df(
                c_br_g_group, df_format=self.devices_format
            )
            # return df with inner format
            add_items = get_target_weights(
                self.session, src_name, _weights_postfix, cl_filters
            )

            # adding to output df
            weights_df_output = pd.concat(
                [weights_df_output, add_items], ignore_index=True
            )

        # Convert to output columns names (consider that weights_df_output has inner format)
        weights_df_output = self.convert_to_output_format(
            weights_df_output, output_df_format
        )

        # Convert units (to self.units and round to self.round)
        try:
            weights_df_output = self.convert_units(
                df=weights_df_output,
                age_column=output_df_format.weight.age,
                weight_column=output_df_format.weight.weight,
            )
        except Exception as e:
            logger.info(
                colorstr(
                    "red", "bold", f"ERROR! get_target_weights.convert_units.\n{e}"
                )
            )

        # Convert columns types
        weights_df_output = output_df_format.convert_df_types(weights_df_output)
        weights_df_output = filters.filter_res_df_csv(
            weights_df_output, age_col=output_df_format.age
        )
        if inner_session:
            self.session.close()
            self.session = None

        return weights_df_output

    def update_target_weights(
            self,
            weights_df: pd.DataFrame,
            input_df_format: TargetWeightsColumnsNew,
            need_commit: bool = True,
            logger=build_logger(Path(__file__), save_log=False)
    ):
        """
        Update weights df, that matches input_df_format.
        Convert weights_df to input format (define cycle house id, src_type id, etc.) and dump to ChickenWeights

        :param weights_df:
        :param input_df_format:
        :return:
        """
        inner_session = False
        if self.session is None:
            self.session = self.sessionmaker()
            inner_session = True

        initial_weight_size = len(weights_df)
        # converting to input format
        weights_df_to_dump = self.convert_to_input_format(weights_df, input_df_format)

        if len(weights_df_to_dump) != len(weights_df):
            logger.info(
                colorstr(
                    "red",
                    f"{len(weights_df) - len(weights_df_to_dump)}/{len(weights_df)} "
                    f"rows could not be converted to input format.",
                )
            )
        tmp_len = len(weights_df_to_dump)

        weight_column = self.weights_input_format.weight_value
        age_column = self.weights_input_format.age

        weights_df_to_dump = weights_df_to_dump.dropna(
            subset=[age_column, weight_column], how="any"
        )

        if len(weights_df_to_dump) != tmp_len:
            logger.info(
                colorstr(
                    "red",
                    f"{tmp_len - len(weights_df_to_dump)}/{tmp_len} rows has nan weight values.",
                )
            )

        try:
            weights_df_to_dump = self.convert_units(
                weights_df_to_dump, age_column=age_column, weight_column=weight_column
            )
        except Exception as e:
            logger.info(colorstr("red", f"warning! convert_units error:\n{e}"))

        weights_df_to_dump[weight_column] = (
            weights_df_to_dump[weight_column].astype(float).round(self.round)
        )

        weights_df_to_dump = weights_df_to_dump.drop_duplicates()
        weight_size = len(weights_df_to_dump)
        if weight_size != initial_weight_size:
            warnings.warn(
                f"Not all weights can be updated ({weight_size}/{len(weights_df_to_dump)})"
            )
        try:
            logger.info(colorstr("blue", "\nUpserting weights to storage"))
            ids = upsert_weights(self.session, weights_df_to_dump)
            logger.info(
                colorstr(
                    "green",
                    f"\tupsert_weights: DONE ({len(ids)} were updated/inserted)",
                )
            )
        except AssertionError as e:
            logger.info(colorstr("red", f"\tupsert_weights: FAILED:\n{e}"))

        if inner_session:
            self.session.commit()
            self.session.close()
            self.session = None
        else:
            if need_commit:
                self.session.commit()
            else:
                self.session.flush()

    def delete_target_weights(
            self,
            src_name: str,
            weights_postfix: Union[str, None],
            filters: Filter,
            need_commit: bool = True,
            logger=build_logger(Path(__file__), save_log=False)
    ) -> int:
        """
        After use session.commit()

        """

        # houses = self.device_storage.get_houses(filters, self.devices_format)
        # TODO: uncomment these lines (!)

        inner_session = False
        if self.session is None:
            self.session = self.sessionmaker()
            inner_session = True

        if filters.isempty():
            tw = []
        else:
            tw = self.get_target_weights(
                src_name=src_name,
                weights_postfix=weights_postfix,
                filters=filters,
                output_df_format=self.inner_format,
            )
        if len(tw):
            deleted_rows_count = (
                self.session.query(ChickenWeights)
                .filter(ChickenWeights.id.in_(tw[self.inner_format.id]))
                .delete()
            )  # tw[self.inner_format.id].tolist()
        else:
            deleted_rows_count = 0
        #
        # for src_id, weight_info in tw.groupby(self.inner_format.src_id):
        #     cycle_house_ids = [int(i) for i in weight_info[self.inner_format.cycle_house_id].unique()]
        #     tmp_deleted_rows_count = self.session.query(ChickenWeights) \
        #         .filter(ChickenWeights.cycle_house_id.in_(cycle_house_ids)) \
        #         .filter(ChickenWeights.source_id == src_id) \
        #         .delete()
        #     deleted_rows_count+=tmp_deleted_rows_count
        #     # logger.info(f"{client}:{farm}:{cycle}:{house} | src_name:'{src_name}' | postfix: '{_weights_postfix}'"
        #     #       f" - delete {deleted_rows_count} rows")
        logger.info(f" - delete {deleted_rows_count} rows")

        if inner_session:
            self.session.commit()
            self.session.close()
            self.session = None
        else:
            if need_commit:
                self.session.commit()
            else:
                self.session.flush()
        return deleted_rows_count
