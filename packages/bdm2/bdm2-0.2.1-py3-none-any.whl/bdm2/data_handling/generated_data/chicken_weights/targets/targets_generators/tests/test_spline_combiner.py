import pandas as pd
import pytest
from typing import Dict, List

from main_config import GlobalConfig
from BIRDOO_IP.birdoo_filter import Filter
from BIRDOO_IP.storages.devices.postgres_devices_storage import PostgresDevicesStorage

# Storages
from BIRDOO_IP.storages.target_weights.target_weights_storage import TargetWeightsStorage
from BIRDOO_IP.storages.target_weights.target_weights_storage import WEIGHTS_SRC_TYPE, WEIGHTS_UNITS
from BIRDOO_IP.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage
from BIRDOO_IP.storages.target_weights.sqlalchemy_target_weights_storage import PostgresAlchemyTargetWeightsStorage

from Utils.TargetWeightsGeneration.targets_generators import SplineTargetsCombiner, WeightSrc

DEVICE_STORAGE = PostgresDevicesStorage()
ACTUAL_INFO_STORAGE = PostgresActualClientsInfoStorage()

LIKELY_GENERATION_PARAMS = [
    SplineTargetsCombiner.LikelyConfig( vis=False, average=5,  use_default_standard=True, max_age=None),
    SplineTargetsCombiner.LikelyConfig( vis=False, average=5,  use_default_standard=False, max_age=70),
]

WEIGHTS_STORAGES = [
    PostgresAlchemyTargetWeightsStorage(device_storage=DEVICE_STORAGE, units=WEIGHTS_UNITS['kg'])
]

FILTERS2TEST = [
    # Filter(clients=['CGBRCV'], breed_types=['ROSS'], genders=['mix']),
    Filter(clients=['CGTHBG'], cycles=["Cycle 1"], houses=['A03']),
    # Filter(clients=['NOCLIENT'], cycles=["Cycle 1"], houses=['A03'])
]
# Weights sources
WEIGHT_SRC_SETS = [
                      ([WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""), WeightSrc(WEIGHTS_SRC_TYPE['Farmers'], "")],
                       [WeightSrc(WEIGHTS_SRC_TYPE['DOC'], None), WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None)]),
]

# Load spline curve
SPLINE_CURVES = [
    pd.read_csv(r"../../spline_curves/spline_coefs_uform_KXPHPSM_80.csv", sep=';', header=None, index_col=0)[1],
    pd.read_csv(r"../../spline_curves/spline_coefs_sigmoid.csv", sep=';', header=None, index_col=0)[1],
    pd.read_csv(r"../../spline_curves/spline_coefs_uform.csv", sep=';', header=None, index_col=0)[1],
]


@pytest.mark.parametrize("src_weights_storage", WEIGHTS_STORAGES)
@pytest.mark.parametrize("filters", FILTERS2TEST)
@pytest.mark.parametrize("first_weights_sources,second_weights_sources", WEIGHT_SRC_SETS)
@pytest.mark.parametrize("spline_curve", SPLINE_CURVES)
@pytest.mark.parametrize("likely_generation_params", LIKELY_GENERATION_PARAMS)
@pytest.mark.parametrize("adjust_spline_curve", [False, True])
def test_simple_combiner(src_weights_storage: TargetWeightsStorage,
                         filters: Filter,
                         spline_curve: pd.Series,
                         likely_generation_params: SplineTargetsCombiner.LikelyConfig,
                         first_weights_sources: List[WeightSrc],
                         second_weights_sources: List[WeightSrc],
                         adjust_spline_curve:bool
                         ):

    spline_combiner = SplineTargetsCombiner(src_devices_storage=DEVICE_STORAGE,
                                            src_weight_storage=src_weights_storage,
                                            actual_info_storage=ACTUAL_INFO_STORAGE,
                                            filters=filters,
                                            spline_curve=spline_curve,
                                            extrapolation_params=likely_generation_params,
                                            first_weights_curve_src=first_weights_sources,
                                            second_weights_curve_src=second_weights_sources,
                                            vis=False,
                                            first_weights_curve_label='first',
                                            second_weights_curve_label='second',
                                            adjust_spline_curve=adjust_spline_curve
                                            )

    collected_df = spline_combiner.collect()
    target_weigh_sources =list(set ([src.name for src in first_weights_sources+second_weights_sources]))
    assert(all([c in target_weigh_sources for c in collected_df[spline_combiner.weights_format.weight_src.src_name]]),
           f'collected_df contains not requested weigh_sources')
    combined_weights_df = spline_combiner.combine()
    assert(all(combined_weights_df[spline_combiner.weights_format.weight_src.src_name] == 'Targets'),
           f'combined_weights_df contains not only targets')
    assert(all(combined_weights_df[spline_combiner.weights_format.weight_src.postfix].isna()),
           f'combined_weights_df contains not nan postfixes')

    combined_likely_weights_df = spline_combiner.generate_likely(combined_weights_df,
                                                                 likely_config=likely_generation_params)
