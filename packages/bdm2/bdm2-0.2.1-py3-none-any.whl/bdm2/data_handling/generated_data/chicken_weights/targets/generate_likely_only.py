#  Copyright (c) Anna Sosnovskaya

"""
Generate likely weights from already prepared Targets

Generated likely weights could be saved to several storages (both Targets and Likely will be saved)
Targets are also saved. if dst_weights_storages are different from src_weights_storages

**Utils/TargetWeightsGeneration/generate_likely_only.py**

Args:

:vis: if true, visualize all possible plots
:client: client name (always set to be able to define actual weights postfixes in sources)
:filters: Filters to specify houses scope
:src: Define base Targets to be used for Likely_targets generation.

.. note::
    If want to use actual weight postfix, use :func:`StandartsManager.get_actual_target_weights_postfix`

.. note::
    Likely target weight will be saves with the same postfix as src weights

:likely_weight_generation_params: params for generation likely weights (simple extrapolation)

:src_weights_storage:  can be LocalTargetWeightsStorage or PostgresAlchemyTargetWeightsStorage
:dst_weights_storages: dict of storages to be updated

"""
from typing import Dict

import matplotlib.pyplot as plt

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage

from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage
from brddb.utils.common import colorstr
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.weights_sources import WEIGHTS_SRC_TYPE
from bdm2.utils.schemas.models.storages.target_weights.local_target_weights_storage import LocalTargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.sqlalchemy_target_weights_storage import \
    PostgresAlchemyTargetWeightsStorage

from bdm2.data_handling.generated_data.chicken_weights.targets.targets_generators import SplineTargetsCombiner, \
    SimpleTargetsCombiner, WeightSrc, save_figures




from bdm2.data_handling.generated_data.standard import generate_standard



if __name__ == '__main__':

    # ========================== Settings =================================
    vis = False
    use_market_standard = True

    # client = 'CGBRCV'

    # Init filters
    filters = Filter()

    filters.clients = ['CGUKED']
    filters.breed_types = ['ROSS']
    filters.genders = ['mix']
    filters.farms = ['Middleton Stoney']  #Arbor Acres	female
    filters.cycles = ["Cycle 3"]
    filters.houses = [
        "House 6"

    ]


    # filters.cycles = ["Cycle 5"]
    # filters.houses = ["House 5"]

    # weights curve sources
    src = WeightSrc(name=WEIGHTS_SRC_TYPE['Targets'],
                    # postfix=StandartsManager.get_actual_target_weights_postfix(client)
                    postfix="_target_new" #  "_new_method_target"
                    )

    # define likely_weights generation params
    # Used for final likely weight generation
    likely_weight_generation_params = SplineTargetsCombiner.LikelyConfig(
        vis=vis,
        useLastStandardValue=True,
        use_market_standard=use_market_standard

    )

    #  ==================================================================
    # Init storages
    # devices storage
    src_devices_storage = PostgresDevicesStorage()

    # -- actual info
    # clients_info = LocalActualClientsInfoStorage(GlobalConfig.actual_engines_info_path)
    clients_info = PostgresActualClientsInfoStorage()

    # weights storage
    src_weights_storage = LocalTargetWeightsStorage(device_storage=src_devices_storage,
                                                    units=WEIGHTS_UNITS['kg'])

    # Init storages to be updated
    dst_weights_storages: Dict[str, TargetWeightsStorage] = {
        "Local": src_weights_storage,
        "PostfreSQL": PostgresAlchemyTargetWeightsStorage(device_storage=src_devices_storage,
                                                          units=WEIGHTS_UNITS['kg'])
    }
    simple_combiner = SimpleTargetsCombiner(src_devices_storage=src_devices_storage,
                                            src_weight_storage=src_weights_storage,
                                            filters=filters,
                                            weights_sources=[src],
                                            actual_info_storage=clients_info
                                            )

    simple_combiner.collect()
    combined_weights_df = simple_combiner.combine()

    combined_likely_weights_df = simple_combiner.generate_likely(combined_weights_df,
                                                                 likely_config=likely_weight_generation_params)
    combined_likely_weights_df['client'] = ''
    combined_combos = combined_weights_df[
        ['client', 'breed_type', 'gender', 'farm', 'cycle', 'house']].drop_duplicates()
    for i, row in combined_combos.iterrows():
        combined_likely_weights_df.loc[(combined_likely_weights_df.farm == row.farm) &
                                       (combined_likely_weights_df.cycle == row.cycle) &
                                       (combined_likely_weights_df.house == row.house), 'client'] = \
            combined_weights_df.loc[(combined_weights_df.farm == row.farm) &
                                    (combined_weights_df.cycle == row.cycle) &
                                    (combined_weights_df.house == row.house)]['client'].unique().tolist()[0]

        combined_likely_weights_df.loc[(combined_likely_weights_df.farm == row.farm) &
                                       (combined_likely_weights_df.cycle == row.cycle) &
                                       (combined_likely_weights_df.house == row.house), 'breed_type'] = \
            combined_weights_df.loc[(combined_weights_df.farm == row.farm) &
                                    (combined_weights_df.cycle == row.cycle) &
                                    (combined_weights_df.house == row.house)]['breed_type'].unique().tolist()[0]

        combined_likely_weights_df.loc[(combined_likely_weights_df.farm == row.farm) &
                                       (combined_likely_weights_df.cycle == row.cycle) &
                                       (combined_likely_weights_df.house == row.house), 'gender'] = \
            combined_weights_df.loc[(combined_weights_df.farm == row.farm) &
                                    (combined_weights_df.cycle == row.cycle) &
                                    (combined_weights_df.house == row.house)]['gender'].unique().tolist()[0]

    # смержить по ['farm', 'cycle', 'house'] клиент брид гендер
    plt.close()

    # Saving only likely
    for weights_storage in dst_weights_storages:
        print(colorstr('magenta', f"\n===============================\nUpdating {weights_storage}"))
        # len(list(set((
        #                          combined_weights_df.farm + ' ' + combined_weights_df.cycle + ' ' + combined_weights_df.house).tolist())))
        simple_combiner.save(combined_weights_df,
                             storage=dst_weights_storages[weights_storage],
                             weights_postfix=src.postfix)

        simple_combiner.save(combined_likely_weights_df,
                             storage=dst_weights_storages[weights_storage],
                             weights_postfix=src.postfix)

    save_figures(combined_weights_df, combined_likely_weights_df,
                 weights_format=src_weights_storage.output_default_format,
                 device_storage=src_devices_storage,
                 actual_info_storage=clients_info,
                 weights_postfix=src.postfix,
                 vis=vis
                 )

    # generate_standard(filters)
    print("FINISHED")
