import os.path
import datetime

from BIRDOO_IP import BirdooUtils

# Storages
from BIRDOO_IP.storages.target_weights.target_weights_storage import WEIGHTS_SRC_TYPE, WEIGHTS_UNITS, \
    TargetWeightsColumnsNew

from BIRDOO_IP.storages.target_weights.local_target_weights_storage import LocalTargetWeightsStorage
from BIRDOO_IP.storages.target_weights.sqlalchemy_target_weights_storage import PostgresAlchemyTargetWeightsStorage

from BIRDOO_IP.storages.devices.local_devices_storage import LocalDevicesStorage

from BIRDOO_IP.storages.utils.transfer_utils import compare_target_weights
from main_config import GlobalConfig

if __name__ == '__main__':

    filters = BirdooUtils.Filter()
    filters.clients = ['CGTHBG']
    # filters.farms = ['Kelly']  # Edegar
    # filters.cycles = ["Cycle 4"]
    # filters.houses = ['A08']
    # filters.age = ['A08']

    src_name = WEIGHTS_SRC_TYPE['Likely_targets']  # 'DOC', 'Farmers', "SLT" ,"Targets" ,"Likely_targets" ,"PIWFHA"
    weights_postfix = None  # '' - for Mahender and DOC, otherwise can be any other

    # INIT DEVICE STORAGE
    src_devices_storage = LocalDevicesStorage(GlobalConfig.device_csv)

    # INIT LOCAL WEIGHT STORAGE
    local_storage = LocalTargetWeightsStorage(device_storage=src_devices_storage,
                                              units=WEIGHTS_UNITS['kg'],
                                              use_slt_timetable_for_slt=True)

    # INIT DB WEIGHT STORAGE
    db_storage = PostgresAlchemyTargetWeightsStorage(
        device_storage=src_devices_storage,
        units=WEIGHTS_UNITS['kg']
    )

    logs_dir = 'compare_logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_fname = f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{src_name}.txt"
    log_fname = os.path.join(logs_dir, log_fname)

    weights_format = TargetWeightsColumnsNew()

    equal_map_gb = weights_format.house_index.get_columns()
    equal_map, compare_map = compare_target_weights(src_storage=local_storage, dst_storage=db_storage,
                                                    src_name=src_name,
                                                    weights_postfix=weights_postfix,
                                                    filters=filters,
                                                    compare_group_by=equal_map_gb,
                                                    weights_format=weights_format)

    print(f"\nWEIGHTS {src_name}{weights_postfix} SUMMARY ({local_storage.__class__.__name__}|{db_storage.__class__.__name__}):")
    compare_map_groups = compare_map.groupby(equal_map_gb)
    n_differences = 0

    with open(log_fname, 'w') as st:
        for label, row in equal_map.iterrows():
            if all(row == True):
                continue
            else:
                n_differences += 1
                diff_group = compare_map_groups.get_group(label)
                for _, diff_raw in diff_group.iterrows():

                    if not row['weight']:
                        weights_src = diff_raw["weight_src"]
                        weights_dst = diff_raw["weight_dst"]
                        if weights_src != weights_dst:
                            msg = f"Differences are found for {label} group: "
                            weights_postfix = diff_raw[weights_format.weights_postfix+"_src"]
                            msg += f"age {diff_raw[weights_format.age]}: "
                            msg += f"weight postfix {weights_postfix}: "
                            msg += f"weight ( {weights_src} | {weights_dst} ):"
                            print(msg)
                            st.write(msg+"\n")

        print(f'Total mismatches found: {n_differences} from {len(equal_map)} {equal_map_gb} groups')
