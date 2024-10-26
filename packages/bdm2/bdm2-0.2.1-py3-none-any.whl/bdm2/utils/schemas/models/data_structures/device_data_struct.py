from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct


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
