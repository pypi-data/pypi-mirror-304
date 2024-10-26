import pytest
from typing import Dict, List

from BIRDOO_IP.birdoo_filter import Filter
from BIRDOO_IP.storages.devices.postgres_devices_storage import PostgresDevicesStorage

# Storages
from BIRDOO_IP.storages.target_weights.target_weights_storage import TargetWeightsStorage
from BIRDOO_IP.storages.target_weights.target_weights_storage import WEIGHTS_SRC_TYPE, WEIGHTS_UNITS
from BIRDOO_IP.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage
from BIRDOO_IP.storages.target_weights.sqlalchemy_target_weights_storage import PostgresAlchemyTargetWeightsStorage

from Utils.TargetWeightsGeneration.targets_generators import SimpleTargetsCombiner, WeightSrc

DEVICE_STORAGE = PostgresDevicesStorage()
ACTUAL_INFO_STORAGE = PostgresActualClientsInfoStorage()

WEIGHTS_STORAGES = [
    PostgresAlchemyTargetWeightsStorage(device_storage=DEVICE_STORAGE, units=WEIGHTS_UNITS['kg'])
]

FILTERS2TEST = [
    # Filter(clients=['CGBRCV'], breed_types=['ROSS'], genders=['mix']),
    Filter(clients=['CGTHBG'], cycles=["Cycle 1"], houses=['A03']),
    Filter(clients=['NOCLIENT'], cycles=["Cycle 1"], houses=['A03'])
]
# Weights sources
WEIGHT_SRC_SETS = [
    [WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""), WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None),
     WeightSrc(WEIGHTS_SRC_TYPE['Farmers'], "")],
    # [WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""), WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None)],
    [WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None)]
]


@pytest.mark.parametrize("src_weights_storage", WEIGHTS_STORAGES)
@pytest.mark.parametrize("filters", FILTERS2TEST)
@pytest.mark.parametrize("weights_sources", WEIGHT_SRC_SETS)
def test_simple_combiner(src_weights_storage: TargetWeightsStorage,
                         filters: Filter,
                         weights_sources: List[WeightSrc]):
    simple_combiner = SimpleTargetsCombiner(src_devices_storage=DEVICE_STORAGE,
                                            src_weight_storage=src_weights_storage,
                                            actual_info_storage=ACTUAL_INFO_STORAGE,
                                            filters=filters,
                                            weights_sources=weights_sources
                                            )
    collected_df = simple_combiner.collect()
    target_weigh_sources = [src.name for src in weights_sources]
    assert (all([c in target_weigh_sources for c in collected_df[simple_combiner.weights_format.weight_src.src_name]]),
            f'collected_df contains not requested weigh_sources')
    combined_weights_df = simple_combiner.combine()
    assert (all(combined_weights_df[simple_combiner.weights_format.weight_src.src_name] == 'Targets'),
            f'combined_weights_df contains not only targets')
    assert (all(combined_weights_df[simple_combiner.weights_format.weight_src.postfix].isna()),
            f'combined_weights_df contains not nan postfixes')
