from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
from sqlalchemy import UniqueConstraint, Table
from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, Query, Session

from bdm2.logger import build_logger

SQLABase = declarative_base()


def row2dict(row: SQLABase, drop_none=True) -> Dict[str, Any]:
    """
    Convert entities to dict,

    :param row: entity
    :param drop_none: if any of entity field are None on Nan, will drop them
    :return: dict
    """
    d = {}
    for column in row.__table__.columns:
        v = getattr(row, column.name)
        if pd.isnull(v):
            v = None
        if (v is None) and drop_none:
            continue
        d[column.name] = getattr(row, column.name)
    return d


def get_unique_constraints(table: Table) -> List[UniqueConstraint]:
    """
    Return all unique constraints that are defined for table

    :param table:
    :return: list of unique constraints
    """
    unique_constraints = [
        constraint
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]
    return unique_constraints


def compile_query(query: Query):
    """
    Compile SQLAlchemy query to the postgres engine format.
    Return compiled request, that can be used in session.execute()

    :param query: predefined query
    :return: compiled request, that can be used in session.execute()
    """
    compiler = (
        query.compile if not hasattr(query, "statement") else query.statement.compile
    )
    return compiler(dialect=postgresql.dialect())


def upsert(
        session: Session,
        model: SQLABase,
        rows: List[Dict[str, Any]],
        no_update_cols: Optional[List[str]] = None,
        logger=build_logger(Path(__file__), save_log=False)
):
    """
    Upsert many rows

    :param session:
    :param model:
    :param rows:
    :param no_update_cols:
    :return:
    @param logger:
    """
    if no_update_cols is None:
        no_update_cols = []

    table = model.__table__

    if not rows:
        logger.info(f"!!! Warning.  trying to add Nothing in DB ")
        return []

    stmt = postgresql.insert(table).values(rows).returning(table.c.id)

    unique_constraints = get_unique_constraints(table)
    unique_columns = []
    for uc in unique_constraints:
        for c in uc.columns:
            unique_columns.append(c)

    update_cols = [
        c.name
        for c in table.c
        if (c not in list(table.primary_key.columns))
           and (c not in unique_columns)
           and c.name not in no_update_cols
    ]

    if len(unique_columns):
        if len(update_cols):
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k) for k in update_cols},
            )
        else:
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k.name) for k in unique_columns},
            )
    try:

        # logger.info(f"{compile_query(stmt)}")
        # logger.info(f"{stmt}")
        result = session.execute(stmt)
        session.flush()
        ids = result.fetchall()
        return np.array(ids).flatten()
    except Exception as e:

        session.execute(text("ROLLBACK"))
        session.commit()
        raise e


def upsert_df(
        session: Session,
        model: SQLABase,
        df: pd.DataFrame,
        no_update_cols: Optional[List[str]] = None,
        do_commit: bool = True,
        logger=build_logger(Path(__file__), save_log=False)
):
    table = model.__table__
    unique_constraints = get_unique_constraints(table)
    unique_cols = []
    for uc in unique_constraints:
        for c in uc.columns:
            unique_cols.append(c.name)
    if len(unique_cols):
        assert (
                df.duplicated(unique_cols).sum() == 0
        ), f"upsert df has duplicates on unique constraints"
    table_columns = [c.name for c in table.columns]
    union_columns = list(set(table_columns).intersection(set(df.columns)))
    df_to_insert = df[union_columns].copy()
    df_to_insert = df_to_insert.dropna(subset=unique_cols, how="any")
    if len(df_to_insert) != len(df):
        logger.info(
            f"{len(df) - len(df_to_insert)} was droped as has nan values in unique columns"
        )

    if no_update_cols is None:
        no_update_cols = []

    if len(no_update_cols):
        no_update_cols_active = list(
            set(no_update_cols).intersection(set(df_to_insert.columns))
        )
        if len(no_update_cols_active):
            df_to_insert = df_to_insert.drop(no_update_cols_active, axis=1)
            logger.info(f"{no_update_cols_active} will not be inserted")
    df_to_insert = df_to_insert.replace(np.nan, None)
    upsert(session, model, df_to_insert.to_dict(orient="records"))
    if do_commit:
        session.commit()
    else:
        session.flush()


def upsert_entity(
        session: Session,
        entity: SQLABase,
        update_on_conflict: bool = False,
        no_update_cols: Optional[List[str]] = None,
        update_nones: bool = True,
) -> Optional[int]:
    """
    INSERT entity if not exist or UPDATE If conflict on unique constraints

    .. note::
        Need to session.commit() after!

    Example:
        table columns:
            id, farm, farm_code, country
        unique_constraints:
            Unique(farm_code)

        if trying to add entity with the farm_code that is already in table,
        will update existing data row (all fields that are in entity except no_update_cols
        and unique constraints columns.

        Also, if any of fields fas None values and NOT update_nones, these fields
        will also not to be updated)

    .. warning::
        Can be not correct work if several unique_constraints are specified for entity

    :param session: active session
    :param entity: object of class SQLABase
    :param update_on_conflict: if False, do nothing if conflict
    :param no_update_cols: if None or empty, update all columns (instead of unique and primary keys)
    :param update_nones: If True, will update database with None, if Nones are in entity
    :return: id of data row in database
    """

    data_to_update = row2dict(entity, drop_none=~update_nones)
    if no_update_cols is None:
        no_update_cols = []

    if not update_on_conflict:
        no_update_cols = [c.name for c in entity.__table__.c]

    table = entity.__table__
    stmt = postgresql.insert(table).values(data_to_update).returning(table.c.id)

    # TODO: not very clear implementation of unique_constraints. Need to check them separately.
    #  But SQL request can not handle several unique_constraints.
    unique_constraints = get_unique_constraints(table)
    unique_columns = []
    for uc in unique_constraints:
        for c in uc.columns:
            unique_columns.append(c)

    update_cols = [
        c.name
        for c in table.c
        if (c not in list(table.primary_key.columns))
           and (c not in unique_columns)
           and c.name not in no_update_cols
           and c.name in data_to_update.keys()
    ]

    if len(unique_columns):
        if len(update_cols):
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k) for k in update_cols},
            )
        else:
            stmt = stmt.on_conflict_do_update(
                index_elements=unique_columns,
                set_={k: getattr(stmt.excluded, k.name) for k in unique_columns},
            )
    try:
        # logger.info(f"{compile_query(stmt)}")
        # logger.info(f"{stmt}")
        result = session.execute(stmt)
        session.flush()
        ids = result.fetchall()
        ids = np.array(ids).flatten()
    except Exception as e:
        session.execute("ROLLBACK")
        session.commit()
        raise e
    finally:
        session.close()

    if len(ids) == 0:
        return None

    return int(ids[0])


def get_id_by_name(session, name: str, entity: SQLABase,
                   logger=build_logger(Path(__file__), save_log=False)) -> Optional[int]:
    """
    get Postgres table id by name field in table entity (if name is exists for entity and unique)

    :param session:
    :param name:
    :param entity:
    :return:
    @param logger:
    """
    rows = (
        session.execute(session.query(entity).where(entity.name == name))
        .scalars()
        .all()
    )
    if len(rows) == 0:
        return None
    if len(rows) > 1:
        logger.info(
            f"Execute response has more then 1 output. The first one only will be returned"
        )
    return rows[0].id
