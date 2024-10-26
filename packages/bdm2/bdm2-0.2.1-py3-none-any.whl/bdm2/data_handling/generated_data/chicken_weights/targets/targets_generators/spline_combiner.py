#  Copyright (c) Anna Sosnovskaya

from typing import Optional, List, Iterable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from brddb.utils.common import colorstr

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE, standards_match_columns, house_match_columns
from bdm2.data_handling.generated_data.chicken_weights.targets.targets_generators.targets_generator import WeightSrc
from bdm2.data_handling.generated_data.common_components import manual_weights_manager
from bdm2.data_handling.generated_data.common_components.manual_weights_manager import convert_to_kg
from bdm2.data_handling.generated_data.common_components.targets_generator import TargetsCombiner
from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import ActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage



class SplineTargetsCombiner(TargetsCombiner):
    """
    Advanced target weight combiner that interpolate targets between 2 weight curves with spline curve

    :param src_devices_storage: device info storage to obtain clients, cycle, breed type, gender info
    :param src_weight_storage: weight info storage
    :param filters: define devices scope to work
    :param spline_curve: spline coefs where indexes are ages (will be adjusted to extrapolated src curves length)
    :param first_weights_curve_src: weight sourced to be combined for first likely eights curve
    :param second_weights_curve_src: weight sourced to be combined for first likely eights curve
    """

    def __init__(self,
                 src_devices_storage: DevicesStorage,
                 src_weight_storage: TargetWeightsStorage,
                 actual_info_storage: ActualClientsInfoStorage,
                 filters: Filter,
                 spline_curve: pd.Series,
                 first_weights_curve_src: List[WeightSrc],
                 second_weights_curve_src: List[WeightSrc],
                 extrapolation_params: TargetsCombiner.LikelyConfig,
                 vis: bool = False,
                 first_weights_curve_label: str = 'first',
                 second_weights_curve_label: str = 'second',
                 adjust_spline_curve: bool = True,
                 ):

        TargetsCombiner.__init__(self,
                                 src_devices_storage=src_devices_storage,
                                 src_weight_storage=src_weight_storage,
                                 actual_info_storage=actual_info_storage,
                                 filters=filters)

        self.spline_curve = spline_curve
        self.adjust_spline_curve = adjust_spline_curve
        self.extrapolation_params = extrapolation_params
        self.first_weights: pd.DataFrame = pd.DataFrame(columns=self.weights_format.get_columns())
        self.second_weights: pd.DataFrame = pd.DataFrame(columns=self.weights_format.get_columns())

        assert len(first_weights_curve_src) > 0
        assert len(second_weights_curve_src) > 0

        self.first_weights_curve_src = first_weights_curve_src
        self.second_weights_curve_src = second_weights_curve_src

        self.first_weights_curve_label = first_weights_curve_label
        self.second_weights_curve_label = second_weights_curve_label

        self.vis = vis

    def collect(self) -> pd.DataFrame:

        #  first weights
        for weights_src in self.first_weights_curve_src:
            weights = self.src_weight_storage.get_target_weights(src_name=weights_src.name,
                                                                 weights_postfix=weights_src.postfix,
                                                                 filters=self.filters,
                                                                 output_df_format=self.weights_format)
            weights_src_postfix = weights_src.postfix
            if weights_src_postfix is None:
                weights_src_postfix = "_actual_postfix"
            if len(weights) == 0:
                print(colorstr('yellow', f"{len(weights)} weights for {weights_src.name}{weights_src_postfix}"))
            else:
                print(colorstr('blue', f"{len(weights)} weights for {weights_src.name}{weights_src_postfix} were found"))
            self.first_weights = pd.concat([self.first_weights, weights], axis='rows')

        #  second weights
        for weights_src in self.second_weights_curve_src:
            weights = self.src_weight_storage.get_target_weights(src_name=weights_src.name,
                                                                 weights_postfix=weights_src.postfix,
                                                                 filters=self.filters,
                                                                 output_df_format=self.weights_format)
            weights_src_postfix = weights_src.postfix
            if weights_src_postfix is None:
                weights_src_postfix = "_actual_postfix"

            if len(weights) == 0:
                print(colorstr('yellow', f"{len(weights)} weights for {weights_src.name}{weights_src_postfix}"))
            else:
                print(colorstr('blue', f"{len(weights)} weights for {weights_src.name}{weights_src_postfix} were found"))
            self.second_weights = pd.concat([self.second_weights, weights], axis='rows')

        houses_df = self.get_houses(self.filters)

        self.first_weights = self.match_device_info(self.first_weights, houses_df)
        self.second_weights = self.match_device_info(self.second_weights, houses_df)

        self.first_weights = self.first_weights.drop_duplicates(
            subset=self.weights_format.house_index.get_columns()+[self.weights_format.age],
            keep='last')

        self.second_weights = self.second_weights.drop_duplicates(
            subset=self.weights_format.house_index.get_columns()+[self.weights_format.age],
            keep='last')

        self.first_weights = self.weights_format.convert_df_types(self.first_weights)
        self.second_weights = self.weights_format.convert_df_types(self.second_weights)

        collected_weights = pd.concat([self.first_weights, self.second_weights], ignore_index=True)
        collected_weights = collected_weights.drop_duplicates(
            self.weights_format.house_index.get_columns() + [self.weights_format.age], keep='last'
        )
        collected_weights = collected_weights.sort_values(by=self.weights_format.age)
        collected_weights[self.weights_format.weight_src.src_name] = WEIGHTS_SRC_TYPE['Targets']
        collected_weights[self.weights_format.weight_src.postfix] = np.nan
        return collected_weights

    @staticmethod
    def spline_curves(curve1: pd.Series, curve2: pd.Series,
                      spline_curve: pd.Series,
                      adjust_spline_curve: bool = True) -> (pd.Series, pd.Series):
        """
        Get interpolated between two curves weight curve according to spline curve,
        the more spline curve coef, the more impact of curve1

        :param curve1: first weight curve
        :param curve2: second weight curve
        :param spline_curve: spline coefs curve
        :param adjust_spline_curve: if true, stretch spline_curve, if False, add last spline_curve value
               till max curve 1 index
        :return: interpolated (splined) weight curve
        """
        # Adjust spline_curve for cycle len
        max_age = max(int(max(curve1.index)), int(max(curve2.index)))
        spline_curve_adj = pd.Series([spline_curve.iloc[-1]] * (max_age+1), dtype=float)

        if adjust_spline_curve:

            print(f"adjust_spline_curve: max_age = {max_age}")
            spline_curve_adj_tmp = np.interp(np.linspace(0, len(spline_curve), max_age+1), spline_curve.index,
                                             spline_curve)
            spline_curve_adj = spline_curve_adj_tmp
        else:
            min_curve_age = min(int(max(spline_curve.index)), int(max(spline_curve_adj.index)))
            spline_curve_adj.iloc[:min_curve_age+1] = spline_curve[:min_curve_age+1]

        #  calculating final weight curve
        final_adj_weights = curve1 * spline_curve_adj + curve2 * (1.0 - spline_curve_adj)

        return final_adj_weights, spline_curve_adj

    @staticmethod
    def plot(src_data_1: pd.Series, src_data_2: pd.Series,
             src_manual_data_1: Optional[pd.Series], src_manual_data_2: Optional[pd.Series],
             combined_data: pd.Series,
             spline_curve: pd.Series,
             title: str,
             vis: bool,
             save_fname: Optional[str]):
        """
        Plot curves

        :param src_data_1: first curve weights
        :param src_data_2: second curve weights
        :param combined_data: final curve weights
        :param spline_curve: spline coefs
        :param title: fig title
        :param vis: if true, plt.show()
        :param save_fname: fname to save fig (.png)
        :return: None
        """

        plt.figure()
        plt.subplot(311)

        # plt.plot(std_weights.index, std_weights['Weights'], label='standard')

        plt.plot(src_data_1.index, src_data_1, label=src_data_1.name, )
        if src_manual_data_1 is not None:
            plt.scatter(src_manual_data_1.index, src_manual_data_1, s=35)

        plt.plot(src_data_2.index, src_data_2, label=src_data_2.name)
        if src_manual_data_2 is not None:
            plt.scatter(src_manual_data_2.index, src_manual_data_2, s=15)
        # plt.scatter(src_data_2.index, src_data_2, s=15)

        plt.title("weight curves")
        plt.legend()

        plt.subplot(312)
        plt.plot(spline_curve.index, spline_curve, label='spline curve')
        plt.title("spline coefs")

        plt.subplot(313)
        plt.plot(combined_data.index, combined_data, label='final')
        if src_manual_data_1 is not None:
            plt.scatter(src_manual_data_1.index, src_manual_data_1, s=35)
        if src_manual_data_2 is not None:
            plt.scatter(src_manual_data_2.index, src_manual_data_2, s=15)
        plt.legend()
        plt.title("final curve")

        fig_label = title
        plt.suptitle(fig_label)
        plt.tight_layout()

        if save_fname is not None:
            plt.savefig(save_fname)

        if vis:
            plt.show()

    def combine(self) -> pd.DataFrame:

        # Common columns names
        weights_column = self.weights_format.weight.weight
        age_column = self.weights_format.weight.age

        # Divide weights by client groups
        first_weights_groups = self.first_weights.groupby(standards_match_columns)
        second_weights_groups = self.second_weights.groupby(standards_match_columns)

        # init output df
        df_output = pd.DataFrame(columns=self.first_weights.columns)

        # Iterate by client groups as each client group has its own Standard weight curve
        for (client_label_1, first_group), (client_label_2, second_group) in zip(first_weights_groups,
                                                                                 second_weights_groups):
            assert client_label_1 == client_label_2

            # Get standard weight curve for client group
            client_params = {}
            for i, c in enumerate(standards_match_columns):
                client_params[c] = client_label_1[i]

            if self.extrapolation_params.use_default_standard:
                std_weights_df = self.actual_info_storage.get_default_weights_standard()
            else:
                std_weights_df = self.actual_info_storage.get_actual_weights_standard(**client_params)
                if std_weights_df is None:
                    std_weights_df = self.actual_info_storage.get_default_weights_standard()
            standards = convert_to_kg(std_weights_df['Weights'])
            # Divide client weights by house groups
            house_first_groups = first_group.groupby(house_match_columns)
            house_second_groups = second_group.groupby(house_match_columns)

            # Iterate by house groups to generate likely curve for two weigh sources group and combine them
            # with spline curve
            for (house_label_1, house_first_group), (house_label_2, house_second_group) in zip(house_first_groups,
                                                                                               house_second_groups):
                assert house_label_1 == house_label_2

                house_first_data = house_first_group.set_index(age_column)[weights_column]
                house_first_data.name = f"{house_label_1} {self.first_weights_curve_label}"
                house_second_data = house_second_group.set_index(age_column)[weights_column]
                house_second_data.name = f"{house_label_2} {self.second_weights_curve_label}"

                house_standards = standards.loc[:max(house_first_data.index.max(), house_second_data.index.max())+1]
                if len(house_first_data) < 2:
                    print(f'!!!! NOT ENOUGTH DATA FOR {house_first_data.name}')
                    if len(house_second_data) < 2:
                        print(f'!!!! NOT ENOUGTH DATA FOR {house_second_data.name}')
                        continue
                    print(f'Only  {self.second_weights_curve_label} will be used')
                    house_first_data = house_second_data
                elif len(house_second_data) < 2:
                    print(f'!!!! NOT ENOUGTH DATA FOR {house_second_data.name}')
                    if len(house_first_data) < 2:
                        print(f'!!!! NOT ENOUGTH DATA FOR {house_first_data.name}')
                        continue
                    print(f'Only  {self.first_weights_curve_label} will be used')
                    house_second_data = house_first_data

                first_adj_weights = adjust_standard_to_values(house_standards,
                                                              house_first_data,
                                                              **self.extrapolation_params.__dict__
                                                              )
                first_adj_weights.name = self.first_weights_curve_label.upper()
                second_adj_weights = adjust_standard_to_values(house_standards,
                                                               house_second_data,
                                                               **self.extrapolation_params.__dict__
                                                               )
                second_adj_weights.name = self.second_weights_curve_label.upper()

                combined_weights, spline_curve_adj = self.spline_curves(first_adj_weights, second_adj_weights,
                                                                        spline_curve=self.spline_curve,
                                                                        adjust_spline_curve=self.adjust_spline_curve)

                combined_df = pd.concat([house_first_group, house_second_group])
                combined_df = combined_df.drop_duplicates(
                    subset=house_match_columns + [age_column]
                )
                combined_df[weights_column] = combined_weights[combined_df[age_column]].values

                df_output = pd.concat([df_output, combined_df])

                # visualize
                if self.vis:
                    self.plot(first_adj_weights,
                              second_adj_weights,
                              house_first_data,
                              house_second_data,
                              combined_data=combined_weights,
                              spline_curve=spline_curve_adj,
                              vis=True,
                              title=str(house_label_1),
                              save_fname=None)

        age_column = self.weights_format.weight.age
        index_cols = self.weights_format.house_index.get_columns() + [age_column]
        df_output = df_output.sort_values(by=index_cols)
        df_output = df_output.dropna(subset=[age_column])
        df_output[self.weights_format.weight_src.src_name] = WEIGHTS_SRC_TYPE['Targets']
        df_output[self.weights_format.weight_src.postfix] = np.nan
        df_output = self.weights_format.convert_df_types(df_output)
        return df_output
