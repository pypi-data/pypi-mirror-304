# from brddb.models.postgres import Clients, Farms, CycleHouses, Devices,\
#     BreedTypes, Genders, CycleDevices, CycleFlocks, Flocks, Houses
from pathlib import Path

import pandas as pd
from numpy import nan
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm import sessionmaker

from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.engine.engine_sessions_utils import (
    cycle_start_day_to_datetime,
)
from bdm2.utils.schemas.components.columns import DevicesStorageColumnsNew
from bdm2.utils.schemas.components.sqlhelpers.helpers import (
    compile_query,
    upsert_entity,
)
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.storages.clients_storage import *


def add_filters(
        query: Query,
        filters: Filter,
        # check_client=True,
        # check_farm=True,
        # check_cycle=True,
        # check_house=True
) -> Query:
    # if len(filtration.clients) and check_client:
    #     query = query.filter(Clients.name.in_(filtration.clients))
    # if len(filtration.farms) and check_farm:
    #     query = query.filter(Farms.name.in_(filtration.farms))
    # if len(filtration.cycles) and check_cycle:
    #     query = query.filter(CycleHouses.name.in_(filtration.cycles))
    # if len(filtration.houses) and check_house:
    #     query = query.filter(Houses.name.in_(filtration.houses))

    if len(filters.clients):
        query = query.filter(Clients.name.in_(filters.clients))
    if len(filters.farms):
        query = query.filter(Farms.name.in_(filters.farms))
    if len(filters.cycles):
        query = query.filter(CycleHouses.name.in_(filters.cycles))
    if len(filters.houses):
        query = query.filter(Houses.name.in_(filters.houses))
    if len(filters.devices):
        query = query.filter(Devices.name.in_(filters.devices))
    if len(filters.breed_types):
        query = query.filter(BreedTypes.name.in_(filters.breed_types))
    if len(filters.genders):
        query = query.filter(Genders.name.in_(filters.genders))
    return query


def get_clients(session: Session, filters: Filter) -> pd.DataFrame:
    """
    Get client information based only on filtration.clients
    :param session:
    :param filters:
    :return: pd.DataFrame
    """

    query = (
        session.query(Clients)
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
    )
    query = add_filters(
        query,
        filters,
        # check_client=True,
        # check_farm=False,
        # check_cycle=False,
        # check_house=False
    )
    output = pd.read_sql_query(compile_query(query), postgres_engine.connect())
    return output


def get_farms(session: Session, filters: Filter) -> pd.DataFrame:
    """
    Get client, farm information based only on filtration.clients, filtration.farms
    :param session:
    :param filters:
    :return: pd.DataFrame
    """
    query = (
        session.query(Clients, Farms)
        .join(Farms, Farms.client_id == Clients.id, full=True)
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
    )
    query = add_filters(
        query,
        filters,
        # check_client=True,
        # check_farm=True,
        # check_cycle=False,
        # check_house=False
    )
    output = pd.read_sql_query(compile_query(query), postgres_engine.connect())
    return output


def get_houses(session: Session, filters: Filter) -> pd.DataFrame:
    """
    Get client, farm, house information based only on filtration.clients, filtration.farms , filtration.houses
    :param session:
    :param filters:
    :return: pd.DataFrame
    """
    query = (
        session.query(Clients, Farms, Houses)
        .join(Farms, Farms.client_id == Clients.id, full=True)
        .join(Houses, Houses.farm_id == Farms.id, full=True)
        .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
    )
    query = add_filters(
        query,
        filters,
        # check_client=True,
        # check_farm=True,
        # check_house=True,
        # check_cycle=False
    )
    output = pd.read_sql_query(compile_query(query), postgres_engine.connect())
    return output


def get_cycle_houses(
        session: Session, filters: Filter, add_devices=False
) -> pd.DataFrame:
    """
    Get client, farm, house, cycle_house information based only on filtration.clients, filtration.farms , filtration.houses, filtration.cycle
    :param session:
    :param filters:
    :return: pd.DataFrame
    """
    # TODO: set CycleFlocks,  Flocks, Genders, BreedTypes to be not full!!
    query = (
        session.query(
            Clients,
            Farms,
            Houses,
            CycleHouses,
            Devices,
            CycleDevices,
            CycleFlocks,
            Flocks,
            Genders,
            BreedTypes,
        )
        .join(Farms, Farms.client_id == Clients.id, full=True)
        .join(Houses, Houses.farm_id == Farms.id, full=True)
        .join(CycleHouses, CycleHouses.house_id == Houses.id, full=True)
        .join(CycleDevices, CycleDevices.cycle_house_id == CycleHouses.id, full=True)
        .join(Devices, CycleDevices.device_id == Devices.id, full=True)
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id, full=True)
        .join(Flocks, Flocks.id == CycleFlocks.flock_id, full=True)
        .join(Genders, Genders.id == Flocks.gender_id, full=True)
        .join(BreedTypes, BreedTypes.id == Flocks.breed_type_id, full=True)
    )

    query = query.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)

    query = add_filters(
        query,
        filters,
        # check_client=True,
        # check_farm=True,
        # check_cycle=True,
        # check_house=True
    )
    output = pd.read_sql_query(compile_query(query), postgres_engine.connect())

    return output


def get_cycle_house_id(session: Session, farm, house, cycle):
    query = (
        session.query(CycleHouses.id)
        .join(Houses, CycleHouses.house_id == Houses.id)
        .join(Farms, Houses.farm_id == Farms.id)
    )

    query = (
        query.filter(Farms.name == farm)
        .filter(Houses.name == house)
        .filter(CycleHouses.name == cycle)
    )
    ch_id = query.scalar()
    return ch_id


def upsert_device_info(
        session: Session,
        device_info: pd.Series,
        do_commit: bool = True,
        format: DevicesStorageColumnsNew = DevicesStorageColumnsNew(),
        logger=build_logger(Path(__file__), save_log=False)
):
    """
    :param session:
    :param _device_info:
    :return:
    @type logger: object
    @param format:
    @param do_commit:
    @param device_info:
    @param logger:
    """
    _device_info = device_info.replace(nan, None)

    logger.info("====================================================")
    logger.info(
        " ".join(
            _device_info[
                [
                    format.client_name,
                    format.farm_name,
                    format.house_name,
                    format.device_name,
                    format.cycle_house_name,
                ]
            ]
        )
    )
    try:
        client = Clients(
            name=_device_info[format.client_name], code=_device_info[format.client_code]
        )
        client_id = upsert_entity(
            session, client, update_on_conflict=False, update_nones=False
        )
        logger.info(f"client_id: {client_id}")

        farm = Farms(
            name=_device_info[format.farm_name],
            code=_device_info[format.farm_code],
            client_id=client_id,
            country=_device_info[format.country],
        )
        farm_id = upsert_entity(
            session, farm, update_on_conflict=True, update_nones=False
        )
        logger.info(f"farm_id: {farm_id}")

        if farm_id is None:
            raise Exception(
                "upsert_device_info -> farm_id is NaN. Can't upsert house, etc.."
            )

        house = Houses(
            farm_id=farm_id,
            name=_device_info[format.house_name],
            code=_device_info[format.house_code],
        )
        house_id = upsert_entity(
            session,
            house,
            update_on_conflict=True,
            no_update_cols=[],
            update_nones=False,
        )
        logger.info(f"house_id: {house_id}")

        if house_id is None:
            raise Exception(
                "upsert_device_info -> house_id is NaN. Can't upsert house, etc.."
            )

        devices = Devices(name=_device_info[format.device_name])
        devices_id = upsert_entity(
            session, devices, update_on_conflict=True, update_nones=False
        )
        logger.info(f"devices_id: {devices_id}")

        cycle_start_date = _device_info[format.cycle_start_date]
        if isinstance(cycle_start_date, str):
            cycle_start_date = cycle_start_day_to_datetime(cycle_start_date)
        cycle_house = CycleHouses(
            house_id=house_id,
            name=_device_info[format.cycle_house_name],
            code=_device_info[format.cycle_house_code],
            cycle_start_date=cycle_start_date,
        )
        cycle_house_id = upsert_entity(
            session, cycle_house, update_on_conflict=True, update_nones=True
        )
        logger.info(f"cycle_house_id: {cycle_house_id}")

        cycle_device = CycleDevices(
            cycle_house_id=cycle_house_id,
            device_id=devices_id,
            relative_path=_device_info[format.rel_path],
            code=_device_info[format.cycle_device_code],
            usable_for_train=_device_info[format.usable_for_train],
            comment=_device_info[format.comment],
        )
        cycle_device_id = upsert_entity(
            session, cycle_device, update_on_conflict=True, update_nones=False
        )
        logger.info(f"cycle_device_id: {cycle_device_id}")

        # rel_path = RelativePaths(cycle_house_id=cycle_house_id, device_id=devices_id,
        #                          value=_device_info[format.rel_path], cycle_device_id=_device_info[format.cycle_device_code])
        # upsert_entity(session, rel_path, update_on_conflict=True, update_nones=True)

        breed = BreedTypes(name=_device_info[format.breed_type])
        breed_id = upsert_entity(
            session, breed, update_on_conflict=False, update_nones=False
        )
        logger.info(f"breed_id: {breed_id}")

        gender = Genders(name=_device_info[format.gender])
        gender_id = upsert_entity(
            session, gender, update_on_conflict=False, update_nones=False
        )
        logger.info(f"gender_id: {gender_id}")

        hatch_date = _device_info[format.cycle_start_date]
        if isinstance(hatch_date, str):
            hatch_date = cycle_start_day_to_datetime(hatch_date)
        flock = Flocks(
            name=_device_info[format.flock_name],
            farm_id=farm_id,
            breed_type_id=breed_id,
            gender_id=gender_id,
            hatch_date=hatch_date,
        )
        flock_id = upsert_entity(
            session, flock, update_on_conflict=True, update_nones=True
        )
        logger.info(f"flock_id: {flock_id}")

        if (flock_id is not None) and (cycle_house_id is not None):
            cycle_flock = CycleFlocks(cycle_house_id=cycle_house_id, flock_id=flock_id)
            cycle_flock_id = upsert_entity(
                session, cycle_flock, update_on_conflict=True, update_nones=True
            )
            logger.info(f"cycle_flock_id: {cycle_flock_id}")

    except Exception as e:
        if do_commit:
            session.commit()
        raise e

    if do_commit:
        session.commit()


if __name__ == "__main__":

    logger = build_logger(Path(__file__), save_log=False)

    Session = sessionmaker(bind=postgres_engine)
    session = Session()

    filters = Filter(farms=["Euzebio"])
    f = get_farms(session, filters)
    logger.info(f"Found {len(f)} farms")

    ch = get_cycle_houses(session, filters)
    logger.info(f"Found {len(ch)} cycle-houses")
    for c in ch.columns:
        logger.info(c)
