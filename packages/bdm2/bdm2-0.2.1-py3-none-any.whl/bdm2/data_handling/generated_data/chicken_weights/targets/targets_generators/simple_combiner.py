#  Copyright (c) Anna Sosnovskaya

from typing import Optional, List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE
from bdm2.data_handling.generated_data.checks.interpolation_outliers_search.components.common import colorstr
from bdm2.data_handling.generated_data.common_components.targets_generator import TargetsCombiner, WeightSrc
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import get_rename_dict
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.actual_clients_info_storage import \
    ActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage







class SimpleTargetsCombiner(TargetsCombiner):
    """
    Simple target weight combiner that just collect DOC, Farmers, PIWFHA weights

    .. note:
        During collection all duplicates by house_index + age will be DROPPED with keep='last' parameters.
        So chose weights_sources in init() properly (last ones has MORE priority)

    :param src_devices_storage: device info storage to obtain clients, cycle, breed type, gender info
    :param src_weight_storage: weight info storage
    :param filters: define devices scope to work
    :param weights_sources: src to be combined
    """

    def __init__(self,
                 src_devices_storage: DevicesStorage,
                 src_weight_storage: TargetWeightsStorage,
                 actual_info_storage: ActualClientsInfoStorage,
                 filters: Filter,
                 weights_sources: List[WeightSrc]
                 ):

        TargetsCombiner.__init__(self,
                                 src_devices_storage=src_devices_storage,
                                 src_weight_storage=src_weight_storage,
                                 actual_info_storage=actual_info_storage,
                                 filters=filters)

        self.weights_sources = weights_sources
        self.collected_weights = pd.DataFrame(columns=self.weights_format.get_columns())
        self.collected_weights = self.weights_format.convert_df_types(self.collected_weights)

    def collect(self) -> pd.DataFrame:
        for weights_src in self.weights_sources:
            weights_src_postfix_str = weights_src.postfix
            if weights_src_postfix_str is None:
                weights_src_postfix_str = "_actual_postfix"
            print(colorstr('blue', f'\nGetting {weights_src.name}{weights_src_postfix_str} weights'))
            weights = self.src_weight_storage.get_target_weights(src_name=weights_src.name,
                                                                 weights_postfix=weights_src.postfix,
                                                                 filters=self.filters,
                                                                 output_df_format=self.weights_format)

            if len(weights) == 0:
                print(colorstr('yellow',
                               f"{len(weights)} weights for {weights_src.name}{weights_src_postfix_str}"))
            else:
                print(colorstr('blue',
                               f"{len(weights)} weights for {weights_src.name}{weights_src_postfix_str} were found"))

            self.collected_weights = pd.concat([self.collected_weights, weights])

        self.collected_weights = self.collected_weights.drop_duplicates(
            self.weights_format.house_index.get_columns() + [self.weights_format.age],
            keep='last'
        )

        houses_df = self.get_houses(self.filters)

        self.collected_weights = self.match_device_info(self.collected_weights, houses_df)

        self.collected_weights = self.weights_format.convert_df_types(self.collected_weights)
        return self.collected_weights.copy()

    def combine(self) -> pd.DataFrame:
        age_column = self.weights_format.weight.age
        index_cols = self.weights_format.house_index.get_columns() + [age_column]
        df_output = self.collected_weights.drop_duplicates(subset=index_cols, keep='last')
        df_output = df_output.sort_values(by=index_cols)
        df_output = df_output.dropna(subset=[age_column])
        df_output[self.weights_format.weight_src.src_name] = WEIGHTS_SRC_TYPE['Targets']
        df_output[self.weights_format.weight_src.postfix] = np.nan
        df_output = self.weights_format.convert_df_types(df_output)
        return df_output
