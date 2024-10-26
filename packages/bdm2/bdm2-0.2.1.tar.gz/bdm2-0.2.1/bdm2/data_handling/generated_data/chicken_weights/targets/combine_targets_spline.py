#  Copyright (c) Anna Sosnovskaya

"""
Combine two target weight curves according to spline curve coefs.

**Utils/TargetWeightsGeneration/combine_targets_spline.py**

Two target weight curves are defined by first_curve_sources and second_curve_sources.
For each of two weights src sets will be generated two Likely weight curves.
After that, using spline coefs from spline_curve_fname this two curves are merged by using spline coefs.

.. note::
    The more spline coef the more impact of first curve

Args:

:vis: if true, visualize all possible plots
:spline_curve_fname: fname of spline coefs
:new_postfix: postfix for new generated Targets and Likely_targets weights
:filters: Filters to specify houses scope

Weights to be combined (check :ref:`Weights Sources<WeightsSources>`)

:first_curve_sources: weights sources for the first weight curve
:second_curve_sources: weights sources for the second weight curve

.. note::
    if needed to use actual weights, use StandardsManager.get_actual_weights_postfix(src_type, client)

:likely_weight_generation_params: params for generation likely weights (simple extrapolation)

Storages:

:src_devices_storage:  can be LocalClientsStorage or SQLClientsStorage
:src_weights_storage:  can be LocalTargetWeightsStorage or PostgresAlchemyTargetWeightsStorage
:dst_weights_storages: dict of storages to be updated

"""

from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt

from BIRDOO_IP.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage
from BIRDOO_IP.storages.devices.postgres_devices_storage import PostgresDevicesStorage
from main_config import GlobalConfig
from BIRDOO_IP import BirdooUtils

from BIRDOO_IP.storages.target_weights.target_weights_storage import TargetWeightsStorage, WEIGHTS_SRC_TYPE, \
    WEIGHTS_UNITS
from BIRDOO_IP.storages.target_weights.local_target_weights_storage import LocalTargetWeightsStorage
from BIRDOO_IP.storages.target_weights.sqlalchemy_target_weights_storage import PostgresAlchemyTargetWeightsStorage
from BIRDOO_IP.storages.devices.local_devices_storage import LocalDevicesStorage

from Utils.TargetWeightsGeneration.targets_generators import SplineTargetsCombiner, WeightSrc, save_figures
from Utils.EnginePreparation.utils.general import colorstr

if __name__ == '__main__':

    vis = False
    use_default_standard = False
    # Define spline curve
    spline_curve_fname = r"spline_curves/spline_coefs_uform_KXPHPSM_80.csv"
    # spline_curve_fname = r"spline_curves/spline_coefs_sigmoid.csv"  # 1/(1+EXP(-0.2*(x-25)))
    # spline_curve_fname = r"spline_curves/spline_coefs_uform.csv" #

    # Init actual clients info
    # clients_info = LocalActualClientsInfoStorage(GlobalConfig.actual_engines_info_path)
    clients_info = PostgresActualClientsInfoStorage()

    # Weights postfix to be saved
    new_postfix = "_full_new"

    # Init filters
    filters = BirdooUtils.Filter()
    filters.clients = ['CGUKED']
    filters.breed_types = ['ROSS']
    filters.genders = ['mix']
    filters.farms = ['Middleton Stoney']  # Arbor Acres	female
    filters.cycles = ["Cycle 3"]
    filters.houses = [
        "House 6"

    ]
    # filters.cycles = ["Cycle 1"]
    # filters.houses = ["House 775"]

    # First weights curve sources
    first_curve_label = 'doc_piwfha'
    first_curve_sources = [
        WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""),
        WeightSrc(WEIGHTS_SRC_TYPE['PIWFHA'], None)
    ]
    # Second weights curve sources
    second_curve_label = 'doc_farmers'
    second_curve_sources = [
        WeightSrc(WEIGHTS_SRC_TYPE['DOC'], ""),
        WeightSrc(WEIGHTS_SRC_TYPE['Farmers'], None)
    ]

    # define likely_weights generation params
    # Used for final likely weight generation and for combining
    likely_weight_generation_params = SplineTargetsCombiner.LikelyConfig(
        vis=vis,
        use_default_standard=use_default_standard,
        max_age=None
    )

    # Init storages
    # devices storage. Switch between postgres and local
    # src_devices_storage = LocalDevicesStorage(GlobalConfig.device_csv)
    src_devices_storage = PostgresDevicesStorage()

    # weights storage. Switch between postgres and local
    # src_weights_storage = LocalTargetWeightsStorage(device_storage=src_devices_storage,
    #                                                 units=WEIGHTS_UNITS['kg'])
    src_weights_storage = PostgresAlchemyTargetWeightsStorage(device_storage=src_devices_storage,
                                                              units=WEIGHTS_UNITS['kg'])

    # Init storages to be updated
    dst_weights_storages: Dict[str, TargetWeightsStorage] = {
        "Local": LocalTargetWeightsStorage(device_storage=src_devices_storage, units=WEIGHTS_UNITS['kg']),
        "PostgresSQL": PostgresAlchemyTargetWeightsStorage(device_storage=src_devices_storage,
                                                           units=WEIGHTS_UNITS['kg'])
    }

    # =================================================
    # ===================== RUN =======================
    # Load spline curve
    spline_curve = pd.read_csv(spline_curve_fname, sep=';', header=None, index_col=0)[1]

    spline_combiner = SplineTargetsCombiner(src_devices_storage=src_devices_storage,
                                            src_weight_storage=src_weights_storage,
                                            actual_info_storage=clients_info,
                                            filters=filters,
                                            spline_curve=spline_curve,
                                            extrapolation_params=likely_weight_generation_params,
                                            first_weights_curve_src=first_curve_sources,
                                            second_weights_curve_src=second_curve_sources,
                                            vis=vis,
                                            first_weights_curve_label=first_curve_label,
                                            second_weights_curve_label=second_curve_label
                                            )

    combined_weights_df = spline_combiner.collect()
    combined_splinted_weights_df = spline_combiner.combine()

    if combined_splinted_weights_df.empty:
        raise RuntimeError('spline_combiner.combine returned empty df.\n'
                           f'Maybe weight sources were set wrong. '
                           f'NOTICE, if you want to use actual weights use None on WeightSrc')
    combined_likely_weights_df = spline_combiner.generate_likely(combined_splinted_weights_df,
                                                                 likely_config=likely_weight_generation_params)

    plt.close()

    # Saving Targets and Likely
    print()
    for weights_storage in dst_weights_storages:
        print(colorstr('magenta', f"\n===============================\nUpdating {weights_storage} Targets"))
        spline_combiner.save(combined_weights_df,
                             storage=dst_weights_storages[weights_storage],
                             weights_postfix=new_postfix)
        print(colorstr('magenta', f"\n===============================\nUpdating {weights_storage} Likely_targets"))
        spline_combiner.save(combined_likely_weights_df,
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
