import os
import pandas as pd
import copy

from main_config import GlobalConfig
from BIRDOO_IP import BirdooUtils

# Storages
from BIRDOO_IP.storages.target_weights.target_weights_storage import WEIGHTS_SRC_TYPE, WEIGHTS_UNITS

from BIRDOO_IP.storages.target_weights.local_target_weights_storage import LocalTargetWeightsStorage
from BIRDOO_IP.storages.target_weights.sqlalchemy_target_weights_storage import PostgresAlchemyTargetWeightsStorage

from BIRDOO_IP.storages.devices.local_devices_storage import LocalDevicesStorage
from BIRDOO_IP.storages.devices.postgres_devices_storage import PostgresDevicesStorage


from BIRDOO_IP.storages.utils.transfer_utils import transfer_target_weights

if __name__ == '__main__':

    filters = BirdooUtils.Filter()
    # filters.clients =['TDPHSM']
    #filters.farms = ['Euzebio']
    #filters.cycles = ['Cycle 3']
    # filters.farms = ['Cargill-NG']
    # filters.farms = ['BRF']

    # As it could be that in new weights some weights will be deleted.
    # It is better to clear all previous pack of weights and rewrite them. Deleting/updating pergorms per each house
    delete_all_weights_first = True
    use_actual_weights_postfix = True
    static_weights_postfix = "_Mahender_raw"

    device_storage = LocalDevicesStorage(GlobalConfig.device_csv)
    # device_storage = PostgresDevicesStorage()

    devices = device_storage.get_devices(filters = filters)
    if devices.empty:
        raise ValueError("No devices found for specified filters")

    src_name = WEIGHTS_SRC_TYPE['Targets']  # 'DOC', 'Farmers', "SLT" ,"Targets" ,"Likely_targets" ,"PIWFHA"
    # '' - for Mahender and DOC, otherwise can be any other

    local_storage = LocalTargetWeightsStorage(device_storage=device_storage,
                                              units=WEIGHTS_UNITS['kg'],
                                              use_slt_timetable_for_slt=False)

    p_db_storage = PostgresAlchemyTargetWeightsStorage(device_storage=device_storage,
                                                       units=WEIGHTS_UNITS['kg'])

    if use_actual_weights_postfix:
        weights_postfix = None
        transfer_target_weights(src_storage=local_storage,
                                dst_storage=p_db_storage,
                                src_name=src_name,
                                filters=filters,
                                weights_postfix=weights_postfix,
                                full_update=delete_all_weights_first,
                                use_actual_weights_postfix=True,
                                update_by=['farm']
                                )
    else:
        weights_postfix = static_weights_postfix
        transfer_target_weights(src_storage=local_storage,
                                dst_storage=p_db_storage,
                                src_name=src_name, weights_postfix=weights_postfix,
                                filters=filters,
                                full_update=delete_all_weights_first,
                                use_actual_weights_postfix=False,
                                update_by=['farm'])

    print("script work done")
