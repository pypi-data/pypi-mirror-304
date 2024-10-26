import copy
from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.get_and_add_methods import add_filters
from bdm2.utils.schemas.components.sqlhelpers.helpers import (
    upsert_entity,
    upsert,
    get_unique_constraints,
    compile_query,
)
from bdm2.utils.schemas.models.storages.clients_storage import (
    CycleHouses,
    Houses,
    Farms,
    Clients,
    CycleFlocks,
    Flocks,
    BreedTypes,
    Genders,
)
from bdm2.utils.schemas.models.storages.house_performance_storage import (
    WeightSources,
    ChickenWeights,
    WeightSourceTypes,
)


def get_weight_src_id(
        session: Session, weight_src: str, weight_src_postfix: str
) -> int:
    query = session.query(
        WeightSources.id,
        WeightSourceTypes.name.label("weight_src"),
        WeightSources.postfix.label("weight_src_postfix"),
    ).join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id)

    query = query.filter(WeightSourceTypes.name == weight_src).filter(
        WeightSources.postfix == weight_src_postfix
    )

    output = pd.read_sql_query(compile_query(query), session.connection())

    if len(output) == 0:
        weight_src_type_id = (
            session.query(WeightSourceTypes.id)
            .filter(WeightSourceTypes.name == weight_src)
            .scalar()
        )
        assert (
                weight_src_type_id is not None
        ), f"{weight_src} not in {WeightSourceTypes.__tablename__}"

        entity = WeightSources(
            source_type_id=weight_src_type_id, postfix=weight_src_postfix
        )
        # if weight_src_postfix=="":
        #     entity.postfix = None
        id = upsert_entity(session, entity, update_on_conflict=False)
        session.flush()
    else:
        id = int(output.iloc[0].id)
    return id


def get_target_weights(session: Session, src_type: str, postfix: str, filters: Filter):
    # check filter. Filters will not
    if len(filters.devices) and len(filters.houses) == 0:
        raise ValueError(
            f"target_weights_utils.get_target_weights: "
            "It is impossible to get weights for devices without house information "
            "as weights are matched to houses"
        )

    query_filters = copy.copy(filters)
    query_filters.devices = []
    query = (
        session.query(
            CycleHouses.id.label("cycle_house_id"),
            Clients.name.label("client"),
            Farms.name.label("farm"),
            Houses.name.label("house"),
            CycleHouses.name.label("cycle"),
            BreedTypes.name.label("breed_type"),
            Genders.name.label("gender"),
            WeightSources.id.label("weight_src_id"),
            WeightSourceTypes.name.label("weight_src"),
            WeightSources.postfix.label("weight_src_postfix"),
            ChickenWeights.id,
            ChickenWeights.age,
            ChickenWeights.weight,
            ChickenWeights.confidence,
            ChickenWeights.updated,
            ChickenWeights.comment,
        )
        .join(WeightSources, ChickenWeights.source_id == WeightSources.id)
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id)
        .join(CycleHouses, ChickenWeights.cycle_house_id == CycleHouses.id)
        .join(Houses, CycleHouses.house_id == Houses.id)
        .join(Farms, Houses.farm_id == Farms.id)
        .join(Clients, Farms.client_id == Clients.id)
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id)
        .join(Flocks, CycleFlocks.flock_id == Flocks.id)
        .join(BreedTypes, Flocks.breed_type_id == BreedTypes.id)
        .join(Genders, Flocks.gender_id == Genders.id)
    )

    query = query.filter(
        WeightSourceTypes.name == src_type
    )  # .filter(WeightSources.postfix == postfix)

    query = query.filter(WeightSources.postfix == postfix)

    query = add_filters(
        query,
        query_filters,
    )
    if len(filters.ages):
        query = query.filter(ChickenWeights.age.in_(filters.ages))
    output = pd.read_sql_query(compile_query(query), session.connection())
    return output


def get_table_size(
        session: Session, src_type: str, postfix: str, filters: Filter
) -> int:
    query = (
        session.query(
            CycleHouses.id.label("cycle_house_id"),
            Clients.name.label("client"),
            Farms.name.label("farm"),
            Houses.name.label("house"),
            CycleHouses.name.label("cycle"),
            WeightSources.id.label("weight_src_id"),
            WeightSourceTypes.name.label("weight_src"),
            WeightSources.postfix.label("weight_src_postfix"),
            ChickenWeights.id,
            ChickenWeights.age,
            ChickenWeights.weight,
            ChickenWeights.confidence,
            ChickenWeights.comment,
        )
        .join(WeightSources, ChickenWeights.source_id == WeightSources.id)
        .join(WeightSourceTypes, WeightSources.source_type_id == WeightSourceTypes.id)
        .join(CycleHouses, ChickenWeights.cycle_house_id == CycleHouses.id)
        .join(Houses, CycleHouses.house_id == Houses.id)
        .join(Farms, Houses.farm_id == Farms.id)
        .join(Clients, Farms.client_id == Clients.id)
        .join(CycleFlocks, CycleFlocks.cycle_house_id == CycleHouses.id)
        .join(Flocks, CycleFlocks.flock_id == Flocks.id)
        .join(BreedTypes, Flocks.breed_type_id == BreedTypes.id)
        .join(Genders, Flocks.gender_id == Genders.id)
    )  # output_0 = pd.read_sql_query(compile_query(query), postgres_engine)

    query = query.filter(
        WeightSourceTypes.name == src_type
    )  # .filter(WeightSources.postfix == postfix)
    # output_1_1 = pd.read_sql_query(compile_query(query), postgres_engine)

    query = query.filter(WeightSources.postfix == postfix)
    # output_1_2 = pd.read_sql_query(compile_query(query), postgres_engine)

    # output_1 = pd.read_sql_query(compile_query(query), postgres_engine)
    query = add_filters(
        query,
        filters,
        # check_client=True,
        # check_farm=True,
        # check_cycle=False,
        # check_house=False
    )
    if len(filters.ages):
        query = query.filter(ChickenWeights.age.in_(filters.ages))
    row_count = query.count()
    return row_count


def upsert_weights(session: Session, df: pd.DataFrame) -> List[str]:
    unique_constr = get_unique_constraints(ChickenWeights.__table__)
    unique_cols = []
    for uc in unique_constr:
        for c in uc.columns:
            unique_cols.append(c.name)
    assert (
            df.duplicated(unique_cols).sum() == 0
    ), f"upsert df has duplicates on unique constraints"
    upsert_ids = upsert(session, ChickenWeights, df.to_dict(orient="records"))
    return upsert_ids
