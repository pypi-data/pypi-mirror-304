from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    Date,
    UniqueConstraint,
    PrimaryKeyConstraint,
    JSON,
)

from bdm2.utils.schemas.components.sqlhelpers.helpers import SQLABase


# ============================================
# Static clients entities
# ============================================
class Clients(SQLABase):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    full_name = Column(String)
    code = Column(String)
    active = Column(Boolean)

    __table_args__ = (
        UniqueConstraint("code", name="clients_tb_client_un"),
        PrimaryKeyConstraint("id", name="pk_client_tb"),
    )


class Farms(SQLABase):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    full_name = Column(String)
    code = Column(String)
    country = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    __table_args__ = (
        UniqueConstraint("code", name="farm_table_code_un"),
        PrimaryKeyConstraint("id", name="pk_farm_tb"),
    )


class Houses(SQLABase):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    full_name = Column(String)
    code = Column(String)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    floor_id = Column(Integer, ForeignKey("floor_types.id"))
    size_length = Column(Float)
    size_width = Column(Float)
    size_height = Column(Float)
    max_bird_count = Column(Integer)
    ventilation_type_id = Column(Integer, ForeignKey("ventilation_types.id"))

    __table_args__ = (
        # UniqueConstraint('code',
        #                  name='houses_code_un'),
        UniqueConstraint("name", "farm_id", name="houses_name_farm_id_un"),
        PrimaryKeyConstraint("id", name="pk_house_tb"),
    )


# ============================================
# Cycles
# ============================================
class CycleHouses(SQLABase):
    __tablename__ = "cycle_houses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code = Column(String)
    house_id = Column(Integer, ForeignKey("houses.id"))
    cycle_start_date = Column(Date)

    __table_args__ = (
        # UniqueConstraint('code',
        #                  name='houses_code_un'),
        UniqueConstraint("name", "house_id", name="cycle_houses_name_house_id_un"),
        PrimaryKeyConstraint("id", name="pk_house_tb"),
    )


class Genders(SQLABase):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    __table_args__ = (
        # UniqueConstraint('code',
        #                  name='houses_code_un'),
        UniqueConstraint("name", name="genders_un"),
        PrimaryKeyConstraint("id", name="pk_genders_table"),
    )


class BreedTypes(SQLABase):
    __tablename__ = "breed_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    max_cycle_length = Column(Integer)
    __table_args__ = (
        UniqueConstraint("name", name="breed_types_un"),
        PrimaryKeyConstraint("id", name="pk_breed_types_table"),
    )


class Flocks(SQLABase):
    __tablename__ = "flocks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    breed_type_id = Column(Integer, ForeignKey("breed_types.id"))
    gender_id = Column(Integer, ForeignKey("genders.id"))
    hatch_date = Column(Date)
    farm_id = Column(Integer, ForeignKey("farms.id"))

    __table_args__ = (
        UniqueConstraint(
            "farm_id", "hatch_date", "breed_type_id", "gender_id", name="flocks_un"
        ),
        PrimaryKeyConstraint("id", name="pk_flock_table_1"),
    )


class CycleFlocks(SQLABase):
    __tablename__ = "cycle_flocks"
    id = Column(
        Integer,
        primary_key=True,
    )
    cycle_house_id = Column(Integer, ForeignKey("cycle_houses.id"))
    flock_id = Column(Integer, ForeignKey("flocks.id"))
    percent = Column(Float)
    # cycle_house_id = Column(Integer, ForeignKey('cycle_houses.id'))

    __table_args__ = (
        # UniqueConstraint('code',
        #                  name='houses_code_un'),
        # UniqueConstraint('flock_id', 'cycle_house_id',
        #                  name='cycle_flocks_un'),
        UniqueConstraint("cycle_house_id", name="cycle_flocks_un_tmp"),
        PrimaryKeyConstraint("id", name="cycle_flocks_pk"),
    )


# ============================================
# House params
# ============================================
class FloorTypes(SQLABase):
    __tablename__ = "floor_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class VentilationTypes(SQLABase):
    __tablename__ = "ventilation_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    comment = Column(String)


# ============================================
# Device params
# ============================================
class Devices(SQLABase):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    code = Column(String)
    hardware_type_id = Column(Integer, ForeignKey("hardware_types.id"))

    __table_args__ = (
        UniqueConstraint("name", name="devices_un"),
        PrimaryKeyConstraint("id", name="pk_device_table_1"),
    )


class CycleDevices(SQLABase):
    __tablename__ = "cycle_devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_house_id = Column(Integer, ForeignKey("cycle_houses.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    code = Column(String)
    relative_path = Column(String)
    usable_for_train = Column(Boolean)
    comment = Column(String)

    __table_args__ = (
        UniqueConstraint("device_id", "cycle_house_id", name="cycle_devices_un"),
        PrimaryKeyConstraint("id", name="cycle_devices_pk"),
    )


# class RelativePaths(SQLABase):
#     __tablename__ = 'relative_paths'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     cycle_house_id = Column(Integer, ForeignKey('cycle_houses.id'))
#     device_id = Column(Integer, ForeignKey('devices.id'))
#     value = Column(String)
#     cycle_device_id = Column(String)
#
#     __table_args__ = (
#         PrimaryKeyConstraint('id',
#                          name='relative_paths_pk'),
#         UniqueConstraint('cycle_house_id', 'device_id',
#                          name='relative_paths_un'),
#     )


class HardwareTypes(SQLABase):
    __tablename__ = "hardware_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    comment = Column(String)


class ActualClientsInfoTable(SQLABase):
    __tablename__ = "actual_clients_info"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    breed_type_id = Column(Integer, ForeignKey("breed_types.id"))
    gender_id = Column(Integer, ForeignKey("genders.id"))
    engine_config_id = Column(Integer, ForeignKey("engine_configs.id"))
    # TODO: check why ForeignKey does not work
    target_weights_src_id = Column(Integer)  # , ForeignKey('weight_sources.id'))
    piwfha_weights_src_id = Column(Integer)  # , ForeignKey('weight_sources.id'))
    likely_target_weights_src_id = Column(Integer)  # , ForeignKey('weight_sources.id'))
    standard_weights = Column(JSON)
    statistics = Column(JSON)

    __table_args__ = (
        UniqueConstraint(
            "client_id", "breed_type_id", "gender_id", name="actual_clients_info_un"
        ),
        PrimaryKeyConstraint("id", name="actual_clients_info_pk"),
    )

#
# class ActualClientsInfoView(SQLABase):
#     __tablename__ = 'actual_clients_info_storage'
#
#     client_id = Column(Integer,)
#     client = Column(Integer, ForeignKey('clients.id'),  primary_key=True, autoincrement=True)
#     breed_type_id = Column(Integer, ForeignKey('breed_types.id'),  primary_key=True, autoincrement=True)
#     gender_id = Column(Integer,ForeignKey('genders.id'),   primary_key=True, autoincrement=True)
#     engine_config_id = Column(Integer, ForeignKey('engine_configs.id'))
#     target_weights_source_id = Column(Integer, ForeignKey('weight_sources.id'))
#     piwfha_weights_src_id = Column(Integer, ForeignKey('weight_sources.id'))
