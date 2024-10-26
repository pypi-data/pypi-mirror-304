import copy
import datetime
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
from brddb.models.postgres import Devices, CycleHouses, Houses, Farms, Clients
from brddb.utils.common import colorstr
from loguru import logger
from sqlalchemy.orm import sessionmaker, Session

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.get_and_add_methods import (
    upsert_device_info,
    get_cycle_houses,
)
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.data_structures.columns_struct import get_rename_dict
from bdm2.utils.schemas.models.storages.devices.devices_storage import (
    DevicesStorage,
    DevicesStorageColumnsNew,
)


@dataclass
class PostgresDevicesStorageColumnsNew(DevicesStorageColumnsNew):
    """
    Postgres' DevicesStorage has extra columns for storing primary keys.
    columns names are defined from get_cycle_houses(),
    where query.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) is used

    """

    client_id: str = field(default="clients_id", init=True)
    farm_id: str = field(default="farms_id", init=True)
    house_id: str = field(default="houses_id", init=True)
    device_id: str = field(default="devices_id", init=True)
    cycle_house_id: str = field(default="cycle_houses_id", init=True)
    flock_id: str = field(default="flocks_id", init=True)

    def __post_init__(self):
        self.client_name = "clients_name"
        self.client_code = "clients_code"

        self.farm_name = "farms_name"
        self.farm_code = "farms_code"
        self.country = "farms_country"

        self.house_name = "houses_name"
        self.house_code = "houses_code"

        self.device_name = "devices_name"
        self.device_code = "devices_code"
        self.rel_path = "cycle_devices_relative_path"

        self.cycle_house_name = "cycle_houses_name"
        self.cycle_house_code = "cycle_houses_code"
        self.cycle_device_code = "cycle_devices_code"
        self.cycle_start_date = "cycle_houses_cycle_start_date"
        self.usable_for_train = "cycle_devices_usable_for_train"
        self.comment = "cycle_devices_comment"

        self.flock_name = "flocks_name"
        self.gender = "genders_name"
        self.breed_type = "breed_types_name"


class PostgresDevicesStorage(DevicesStorage):
    _instance = None
    _update_interval = 60  # min
    _data = None
    _last_update = None
    _inner_format: PostgresDevicesStorageColumnsNew = PostgresDevicesStorageColumnsNew()

    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

    @property
    def inner_format(self) -> PostgresDevicesStorageColumnsNew:
        return PostgresDevicesStorageColumnsNew(
            **copy.deepcopy(self._inner_format.__dict__)
        )

    def _check_update(self, session: Optional[Session] = None):
        _need_update = False
        if self._data is None or self._last_update is None:
            _need_update = True
        elif (
                datetime.datetime.now() - self._last_update
        ).total_seconds() / 60 > self._update_interval:
            _need_update = True
        if _need_update:
            need_to_close_sess = False
            if session is None:
                need_to_close_sess = True
                session = sessionmaker(bind=postgres_engine)()
            self.update_df(session)
            if need_to_close_sess:
                session.close()

    def update_df(self, session: Session):
        _st_dt = datetime.datetime.now()
        self._data = get_cycle_houses(session, Filter(), add_devices=True)
        _end_dt = datetime.datetime.now()
        self._last_update = datetime.datetime.now()
        logger.info(
            f"data was updated. It takes: {(_end_dt - _st_dt).total_seconds():.2f} sec"
        )

    def convert_to_input_format(
            self, df: pd.DataFrame, src_format: DevicesStorageColumnsNew
    ) -> pd.DataFrame:

        df_output = pd.DataFrame(columns=self._inner_format.get_columns())
        rename_dict = {}
        for col1, col2 in zip(
                src_format.get_columns(), self._inner_format.get_columns()
        ):
            rename_dict[col1.strip()] = col2.strip()
        df_slt = df.rename(columns=rename_dict)

        union_columns = list(set(df_slt.columns).intersection(set(df_output.columns)))
        df_output = pd.concat(
            [
                df_output.reset_index(drop=True),
                df_slt[union_columns].reset_index(drop=True),
            ],
            axis=0,
            ignore_index=True,
        )
        return df_output

    def get_devices(
            self,
            filters: Filter,
            output_format: Optional[DevicesStorageColumnsNew] = None,
            dropna: bool = False,
            session: Optional[Session] = None,
    ) -> pd.DataFrame:

        if output_format is None:
            output_format = self.output_default_format
        self._check_update(session)

        # Convert to default format to let filters work with it
        # Loose info about data
        rename_dict = get_rename_dict(self.inner_format, DevicesStorageColumnsNew())
        _data = self._data.rename(columns=rename_dict)
        _data = filters.filter_devices(_data)
        if len(_data) == 0:
            logger.info(f"No devices after applying filters")
        rename_dict = get_rename_dict(DevicesStorageColumnsNew(), self.inner_format)
        _data = _data.rename(columns=rename_dict)

        if dropna:
            _data = self.dropna(_data, self.inner_format)

        if output_format is None:
            df_output = self.convert_formats(
                _data,
                input_format=self.inner_format,
                output_format=self.output_default_format,
                save_extra_columns=False,
            )
        else:
            df_output = self.convert_formats(
                _data,
                input_format=self.inner_format,
                output_format=output_format,
                save_extra_columns=False,
            )

        return df_output

    def delete_devices(
            self, filters: Filter, session: Optional[Session] = None, do_commit: bool = True
    ):
        need_to_close_sess = False
        if session is None:
            session = sessionmaker(bind=postgres_engine)()
            need_to_close_sess = True

        logger.info(" get devices .. ")
        # df = get_cycle_houses(self.session, filters)

        df = self.get_devices(filters, session=session)
        for df_iter, df_item in df.iterrows():
            try:
                if len(filters.devices) > 0:
                    device_id = df_item[self._inner_format.device_id]
                    delete_items_count = (
                        session.query(Devices).filter(Devices.id == device_id).delete()
                    )
                    logger.info(
                        f"Delete device_id : {device_id} ({delete_items_count})"
                    )

                if len(filters.cycles) > 0:
                    cycle_houses_id = df_item[self._inner_format.cycle_house_id]
                    delete_items_count = (
                        session.query(CycleHouses)
                        .filter(CycleHouses.id == cycle_houses_id)
                        .delete()
                    )
                    logger.info(
                        f"Delete cycle_houses : {cycle_houses_id} ({delete_items_count})"
                    )

                if len(filters.houses) > 0:
                    houses_id = df_item[self._inner_format.house_id]
                    delete_items_count = (
                        session.query(Houses).filter(Houses.id == houses_id).delete()
                    )
                    logger.info(f"Delete houses : {houses_id} ({delete_items_count})")

                elif len(filters.farms) > 0:
                    farm_id = df_item[self._inner_format.farm_id]
                    delete_items_count = (
                        session.query(Farms).filter(Farms.id == farm_id).delete()
                    )
                    logger.info(f"Delete farm_id : {farm_id} ({delete_items_count})")

                elif len(filters.clients) > 0:
                    clients_id = df_item[self._inner_format.client_id]
                    delete_items_count = (
                        session.query(Clients).filter(Clients.id == clients_id).delete()
                    )
                    logger.info(
                        f"Delete clients_id : {clients_id} ({delete_items_count})"
                    )

                else:
                    clients_id = df_item[self._inner_format.client_id]
                    delete_items_count = (
                        session.query(Clients).filter(Clients.id == clients_id).delete()
                    )
                    logger.info(
                        f"Delete clients_id : {clients_id} ({delete_items_count})"
                    )

            except Exception as ex:
                logger.info(f"Error then deleting \n" f"Exception {ex}")

        if need_to_close_sess:
            session.commit()
            logger.info("Commit DONE")
            session.close()
        elif do_commit:
            session.commit()
            logger.info("Commit DONE")
        logger.info("Deleting End")

    def update_devices(
            self,
            df: pd.DataFrame,
            src_format: DevicesStorageColumnsNew,
            session: Optional[Session] = None,
            do_commit: bool = True,
    ):
        need_to_close_sess = False
        if session is None:
            session = sessionmaker(bind=postgres_engine)()
            need_to_close_sess = True

        if type(df) is pd.Series:
            df = df.to_frame().T

        loc_df = self.convert_to_input_format(df=df, src_format=src_format)
        log_file = open("broke_upsert.csv", "w")
        log_file.write("client;farm;house;cycle;flock;device\n")
        for _, row in loc_df.iterrows():
            try:
                upsert_device_info(session, row, do_commit=do_commit, format=self._inner_format)
                logger.info(colorstr("green", f"\tDONE"))
            except Exception as ex:
                row_text = (
                    f"{row[self._inner_format.client_name]};"
                    f"{row[self._inner_format.farm_name]};"
                    f"{row[self._inner_format.house_name]};"
                    f"{row[self._inner_format.cycle_house_name]};"
                    f"{row[self._inner_format.flock_name]};"
                    f"{row[self._inner_format.device_name]}"
                    f"\n"
                )
                logger.info("Error then Upsert\n" f"{ex}\n" f"{row_text}")

                log_file.write(f"Problems with {row}")
        log_file.close()
        if need_to_close_sess:
            session.close()


if __name__ == "__main__":
    filters = Filter(farms=["BTG"], cycles=["Cycle 2"])
    st = PostgresDevicesStorage()
    st_format = st.output_default_format

    start_dt = datetime.datetime.now()
    st.get_devices(filters)
    end_dt = datetime.datetime.now()
    logger.info(f"First try takes: {(end_dt - start_dt).total_seconds():.2f} sec")

    start_dt = datetime.datetime.now()
    devices = st.get_devices(filters)
    end_dt = datetime.datetime.now()
    logger.info(f"Second try takes: {(end_dt - start_dt).total_seconds():.2f} sec")
    logger.info(f"{len(devices)} devices found")
    pass
