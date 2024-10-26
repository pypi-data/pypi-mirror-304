#  Copyright (c) Anna Sosnovskaya

"""
Merge any combination of weights by sources (DOC, PIWFHA, Farmers) to Targets and also create correspondent
Likely_targets.

Most often usage - generating Targets_full , but also can be used to update piwfha to some already existed Targets

Combined weights could be saved to several storages (both Targets and Likely will be saved)

**Utils/TargetWeightsGeneration/combine_targets_simple.py**

Args:

:vis: if true, visualize all possible plots
:new_postfix: postfix for new generated Targets and Likely_targets weights
:use_default_standard: if True, will use default standard for generating Likely_targets, in other case - actual standard
:filters: Filters to specify houses scope

Weights to be combined (check :ref:`Weights Sources<WeightsSources>`)

:weight_sources: list of weights weight_sources to be combined

    .. note::
        Order of weight sources are important! if two sources has values for the same age,
        will be taken weight of source, that in closer to the end of list

    .. image:: /target_weights_managing/data/combine_simple.png
        :width: 400

    .. note::
        if want to use actual weights, use StandartsManager.get_actual_weights_postfix(src_type, client)

:likely_weight_generation_params: params for generation likely weights (simple extrapolation

Storages:

:src_devices_storage:  can be LocalClientsStorage or SQLClientsStorage
:src_weights_storage:  can be LocalTargetWeightsStorage or PostgresAlchemyTargetWeightsStorage
:dst_weights_storages: dict of storages to be updated

"""

from typing import Dict

from brddb.utils.common import colorstr

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE, house_match_columns
from bdm2.data_handling.generated_data.chicken_weights.targets.targets_generators.simple_combiner import \
    SimpleTargetsCombiner
from bdm2.data_handling.generated_data.chicken_weights.targets.targets_generators.spline_combiner import \
    SplineTargetsCombiner
from bdm2.data_handling.generated_data.common_components.targets_generator import WeightSrc, save_figures
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.local_target_weights_storage import LocalTargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.sqlalchemy_target_weights_storage import \
    PostgresAlchemyTargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage

if __name__ == '__main__':

    vis = False
    use_default_standard = False
    use_market_standard = True
    new_postfix = "_full_new_market"

    filters = Filter()
    filters.clients = ['CGTHBG']
    filters.breed_types = ['Arbor Acres']
    filters.genders = ['mix']
    filters.farms = ['BF2']  # Arbor Acres	female
    filters.cycles = ["Cycle 3"]

    clients_info = PostgresActualClientsInfoStorage()

    # Weights sources
    weight_sources = [
        # doc
        WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""),
        # piwfha
        WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None),
        # farmers
        WeightSrc(WEIGHTS_SRC_TYPE['Farmers'], ""),

        # # targets
        # WeightSrc(WEIGHTS_SRC_TYPE['Targets'],
        #           clients_info.get_actual_weights_postfix(WEIGHTS_SRC_TYPE['Targets'], client))

    ]

    # define likely_weights generation params
    # Used for final likely weight generation
    likely_weight_generation_params = SplineTargetsCombiner.LikelyConfig(
        vis=False,
        average=3,
        max_age=60,  # if None, will use full standard length
        use_default_standard=use_default_standard,
        use_market_standard=use_market_standard
    )

    # ===================================
    # Init source storages
    # ===================================

    # devices storage. Switch between postgres and local
    # src_devices_storage = LocalDevicesStorage(GlobalConfig.device_csv)
    src_devices_storage = PostgresDevicesStorage()

    # weights storage. Switch between postgres and local
    # src_weights_storage = LocalTargetWeightsStorage(device_storage=src_devices_storage,
    #                                                 units=WEIGHTS_UNITS['kg'])
    src_weights_storage = PostgresAlchemyTargetWeightsStorage(device_storage=src_devices_storage,
                                                              units=WEIGHTS_UNITS['kg'])

    # ===================================
    # Init storages to be updated
    # ===================================

    dst_weights_storages: Dict[str, TargetWeightsStorage] = {
        "Local": LocalTargetWeightsStorage(device_storage=src_devices_storage,
                                           units=WEIGHTS_UNITS['kg']),  # to update likely in src storage
        "PostgresSQL": PostgresAlchemyTargetWeightsStorage(device_storage=src_devices_storage,
                                                           units=WEIGHTS_UNITS['kg'])
    }

    simple_combiner = SimpleTargetsCombiner(src_devices_storage=src_devices_storage,
                                            src_weight_storage=src_weights_storage,
                                            actual_info_storage=clients_info,
                                            filters=filters,
                                            weights_sources=weight_sources
                                            )

    simple_combiner.collect()

    s_c_collected = simple_combiner.collected_weights.copy()
    s_c_collected.set_index(house_match_columns, inplace=True)

    for i, group in simple_combiner.collected_weights.groupby(house_match_columns):
        if 'PIWFHA' not in group['src_name'].values:
            s_c_collected = s_c_collected.loc[~(s_c_collected.index == i)]
            print(f"skipped {i} because of no PIWFHA in points")

    s_c_collected.reset_index(inplace=True)
    simple_combiner.collected_weights = s_c_collected

    combined_weights_df = simple_combiner.combine()

    combined_likely_weights_df = simple_combiner.generate_likely(combined_weights_df,
                                                                 likely_config=likely_weight_generation_params)

    # Saving Targets and Likely
    print()
    for weights_storage in dst_weights_storages:
        print(colorstr('magenta', f"\n===============================\nUpdating {weights_storage}"))
        simple_combiner.save(combined_weights_df,
                             storage=dst_weights_storages[weights_storage],
                             weights_postfix=new_postfix)
        simple_combiner.save(combined_likely_weights_df,
                             storage=dst_weights_storages[weights_storage],
                             weights_postfix=new_postfix)

    save_figures(combined_weights_df, combined_likely_weights_df,
                 weights_format=src_weights_storage.output_default_format,
                 device_storage=src_devices_storage,
                 actual_info_storage=clients_info,
                 weights_postfix=new_postfix,
                 vis=vis
                 )
    print("FINISHED")
