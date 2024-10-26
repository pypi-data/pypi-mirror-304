from typing import List, Dict, Optional, Union, Iterable, Any, Tuple
from pydantic import BaseModel, Field

import datetime
import numpy as np

import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func as sql_func
from sqlalchemy.orm import Query
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, ForeignKey, UniqueConstraint, \
    PrimaryKeyConstraint, \
    and_, delete,tuple_

from brddb.utils.sql import row2dict, get_uk_constraints
from brddb.models.postgres import *
from brddb.models.postgres.core import PG_PUBLIC_BASE
from brddb.constants import PgColumns
from brddb.schemas.pydantic.others import BirdooFilter

# from DataBase.SQLAlchemyTables.utils.utils import SQLABase

# =====================================================
# BRDDB Models
# =====================================================

__all__ = ['PIWFHAMethodsDescription', 'PIWFHACalculationMethods', 'PIWFHATable',
           # 'PIWFHAUpdateRequest', 'PIWFHA2Update',
           'multiple_upsert_statement',
           'get_specific_piwfha_methods_stmt', 'get_harvest_data_stmt', 'get_weight_source_info_stmt',
           'delete_piwfha_stmt']

from bdm2.utils.schemas.models.storages.house_performance_storage import SLTTimetable




class PIWFHAMethodsDescription(PG_PUBLIC_BASE):
    __tablename__ = "piwfha_methods_description"
    id = Column(Integer, primary_key=True)
    method_name = Column(String)
    description = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('id',
                             name='piwfha_methods_description_pk'),
        UniqueConstraint('method_name',
                         name='piwfha_methods_description_un'),
    )


class PIWFHACalculationMethods(PG_PUBLIC_BASE):
    __tablename__ = "piwfha_calculation_methods"
    id = Column(Integer, primary_key=True)
    specific_client_id = Column(Integer, ForeignKey('clients.id'))
    method_id = Column(Integer, ForeignKey('piwfha_methods_description.id'))
    aggregation_mode = Column(String)
    aggregation_max_age_diff = Column(Integer)
    __table_args__ = (
        UniqueConstraint('specific_client_id',
                         name='piwfha_calculation_methods_un'),
        PrimaryKeyConstraint('id',
                             name='piwfha_calculation_methods_pk'),
    )


class PIWFHATable(PG_PUBLIC_BASE):
    __tablename__ = 'piwfha_new'
    id = Column(Integer, primary_key=True, autoincrement=True)
    slt_id = Column(Integer, ForeignKey('slt_timetable.id'), nullable=False)
    src_id = Column(Integer, ForeignKey('weight_sources.id'), nullable=False)
    weight = Column(Float)
    fasting_start_dt = Column(DateTime)
    fasting_start_weight = Column(Float)
    piwfha_dt = Column(DateTime)
    fasting_time = Column(Float)
    weight_loss = Column(Float)
    comment = Column(String)
    updated = Column(DateTime, nullable=False)
    user_id = Column(String, nullable=False)
    method_id = Column(Integer, ForeignKey('piwfha_methods_description.id'), )
    aggregation_features = Column(JSON)

    __table_args__ = (UniqueConstraint('slt_id', 'src_id',
                                       name='piwfha_new_un'),
                      )


# =====================================================
# API schema
# =====================================================
# class PIWFHA2Update(BaseModel):
#     cycle_house_code: str = Field(..., example="DEFAULT-1-1")
#
#     slt_id: int
#     weight_src_postfix: str = Field(..., example="_union")
#     weight_src_id: int
#
#     age: int = Field(gt=0,lt=100)
#     weight: float = Field(gt=0,lt=10)
#     piwfha_dt: datetime.datetime
#     method_id: Optional[int]
#
#     fasting_start_dt: Optional[datetime.datetime] = Field(default=None)
#     fasting_start_weight: Optional[float] = Field(default=None,gt=0,lt=10)
#
#     fasting_time: Optional[float] = Field(default=None,gt=0,lt=100)
#     weight_loss: Optional[float] = Field(default=None)
#
#     aggregation_features: Optional[str] = Field(default=None)
#     comment: Optional[str]= Field(default=None)


# class PIWFHAUpdateRequest(BaseModel):
#     hard_update: bool
#     user: str = Field(..., example="user_name")
#     data: List[PIWFHA2Update]
#
# # =====================================================
# # BRD_DB QUERIES
# =====================================================


def add_filter(stmt: sqlalchemy.sql.Select, filters: BirdooFilter) -> sqlalchemy.sql.Select:
    """
    TODO: add description + consider renaming: add_filter -> add_birdoo_filter_to_stmt
    TODO: fix in brddb
    """
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


def get_specific_piwfha_methods_stmt():
    """
    TODO: primary usage: /views/get-specific-piwfha-methods endpoint
    """
    statement = sqlalchemy.select(
        CycleHouses.code.label('cycle_house_code'),
        Clients.code.label('client'),
        PIWFHACalculationMethods.method_id.label('calc_method_id'),
        PIWFHAMethodsDescription.method_name.label('calc_method_name'),
        PIWFHAMethodsDescription.description.label('calc_method_description'),
        PIWFHACalculationMethods.aggregation_mode.label('aggregation_mode'),
        PIWFHACalculationMethods.aggregation_max_age_diff.label('aggregation_max_age_diff')

    ) \
        .join(Houses, CycleHouses.house_id == Houses.id) \
        .join(Farms, Houses.farm_id == Farms.id, ) \
        .join(Clients, Farms.client_id == Clients.id) \
        .join(PIWFHACalculationMethods, PIWFHACalculationMethods.specific_client_id == Clients.id, isouter=True) \
        .join(PIWFHAMethodsDescription, PIWFHACalculationMethods.method_id == PIWFHAMethodsDescription.id, isouter=True)
    return statement


def get_harvest_data_stmt(piwfha_weight_postfix: Optional[str]):
    """
    TODO: primary usage: /views/slt-view endpoint
    """
    piwfha_subq = sqlalchemy.select(
        PIWFHATable.id.label('piwfha_id'),
        PIWFHATable.slt_id.label('slt_id_p'),
        PIWFHATable.method_id.label('piwfha_method_id'),
        PIWFHATable.src_id.label('piwfha_weight_src_id'),
        WeightSources.postfix.label('piwfha_weight_src_postfix'),
        PIWFHATable.piwfha_dt.label('piwfha_dt'),
        PIWFHATable.weight.label('piwfha_weight'),
        PIWFHATable.fasting_start_dt.label('fasting_start_dt'),
        PIWFHATable.fasting_start_weight.label('fasting_start_weight'),
        PIWFHATable.aggregation_features.label('piwfha_aggregation_features'),
        PIWFHATable.comment.label('piwfha_comment'),
        PIWFHATable.updated.label('piwfha_updated'),
    ) \
        .join(SLTTimetable, SLTTimetable.id == PIWFHATable.slt_id, isouter=False, ) \
        .join(CycleHouses, CycleHouses.id == SLTTimetable.cycle_house_id, isouter=False, ) \
        .join(Houses, CycleHouses.house_id == Houses.id) \
        .join(Farms, Houses.farm_id == Farms.id, ) \
        .join(Clients, Farms.client_id == Clients.id) \
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id, isouter=False, ) \
        .join(Flocks, Flocks.id == CycleFlocks.flock_id, isouter=False, ) \
        .join(BreedTypes, Flocks.breed_type_id == BreedTypes.id, isouter=False, ) \
        .join(Genders, Flocks.gender_id == Genders.id, isouter=False, ) \
        .join(WeightSources, PIWFHATable.src_id == WeightSources.id, isouter=False)

    if piwfha_weight_postfix is None:
        piwfha_subq = piwfha_subq.join(ActualClientsInfoTable,
                                       and_(ActualClientsInfoTable.client_id == Clients.id,
                                            ActualClientsInfoTable.breed_type_id == BreedTypes.id,
                                            ActualClientsInfoTable.gender_id == Genders.id), isouter=False)
        piwfha_subq = piwfha_subq.filter(PIWFHATable.src_id == ActualClientsInfoTable.piwfha_weights_src_id)
    else:
        piwfha_subq = piwfha_subq.filter(WeightSources.postfix == piwfha_weight_postfix)
    piwfha_subq = piwfha_subq.cte("piwfha_subq")

    # statement  = PIWFHA_subq
    statement = sqlalchemy.select(

        CycleHouses.id.label(PgColumns.cycle_house_id),
        CycleHouses.code.label(PgColumns.cycle_house_code),
        Clients.name.label(PgColumns.client_name),
        Farms.name.label(PgColumns.farm_name),
        Houses.name.label(PgColumns.house_name),
        CycleHouses.name.label(PgColumns.cycle_house_name),
        BreedTypes.name.label(PgColumns.breed_type_name),
        Genders.name.label(PgColumns.gender_name),
        CycleHouses.cycle_start_date.label(PgColumns.cycle_start_date),
        # TODO: replace with PgColumns

        SLTTimetable.id.label('slt_id'),
        SLTTimetable.age.label('harvest_age'),
        SLTTimetable.date.label('harvest_date'),
        SLTTimetable.weight.label('slt_weight'),
        SLTTimetable.slt_dt.label('slt_dt'),
        SLTTimetable.harvest_dt.label('harvest_dt'),
        SLTTimetable.lifting_dt.label('lifting_dt'),
        SLTTimetable.stop_feed_dt.label('stop_feed_dt'),
        SLTTimetable.bird_count.label('birds_count'),
        SLTTimetable.comment.label('slt_comment'),
        SLTTimetable.updated.label('slt_updated'),
        piwfha_subq

    ) \
        .join(Houses, CycleHouses.house_id == Houses.id, isouter=False, ) \
        .join(Farms, Houses.farm_id == Farms.id, isouter=False, ) \
        .join(Clients, Farms.client_id == Clients.id, isouter=False, ) \
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id, isouter=False, ) \
        .join(Flocks, Flocks.id == CycleFlocks.flock_id, isouter=False, ) \
        .join(BreedTypes, Flocks.breed_type_id == BreedTypes.id, isouter=False, ) \
        .join(Genders, Flocks.gender_id == Genders.id, isouter=False, ) \
        .join(SLTTimetable, CycleHouses.id == SLTTimetable.cycle_house_id, isouter=True, ) \
        .join(piwfha_subq, piwfha_subq.c.slt_id_p == SLTTimetable.id, isouter=True, )
    return statement


def get_weight_source_info_stmt(union_piwfha_postfix: Optional[str] = None, targets_postfix: Optional[str] = None, ):
    # ===================================
    # SUB STATEMENTS

    # PIWFHA weight sources subq
    union_piwfha_ws_subq = sqlalchemy.select(WeightSources.id, WeightSources.postfix) \
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id) \
        .filter(WeightSourceTypes.name == 'PIWFHA').filter(WeightSources.postfix.like("%_union"))
    union_piwfha_ws_subq = union_piwfha_ws_subq.cte("union_piwfha_ws_subq")

    piwfha_ws_subq = sqlalchemy.select(WeightSources.id, WeightSources.postfix) \
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id) \
        .filter(WeightSourceTypes.name == 'PIWFHA')
    piwfha_ws_subq = piwfha_ws_subq.cte("piwfha_ws_subq")

    targets_ws_subq = sqlalchemy.select(WeightSources.id, WeightSources.postfix) \
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id) \
        .filter(WeightSourceTypes.name == 'Targets')
    targets_ws_subq = targets_ws_subq.cte("targets_ws_subq")

    likely_targets_ws_subq = sqlalchemy.select(WeightSources.id, WeightSources.postfix) \
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id) \
        .filter(WeightSourceTypes.name == 'Likely_targets')
    likely_targets_ws_subq = likely_targets_ws_subq.cte("likely_targets_ws_subq")

    # ===================================
    # SUB STATEMENT
    base_stmt = sqlalchemy.select(
        CycleHouses.id.label(PgColumns.cycle_house_id),
        CycleHouses.code.label(PgColumns.cycle_house_code),
        # ActualClientsInfoTable,

        union_piwfha_ws_subq.c.id.label('piwfha_union_src_id'),
        union_piwfha_ws_subq.c.postfix.label('piwfha_union_src_postfix'),
        piwfha_ws_subq.c.id.label('piwfha_individual_src_id'),
        piwfha_ws_subq.c.postfix.label('piwfha_individual_src_postfix'),
        targets_ws_subq.c.id.label('targets_src_id'),
        targets_ws_subq.c.postfix.label('targets_src_postfix'),
        likely_targets_ws_subq.c.id.label('likely_targets_src_id'),
        likely_targets_ws_subq.c.postfix.label('likely_targets_src_postfix'),
    ) \
        .join(Houses, CycleHouses.house_id == Houses.id, isouter=False, ) \
        .join(Farms, Houses.farm_id == Farms.id, isouter=False, ) \
        .join(Clients, Farms.client_id == Clients.id, isouter=False, ) \
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id, isouter=False, ) \
        .join(Flocks, Flocks.id == CycleFlocks.flock_id, isouter=False, ) \
        .join(BreedTypes, Flocks.breed_type_id == BreedTypes.id, isouter=False, ) \
        .join(Genders, Flocks.gender_id == Genders.id, isouter=False, ) \
        .join(ActualClientsInfoTable, and_(ActualClientsInfoTable.client_id == Clients.id,
                                           ActualClientsInfoTable.breed_type_id == BreedTypes.id,
                                           ActualClientsInfoTable.gender_id == Genders.id, ))
    # ==================================================
    # ADD PIWFHA_UNION
    if union_piwfha_postfix is None:
        base_stmt = base_stmt \
            .join(union_piwfha_ws_subq,
                  union_piwfha_ws_subq.c.id == ActualClientsInfoTable.piwfha_weights_src_id,
                  isouter=True)
    else:
        base_stmt = base_stmt \
            .join(union_piwfha_ws_subq,
                  union_piwfha_ws_subq.c.postfix == union_piwfha_postfix,
                  isouter=True)
    base_stmt = base_stmt \
        .join(piwfha_ws_subq,
              piwfha_ws_subq.c.postfix == sql_func.substr(union_piwfha_ws_subq.c.postfix,
                                                          0,
                                                          sql_func.length(union_piwfha_ws_subq.c.postfix) - 5),
              isouter=True)
    if targets_postfix is None:
        base_stmt = base_stmt \
            .join(targets_ws_subq,
                  targets_ws_subq.c.id == ActualClientsInfoTable.target_weights_src_id,
                  isouter=True) \
            .join(likely_targets_ws_subq,
                  likely_targets_ws_subq.c.id == ActualClientsInfoTable.likely_target_weights_src_id,
                  isouter=True)
    else:
        base_stmt = base_stmt \
            .join(targets_ws_subq,
                  targets_ws_subq.c.postfix == targets_postfix,
                  isouter=True) \
            .join(likely_targets_ws_subq,
                  likely_targets_ws_subq.c.postfix == targets_postfix,
                  isouter=True)

    stmt = base_stmt
    return stmt


def multiple_upsert_statement(model: PG_PUBLIC_BASE,
                              rows: List[Dict[str, Any]],
                              no_update_cols: Optional[Iterable[str]] = None
                              ):
    """
    Returns `insert with update on conflict` statement guaranteeing no runtime error when table has some constraints
        declared in sqlalchemy table classes for primary/unique/foreign keys

    :param model:
    :param rows:
    :param no_update_cols:
    :return:
    """
    if no_update_cols is None:
        no_update_cols = []

    table = model.__table__

    if not rows:
        print(f"!!! Warning.  trying to add Nothing in DB ")
        return []

    stmt = postgresql.insert(table).values(rows).returning(table.c.id)

    unique_constraints = get_uk_constraints(table)
    unique_columns = []
    for uc in unique_constraints:
        for c in uc.columns:
            unique_columns.append(c)

    update_cols = [c.name for c in table.c
                   if (c not in list(table.primary_key.columns))
                   and (c not in unique_columns)
                   and c.name not in no_update_cols]

    if len(unique_columns):
        if len(update_cols):
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k) for k in update_cols}
            )
        else:
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k.name) for k in unique_columns}
            )
    return stmt


def delete_piwfha_stmt(ch_code_src_id_del_combinations: List[Tuple[str, int]]):
    """
    Return statement that delete all piwfha ages for specified combinations

    :param ch_id_src_id_del_combinations:
    :return:
    """
    stmt = delete(PIWFHATable)\
        .where(SLTTimetable.id == PIWFHATable.slt_id)\
        .where(CycleHouses.id==SLTTimetable.cycle_house_id)\
        .where(tuple_(CycleHouses.code, PIWFHATable.src_id).in_(ch_code_src_id_del_combinations))\
        .returning(PIWFHATable.id)
    return stmt
