import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from brddb.models.postgres import ActualClientsInfoTable
from pandas import DataFrame

from bdm2.logger import build_logger


class ColumnsStruct:
    def copy(self):
        return copy.deepcopy(self)

    def get_columns(self) -> List[str]:
        logger = build_logger(Path(__file__), save_log=False)
        output_cols = []
        attributes = self.__dict__
        for attr in attributes:
            if isinstance(attributes[attr], str):
                output_cols.append(attributes[attr])
            elif isinstance(attributes[attr], ColumnsStruct):
                output_cols += attributes[attr].get_columns()
            else:
                logger.info(
                    f"!! Warning !! Wrong format for attribute {attr}. Could be only str or ColumnsStruct"
                )
        return output_cols

    def convert_df_types(self, df: DataFrame) -> DataFrame:
        return df.copy()


from bdm2.utils.schemas.components.columns import ColumnsStruct


class ClientBreedGenderColumns(ColumnsStruct):
    def __init__(self, client: str, breed_type: str, gender: str):
        self.client = client
        self.breed_type = breed_type
        self.gender = gender


class HouseColumns(ColumnsStruct):
    def __init__(self, farm: str, cycle: str, house: str):
        self.farm = farm
        self.cycle = cycle
        self.house = house


class DeviceIndexColumns(ColumnsStruct):
    def __init__(self, farm: str, cycle: str, house: str, device: str):
        self.farm = farm
        self.cycle = cycle
        self.house = house
        self.device = device

    @property
    def house_columns(self) -> HouseColumns:
        return HouseColumns(farm=self.farm, cycle=self.cycle, house=self.house)


#
# # TODO: deprecate
# class ClientColumns(ColumnsStruct):
#     def __init__(self, client: str, country: str, farm: str, house: str, device: str):
#         self.client = client
#         self.country = country
#         self.farm = farm
#         self.house = house
#         self.device = device


class HouseInfoStruct(ColumnsStruct):
    def __init__(self, farm: str, cycle: str, house: str):
        self.farm = farm
        self.cycle = cycle
        self.house = house


# ======================================


# clients common data
class HouseNewColumns(ColumnsStruct):
    def __init__(self, client: str, farm: str, house: str):
        self.client: str = client
        self.farm: str = farm
        self.house: str = house


class DeviceColumns(ColumnsStruct):
    def __init__(self, client: str, farm: str, house: str, device: str):
        self.client: str = client
        self.farm: str = farm
        self.house: str = house
        self.device: str = device

    @property
    def house_columns(self) -> HouseNewColumns:
        return HouseNewColumns(client=self.client, farm=self.farm, house=self.house)


# flocks common data
class FlockColumns(ColumnsStruct):
    def __init__(
            self,
            flock: str,
            breed_type: str,
            gender: str,
            hatch_day: str,
    ):
        self.flock: str = flock
        self.breed_type: str = breed_type
        self.gender: str = gender
        self.hatch_day: str = hatch_day


# cycle common data
class CycleColumns(ColumnsStruct):
    def __init__(
            self, cycle: str, flock: str, breed_type: str, gender: str, hatch_day: str
    ):
        self.cycle: str = cycle
        self.flock: str = flock
        self.breed_type: str = breed_type
        self.gender: str = gender
        self.hatch_day: str = hatch_day

        # self.flock_columns: FlockColumns = flock

    @property
    def flock_columns(self) -> FlockColumns:
        return FlockColumns(
            flock=self.flock,
            breed_type=self.breed_type,
            gender=self.gender,
            hatch_day=self.hatch_day,
        )


# cycle-house common data
class CycleHouseColumns(ColumnsStruct):
    def __init__(self, house_struct: HouseNewColumns, cycle_struct: CycleColumns):
        self.house_columns: HouseNewColumns = house_struct
        self.cycle_columns: CycleColumns = cycle_struct


# cycle-house common data
class CycleDeviceColumns(ColumnsStruct):
    @property
    def house_columns(self) -> HouseNewColumns:
        return self.device_columns.house_columns

    def __init__(self, device_struct: DeviceColumns, cycle_struct: CycleColumns):
        self.device_columns: DeviceColumns = device_struct
        self.cycle_columns: CycleColumns = cycle_struct


# UNION STRUCTURES
HOUSE_COLUMNS = HouseNewColumns(client="client", farm="farm", house="house")
DEVICE_COLUMNS = DeviceColumns(**HOUSE_COLUMNS.__dict__, device="device")

FLOCK_COLUMNS = FlockColumns(
    flock="flock", breed_type="breed_type", gender="gender", hatch_day="hatch_day"
)
CYCLE_COLUMNS = CycleColumns(cycle="cycle", **FLOCK_COLUMNS.__dict__)

FULL_HOUSE_COLUMNS = CycleHouseColumns(
    house_struct=HOUSE_COLUMNS, cycle_struct=CYCLE_COLUMNS
)
FULL_DEVICE_COLUMNS = CycleDeviceColumns(
    device_struct=DEVICE_COLUMNS, cycle_struct=CYCLE_COLUMNS
)


# ss = HOUSE_COLUMNS + CYCLE_COLUMNS


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
class PostgresActualClientsInfoColumns(
    ActualClientsInfoColumns, PostgresInputActualClientsInfoColumns
):
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
