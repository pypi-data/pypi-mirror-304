from typing import *

import pandas as pd

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.storages.target_weights.sqlalchemy_target_weights_storage import \
    PostgresAlchemyTargetWeightsStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsColumnsNew

TargetWeightsColumnsNew()


def get_target_key_days(filters: Filter,
                        storage: Union[PostgresAlchemyTargetWeightsStorage],
                        src_names: List[str] = ['Farmers', 'PIWFHA'],
                        # units=WEIGHTS_UNITS['kg'],
                        output_df_format: Optional[TargetWeightsColumnsNew] = None,  # =TARGET_WEIGHTS_COLUMNS
                        ) -> Tuple[List[int], List[str]]:
    if output_df_format is None:
        output_df_format = TargetWeightsColumnsNew()

    output_df: pd.DataFrame = pd.DataFrame()
    for src_name in src_names:
        local_weights = storage.get_target_weights(src_name=src_name, weights_postfix=None,
                                                   filters=filters,
                                                   output_df_format=output_df_format)

        output_df = pd.concat([output_df, local_weights], axis=0, ignore_index=True)

    # cast to int:
    output_df = output_df.dropna(subset=['age'])
    ages = output_df['age'].astype(int).to_list()
    output_src_names: List[str] = output_df['src_name'].astype(str).to_list()
    return ages, output_src_names


if __name__ == '__main__':
    filters = Filter()
    filters.farms = ['JO']
    # device_storage = LocalDevicesStorage(GlobalConfig.device_csv)
    # local_storage = LocalTargetWeightsStorage(device_storage=device_storage,
    #                                           units=WEIGHTS_UNITS['kg'],
    #                                           use_slt_timetable_for_slt=True)
    # postgres_storage = PostgresAlchemyTargetWeightsStorage(device_storage=device_storage,
    #                                                        units=WEIGHTS_UNITS['kg'])
    #
    # output_df = get_target_key_days(filters=filters, storage=postgres_storage)
    # print(output_df.shape)
    # print(output_df.head(3))
    # # local_weights.set_index(GlobalConfig.house_match_columns)
    #
    #
