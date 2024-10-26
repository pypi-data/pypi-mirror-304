import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.device_data_struct import (ClientBreedGenderColumns,
                                                                          CycleColumns,
                                                                          CycleDeviceColumns,
                                                                          CycleHouseColumns,
                                                                          DeviceColumns,
                                                                          FlockColumns,
                                                                          HouseColumns)
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import StorageBase
from bdm2.utils.schemas.models.storages.brddbapi_client.brddb_client import brddb_client


logger = logging.getLogger("pipeline_runner")


@dataclass
class BrdDBDevicesStorageColumns(ColumnsStruct):
    """
    Struct for storing data format of DevicesStorage. It defines DeviceStorage working data format
    (each attribute is available data for DeviceStorage). It actually stores columns names of input/output data

    Used as DEFAULT data format

    """

    # Clients' Hierarchy
    client_id: str = field(default="client_id", init=True)
    client_name: str = field(default="client", init=True)
    client_code: str = field(default="client_code", init=True)

    farm_name: str = field(default="farm", init=True)
    farm_code: str = field(default="farm_code", init=True)
    farm_id: str = field(default="farm_id", init=True)

    # House's info
    house_id: str = field(default="house_id", init=True)
    house_name: str = field(default="house", init=True)
    house_code: str = field(default="house_code", init=True)

    # Cycles' info
    cycle_house_id: str = field(default="cycle_house_id", init=True)
    cycle_house_name: str = field(default="cycle", init=True)
    cycle_house_code: str = field(default="cycle_house_code", init=True)
    cycle_start_date: str = field(default="cycle_start_day", init=True)
    # Flocks' info
    flock_id: str = field(default="flock_id", init=True)
    # Genders' info
    gender_id: str = field(default="gender_id", init=True)
    gender: str = field(default="gender", init=True)
    # Breed types' info
    breed_type_id: str = field(default="breed_type_id")
    breed_type: str = field(default="breed_type", init=True)
    # Cycle House`s info
    cycle_house_id: str = field(default="cycle_house_id", init=True)
    cycle_house_code: str = field(default="cycle_house_code", init=True)
    cycle_house_name: str = field(default="cycle_house_name", init=True)
    # Device's info
    device_name: str = field(default="device", init=True)
    device_code: str = field(default="device_code", init=True)

    @property
    def cycle_columns(self) -> CycleColumns:
        return CycleColumns(
            cycle=self.cycle_house_name,
            start_date=self.cycle_start_date,
        )

    @property
    def house_columns(self) -> HouseColumns:
        return HouseColumns(
            client=self.client_name,
            farm=self.farm_name,
            house=self.house_name,
        )

    @property
    def client_breed_gender_columns(self) -> ClientBreedGenderColumns:
        return ClientBreedGenderColumns(
            client=self.client_name,
            breed_type=self.breed_type,
            gender=self.gender,
        )

    @property
    def house_index(self) -> CycleHouseColumns:
        return CycleHouseColumns(
            cycle=self.cycle_house_name,
            farm=self.farm_name,
            house=self.house_name,
        )

    @property
    def device_index(self) -> CycleDeviceColumns:
        return CycleDeviceColumns(
            cycle=self.cycle_house_name,
            farm=self.farm_name,
            house=self.house_name,
            device=self.device_name,
        )

    @property
    def flock_columns(self) -> FlockColumns:
        return FlockColumns(
            flock=self.flock_name,
            breed_type=self.breed_type,
            gender=self.gender,
            hatch_day=self.cycle_start_date,
        )

    @property
    def cycle_columns(self) -> CycleColumns:
        return CycleColumns(cycle=self.cycle_house_name, **self.flock_columns.__dict__)

    @property
    def device_columns(self) -> DeviceColumns:
        return DeviceColumns(**self.house_columns.__dict__, device=self.device_name)

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


class BrddbAPIDevicesStorage(StorageBase):
    @property
    def inner_as_default_format(self) -> BrdDBDevicesStorageColumns:
        output = {}
        loc_inner_format = self.inner_format
        for atr in BrdDBDevicesStorageColumns.__annotations__:
            output[atr] = loc_inner_format.__dict__[atr]
        return BrdDBDevicesStorageColumns(**output)

    @property
    def inner_format(self) -> BrdDBDevicesStorageColumns:
        return BrdDBDevicesStorageColumns()

    @property
    def output_default_format(self) -> BrdDBDevicesStorageColumns:
        return BrdDBDevicesStorageColumns()

    def generate_filter_from_df(
            self,
            df: pd.DataFrame,
            df_format: BrdDBDevicesStorageColumns,
    ) -> Filter:
        output_filter = Filter()

        all_columns = list(output_filter.__dict__.keys())
        union_columns = list(set(df.columns).intersection(all_columns))
        df_not_nan = df.dropna(subset=union_columns)

        if df_format.client_name in df_not_nan.columns:
            output_filter.clients = list(
                df_not_nan[df_format.client_name].dropna().unique(),
            )
        if df_format.farm_name in df_not_nan.columns:
            output_filter.farms = list(
                df_not_nan[df_format.farm_name].dropna().unique(),
            )
        if df_format.cycle_house_name in df_not_nan.columns:
            output_filter.cycles = list(
                df_not_nan[df_format.cycle_house_name].dropna().unique(),
            )
        if df_format.house_name in df_not_nan.columns:
            output_filter.houses = list(
                df_not_nan[df_format.house_name].dropna().unique(),
            )
        if df_format.device_name in df_not_nan.columns:
            output_filter.devices = list(
                df_not_nan[df_format.device_name].dropna().unique(),
            )
        if df_format.gender in df_not_nan.columns:
            output_filter.genders = list(df_not_nan[df_format.gender].dropna().unique())
        if df_format.breed_type in df_not_nan.columns:
            output_filter.breed_types = list(
                df_not_nan[df_format.breed_type].dropna().unique(),
            )
        return output_filter

    def dropna(
            self,
            df: pd.DataFrame,
            format: BrdDBDevicesStorageColumns,
    ) -> pd.DataFrame:
        logger.exception("try to use not implemented function")
        raise NotImplementedError
        cols_to_check = [
            c for c in format.device_columns.get_columns() if c in df.columns
        ]
        return df.dropna(axis=0, how="any", subset=cols_to_check)

    def get_devices(
            self,
            filters: Filter,
            output_format: Optional[BrdDBDevicesStorageColumns] = None,
            dropna: bool = False,
    ) -> pd.DataFrame:
        """
        return df with all unique devices (including cycle and flocks information), that matches filter

        :param filters: filter for specifying devices scope
        :param output_format: column names of output data
        :param dropna: drop rows with nan or None values in main device columns
        :return: devices df with output_format column's names
        """
        logger.exception("try to use not implemented function")
        raise NotImplementedError

    def get_houses(
            self,
            filters: Filter,
            output_format: Optional[BrdDBDevicesStorageColumns] = None,
    ) -> pd.DataFrame:
        """
        return df with all unique houses (including cycle and flocks information), that matches filter

        :param filters: filter for specifying house scope
        :param output_format: column names of output data
        :return: devices df with output_format column's names
        """
        if output_format is None:
            output_format = self.output_default_format

        houses = brddb_client.get_device_view().rename(
            columns=BrdDBDevicesStorageColumns().__dict__,
        )
        gpby_columns = output_format.house_columns.get_columns() + [
            output_format.cycle_house_name,
        ]
        houses = houses.groupby(gpby_columns, as_index=False).first()
        return houses

    def delete_devices(self, filters: Filter):
        """
        Add new device info to storage

        :param filters: filter for specifying house scope
        """
        logger.exception("try to use not implemented function")
        raise NotImplementedError

    def update_devices(self, df: pd.DataFrame, src_format: BrdDBDevicesStorageColumns):
        """
        Update device info to storage.

        :param df: device data to be updated, has to have src_format columns
        :param src_format: column's names to be used fir updating
        :return: None
        """
        logger.exception("try to use not implemented function")
        raise NotImplementedError
