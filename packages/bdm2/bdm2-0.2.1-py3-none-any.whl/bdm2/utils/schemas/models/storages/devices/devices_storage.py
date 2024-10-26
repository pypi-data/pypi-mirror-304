from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.device_data_struct import (
    HouseNewColumns,
    DeviceIndexColumns,
    DeviceColumns,
    CycleColumns,
    FlockColumns,
    HouseColumns,
    ClientBreedGenderColumns,
)
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import StorageBase


@dataclass
class DevicesStorageColumnsNew(ColumnsStruct):
    """
    Struct for storing data format of DevicesStorage. It defines DeviceStorage working data format
    (each attribute is available data for DeviceStorage). It actually stores columns names of input/output data

    Used as DEFAULT data format

    It helps to switch between storages easily.

    .. warning::
        Each implementation on DeviceStorage has to be able to work with data, that has current struct' columns names
        self.get_devices() must return data with DevicesStorageColumn column' names
        self.update_devices() must be able to update data with DevicesStorageColumn column' names

    DevicesStorage data has full clients' hierarchy information:
        client -> farm -> house -> device

    And also contains information about cycle:
        house -> cycle -> flock -> breed_type, gender

    Each level of hierarchy has name (used in pawlin) and code (used in knex team)

    """

    # Clients' Hierarchy
    client_name: str = field(default="client", init=True)
    client_code: str = field(default="client_id", init=True)

    farm_name: str = field(default="farm", init=True)
    farm_code: str = field(default="farm_id", init=True)
    country: str = field(default="country", init=True)

    house_name: str = field(default="house", init=True)
    house_code: str = field(default="house_id", init=True)

    device_name: str = field(default="device", init=True)
    device_code: str = field(default="device_id", init=True)

    # Cycles' info
    cycle_house_name: str = field(default="cycle", init=True)
    cycle_house_code: str = field(default="cycle_house_id", init=True)
    cycle_device_code: str = field(default="id", init=True)  # TODO: change
    cycle_start_date: str = field(default="cycle_start_day", init=True)
    flock_name: str = field(default="flock", init=True)
    gender: str = field(default="gender", init=True)
    breed_type: str = field(default="breed_type", init=True)
    rel_path: str = field(default="path", init=True)
    usable_for_train: str = field(default="usable_for_train", init=True)
    comment: str = field(default="comment", init=True)

    @property
    def house_columns(self) -> HouseNewColumns:
        return HouseNewColumns(
            client=self.client_name, farm=self.farm_name, house=self.house_name
        )

    @property
    def client_breed_gender_columns(self) -> ClientBreedGenderColumns:
        return ClientBreedGenderColumns(
            client=self.client_name, breed_type=self.breed_type, gender=self.gender
        )

    @property
    def house_index(self) -> HouseColumns:
        return HouseColumns(
            cycle=self.cycle_house_name, farm=self.farm_name, house=self.house_name
        )

    @property
    def device_index(self) -> DeviceIndexColumns:
        return DeviceIndexColumns(
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


class DevicesStorageColumns(ColumnsStruct):
    """
    TODO: Deprecated. Better use DevicesStorageColumnsNew
    Data output format for all implementations of DevicesStorage

    """

    @property
    def house_columns(self) -> HouseNewColumns:
        return self.device_columns.house_columns

    @property
    def flock_columns(self) -> FlockColumns:
        return self.cycle_columns.flock_columns

    def __init__(self, device_columns: DeviceColumns, cycle_columns: CycleColumns):
        self.device_columns: DeviceColumns = device_columns
        self.cycle_columns: CycleColumns = cycle_columns
        self.farm_id = "farm_id"
        self.cycle_id = "cycle_id"
        self.house_id = "house_id"

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


class DevicesStorage(StorageBase):

    @property
    def output_default_format(self) -> DevicesStorageColumnsNew:
        """"""
        # DEPRECATED USING INNER FORMAT COLUMNS. TO COMPLEX TO MANAGE WTH
        #     output = {}
        #     loc_inner_format = self.inner_format
        #     for atr in DevicesStorageColumnsNew.__annotations__:
        #         output[atr] = loc_inner_format.__dict__[atr]
        #     return DevicesStorageColumnsNew(**output)
        return DevicesStorageColumnsNew()

    @property
    def inner_as_default_format(self) -> DevicesStorageColumnsNew:
        output = {}
        loc_inner_format = self.inner_format
        for atr in DevicesStorageColumnsNew.__annotations__:
            output[atr] = loc_inner_format.__dict__[atr]
        return DevicesStorageColumnsNew(**output)

    @property
    @abstractmethod
    def inner_format(self) -> DevicesStorageColumnsNew:
        """ """

    def generate_filter_from_df(
            self, df: pd.DataFrame, df_format: DevicesStorageColumnsNew
    ) -> Filter:
        output_filter = Filter()

        all_columns = list(output_filter.__dict__.keys())
        union_columns = list(set(df.columns).intersection(all_columns))
        df_not_nan = df.dropna(subset=union_columns)

        if df_format.client_name in df_not_nan.columns:
            output_filter.clients = list(
                df_not_nan[df_format.client_name].dropna().unique()
            )
        if df_format.farm_name in df_not_nan.columns:
            output_filter.farms = list(
                df_not_nan[df_format.farm_name].dropna().unique()
            )
        if df_format.cycle_house_name in df_not_nan.columns:
            output_filter.cycles = list(
                df_not_nan[df_format.cycle_house_name].dropna().unique()
            )
        if df_format.house_name in df_not_nan.columns:
            output_filter.houses = list(
                df_not_nan[df_format.house_name].dropna().unique()
            )
        if df_format.device_name in df_not_nan.columns:
            output_filter.devices = list(
                df_not_nan[df_format.device_name].dropna().unique()
            )
        if df_format.gender in df_not_nan.columns:
            output_filter.genders = list(df_not_nan[df_format.gender].dropna().unique())
        if df_format.breed_type in df_not_nan.columns:
            output_filter.breed_types = list(
                df_not_nan[df_format.breed_type].dropna().unique()
            )
        return output_filter

    @abstractmethod
    def convert_to_input_format(
            self, df: pd.DataFrame, src_format: DevicesStorageColumnsNew
    ) -> pd.DataFrame:
        """
        Convert df with format src_format to input format, All columns of df that are not in src_format will be lost

        :param df:
        :param src_format:
        :return: converted df
        """

    def dropna(
            self, df: pd.DataFrame, format: DevicesStorageColumnsNew
    ) -> pd.DataFrame:
        cols_to_check = [
            c for c in format.device_columns.get_columns() if c in df.columns
        ]
        return df.dropna(axis=0, how="any", subset=cols_to_check)

    @abstractmethod
    def get_devices(
            self,
            filters: Filter,
            output_format: Optional[DevicesStorageColumnsNew] = None,
            dropna: bool = False,
    ) -> pd.DataFrame:
        """
        return df with all unique devices (including cycle and flocks information), that matches filter

        :param filters: filter for specifying devices scope
        :param output_format: column names of output data
        :param dropna: drop rows with nan or None values in main device columns
        :return: devices df with output_format column's names
        """

    def get_houses(
            self, filters: Filter, output_format: Optional[DevicesStorageColumnsNew] = None
    ) -> pd.DataFrame:
        """
        return df with all unique houses (including cycle and flocks information), that matches filter

        :param filters: filter for specifying house scope
        :param output_format: column names of output data
        :return: devices df with output_format column's names
        """
        if output_format is None:
            output_format = self.output_default_format

        tmp_devices = self.get_devices(filters, output_format)
        gpby_columns = output_format.house_columns.get_columns() + [
            output_format.cycle_house_name
        ]
        houses = tmp_devices.groupby(gpby_columns, as_index=False).first()
        return houses

    @abstractmethod
    def delete_devices(self, filters: Filter):
        """
        Add new device info to storage

        :param filters: filter for specifying house scope
        """

    @abstractmethod
    def update_devices(self, df: pd.DataFrame, src_format: DevicesStorageColumnsNew):
        """
        Update device info to storage.

        :param df: device data to be updated, has to have src_format columns
        :param src_format: column's names to be used fir updating
        :return: None
        """
