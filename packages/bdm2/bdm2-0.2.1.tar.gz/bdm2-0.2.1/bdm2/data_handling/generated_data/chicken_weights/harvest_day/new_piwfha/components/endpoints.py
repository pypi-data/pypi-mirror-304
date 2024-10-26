import datetime
import json
from typing import List, Dict, Optional

import numpy as np
import sqlalchemy
from brddb.queries.postgres.slt import delete_piwfha_stmt, get_harvest_data_stmt, get_specific_piwfha_methods_stmt
from brddb.schemas.pydantic.postgres.piwfha import PIWFHAUpdateRequest
from sqlalchemy.orm import Query

from brddb.models.postgres import *
from brddb.constants import PgColumns
from brddb.utils.sql import row2dict, get_pk_constraints, multiple_upsert_statement
from brddb.schemas.pydantic.others import BirdooFilter

from bdm2.utils.schemas.connection import postgres_engine as pg_engine

# from DataBase.SQLAlchemyTables.connection import postgres_test_engine as pg_engine

__all__ = ['get_harvest_data', 'get_specific_piwfha_methods', 'get_actual_weight_source_info', 'update_piwfha_data']

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components._brddb import \
    get_weight_source_info_stmt
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import WeightSrcInfo


# =====================================================
# ENDPOINTS
# =====================================================


def add_filters(stmt: Query, filters: BirdooFilter
                ) -> Query:
    if filters.clients:  # allow cast to boolean container/None since it can be None
        stmt = stmt.filter(Clients.name.in_(filters.clients))
    if filters.farms:
        stmt = stmt.filter(Farms.name.in_(filters.farms))
    if filters.houses:
        stmt = stmt.filter(Houses.name.in_(filters.houses))
    if filters.devices:
        stmt = stmt.filter(Devices.name.in_(filters.devices))
    if filters.cycles:
        stmt = stmt.filter(CycleHouses.name.in_(filters.cycles))
    if filters.breed_types:
        stmt = stmt.filter(BreedTypes.name.in_(filters.breed_types))
    if filters.genders:
        stmt = stmt.filter(Genders.name.in_(filters.genders))
    return stmt


def get_harvest_data(filters: BirdooFilter,
                     piwfha_weight_src_postfic: Optional[str]):
    """
    TODO: primary usage: /views/cycle-house-harvest-view endpoint

    :param filters:
    :return:
    """
    # _output_data: Dict[str, CycleHarvestData] = {}
    stmt = get_harvest_data_stmt(piwfha_weight_src_postfic)
    stmt = add_filters(stmt, filters)

    # check for specific method
    with pg_engine.connect() as session:
        res = session.execute(stmt).fetchall()

    return res


def get_actual_weight_source_info(union_piwfha_postfix: Optional[str] = None,
                                  targets_postfix: Optional[str] = None,
                                  filters: Optional[BirdooFilter] = None) -> Dict[str, WeightSrcInfo]:
    stmt = get_weight_source_info_stmt(union_piwfha_postfix, targets_postfix)
    if filters is not None:
        stmt = add_filters(stmt, filters)
    with pg_engine.connect() as session:
        res = session.execute(stmt).fetchall()
    return res


def get_specific_piwfha_methods(filters: Optional[BirdooFilter]):
    stmt = get_specific_piwfha_methods_stmt()
    if filters is not None:
        stmt = add_filters(stmt, filters)
    with pg_engine.connect() as session:
        res = session.execute(stmt).fetchall()
    return res


def update_piwfha_data(piwfha2update: PIWFHAUpdateRequest):
    """

    :param cycle_house_data:
    :return:
    """
    # delete first if hard_update
    ch_code_src_id_del_combinations = []
    if piwfha2update.hard_update:
        for _data in piwfha2update.data:
            ch_code_src_id_del_combinations.append((_data.cycle_house_code, _data.weight_src_id))
    ch_code_src_id_del_combinations = list(set(ch_code_src_id_del_combinations))
    update_nones = True
    data2upsert = []
    for _data in piwfha2update.data:
        entity = PIWFHATable(
            slt_id=_data.slt_id,
            src_id=_data.weight_src_id,
            weight=_data.weight,
            fasting_start_dt=_data.fasting_start_dt,
            fasting_start_weight=_data.fasting_start_weight,
            piwfha_dt=_data.piwfha_dt,
            fasting_time=_data.fasting_time,
            weight_loss=_data.weight_loss,
            comment=_data.comment,
            updated=datetime.datetime.now(),
            user_id=piwfha2update.user,
            method_id=_data.method_id,
            aggregation_features=json.loads(_data.aggregation_features) if _data.aggregation_features else sqlalchemy.null()
        )
        upsert_data = row2dict(entity, drop_none=not update_nones)
        # ignore ids when upsert
        pk_columns = [c.key for c in get_pk_constraints(entity.__table__)[0].columns]
        for pk_col in pk_columns:
            if pk_col in upsert_data:
                del upsert_data[pk_col]
        data2upsert.append(upsert_data)

    with pg_engine.connect() as session:
        try:

            if len(ch_code_src_id_del_combinations) > 0:
                del_stmt = delete_piwfha_stmt(ch_code_src_id_del_combinations=ch_code_src_id_del_combinations)
                result = session.execute(del_stmt)
                # session.flush()
                print(f"{result.rowcount} rows were deleted")

            upsert_stmt = multiple_upsert_statement(model=PIWFHATable, rows=data2upsert, no_update_cols=None)
            result = session.execute(upsert_stmt)
            # session.flush()
            ids = result.fetchall()
            ids = np.array(ids).flatten()
            print(f"{len(ids)} rows were inserted")
        except Exception as E:
            session.rollback()
            print(f"{E}")
            raise E
    # print(ids)
    return ids
