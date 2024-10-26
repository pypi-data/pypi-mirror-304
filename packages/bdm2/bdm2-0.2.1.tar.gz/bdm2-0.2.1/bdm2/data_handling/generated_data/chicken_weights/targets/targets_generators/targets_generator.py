#  Copyright (c) Anna Sosnovskaya

from abc import abstractmethod, ABC
from typing import Optional, List, Iterable
from dataclasses import dataclass

# for saving figures
import matplotlib.pyplot as plt
import os
from bdm2.constants.global_setup.data import max_age, house_match_columns
import pandas as pd
from brddb.utils.common import colorstr

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE, standards_match_columns
from bdm2.data_handling.generated_data.common_components import manual_weights_manager
from bdm2.data_handling.generated_data.manual_weights_manager import get_adjusted_weights_folder, convert_to_kg
from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.utils.process_data_tools.components.birdoo_filter import init_filter_from_devices, Filter
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import get_rename_dict, ActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage, \
    TargetWeightsColumnsNew




def save_figures(targets_df: pd.DataFrame,
                 likely_df: pd.DataFrame,
                 weights_format: TargetWeightsColumnsNew,
                 device_storage: DevicesStorage,
                 actual_info_storage: ActualClientsInfoStorage,
                 weights_postfix: str,
                 vis: bool
                 ):
    target_generator = targets_df.groupby(weights_format.house_index.get_columns())
    likely_generator = likely_df.groupby(weights_format.house_index.get_columns())
    for house_label, house_group in target_generator:
        # client_info = pd.merge(house_group.iloc[:1], devices, on=devices_format.house_index.get_columns())
        house_s = pd.Series(house_label, index=weights_format.house_index.get_columns())
        if house_label not in likely_generator.indices:
            print(colorstr('yellow', f'WARNING No likely weights were generated for {house_label}'))
            continue
        likely_group = likely_generator.get_group(house_label)

        client_info = house_group[standards_match_columns].iloc[0]

        standard = actual_info_storage.get_actual_weights_standard(client_info['client'],
                                                                   client_info['breed_type'],
                                                                   client_info['gender'])
        default_standard = actual_info_storage.get_default_weights_standard()

        plt.figure()
        if standard is not None:
            plt.plot(standard["Weights"], label="standard", c="orange")
        if default_standard is not None:
            plt.plot(default_standard["Weights"], label="default standard", c="lime")
        plt.plot(likely_group['age'].values, likely_group['weight'].values, label="Likely", c="blue")
        plt.scatter(house_group['age'].values, house_group['weight'].values, label="Manual", c="blue")

        title = f"{house_label}"
        plt.title(title)
        plt.ylim(0,6)
        plt.legend()

        dst_dir = get_adjusted_weights_folder(house_s.farm, weights_postfix)
        if not os.path.exists(dst_dir + "\\figs"):
            os.makedirs(dst_dir + "\\figs")
        save_fname = dst_dir + "\\figs\\" + f"fig_{house_s.farm}_{house_s.cycle}_{house_s.house}.png"
        plt.savefig(save_fname)
        print(f"figure is saved to {save_fname}")

        if vis:
            plt.show()
        plt.close()
        pass


@dataclass
class WeightSrc:
    """
    Structure for defining weights sources

    """
    name: str
    postfix: Optional[str]


class TargetsCombiner:
    """
    Class for collecting, analysing and combining src weight to target weights

    """

    @dataclass
    class LikelyConfig:
        """
        Settings for generating likely weights with BIRDOO_IP.BirdooUtils.adjust_standard_to_values

        """
        vis: bool

        max_age: Optional[int] = max_age  # if None, will use full standard length
        smooth_window: int = 1
        useFirstStandardValue: bool = True
        useLastStandardValue: False = False
        average: int = 1
        use_default_standard: bool = True

    def __init__(self,
                 src_devices_storage: DevicesStorage,
                 src_weight_storage: TargetWeightsStorage,
                 actual_info_storage: ActualClientsInfoStorage,
                 filters: Optional[Filter] = None
                 ):
        """

        :param src_devices_storage: device info storage to obtain clients, cycle, breed type, gender info
        :param src_weight_storage: weight info storage
        :param filters: define devices scope to work

        """
        self.src_devices_storage = src_devices_storage
        self.src_weight_storage = src_weight_storage
        self.actual_info_storage = actual_info_storage
        self.weights_format = TargetWeightsColumnsNew()
        self.filters = filters

    def get_houses(self, filters: Filter) -> pd.DataFrame:
        houses_df = self.src_devices_storage.get_houses(filters)
        rd = get_rename_dict(self.src_devices_storage.output_default_format.house_index,
                             self.src_weight_storage.output_default_format.house_index)
        rd[self.src_devices_storage.output_default_format.client_name] = 'client'
        rd[self.src_devices_storage.output_default_format.breed_type] = 'breed_type'
        rd[self.src_devices_storage.output_default_format.gender] = 'gender'
        houses_df = houses_df.rename(columns=rd)
        return houses_df

    @staticmethod
    def match_device_info(weights_df: pd.DataFrame, houses: pd.DataFrame) -> pd.DataFrame:
        """
        Return updated weights_df with house extra info

        :param weights_df:
        :param houses:
        :return:
        """

        #  setting union index
        houses = houses.set_index(house_match_columns)
        weights_df_output = weights_df.set_index(house_match_columns)

        union_index = list(set(weights_df_output.index).intersection(set(houses.index)))
        if len(union_index) == 0:
            print(colorstr('yellow', f"TargetsCombiner._match_device_info: NO union index of houses df and weight  "))
        weights_df_output = weights_df_output.loc[union_index]

        columns_to_add = list(set(houses.columns).difference(set(weights_df_output.columns)))
        if len(columns_to_add) == 0:
            print(colorstr('yellow', f"TargetsCombiner._match_device_info: NO columns_to_add "))
            return weights_df_output.reset_index()

        weights_df_output = pd.merge(weights_df_output, houses[columns_to_add],
                                     left_index=True, right_index=True,
                                     how='inner')

        weights_df_output = weights_df_output.reset_index()
        return weights_df_output

    @abstractmethod
    def collect(self) -> pd.DataFrame():
        """
        Collect all data from self.src_weight_storage according to class settings

        :return: None, update inner attributes for next combining
        """

    @abstractmethod
    def combine(self) -> pd.DataFrame:
        """
        Used after self.collect(). Aggregate information, obtained during collect and generate combined targets
        Combine all collected data

        .. warning::
            output df postfix = np.nan! Should be defined before save


        :return: combined target weights df with weights_src name = Targets and self.weights_format columns
        """

    def generate_likely(self, df: pd.DataFrame, likely_config: LikelyConfig) -> pd.DataFrame:
        """
        Generate Likely targets weights with weights_src name = Likely_targets from df weight

        :param df: df of weights (obtained after self.combine() or other df with format self.weights_format)
        :param likely_config: settings for generating likely weights
        :return: likely weights df with weights_src name = Likely_targets and self.weights_format columns
        """

        weights_column = self.weights_format.weight.weight
        age_column = self.weights_format.weight.age

        df_output = pd.DataFrame(columns=self.weights_format.get_columns())
        for client_label, client_group in df.groupby(standards_match_columns):
            client_params = {}
            for i, c in enumerate(standards_match_columns):
                client_params[c] = client_label[i]

            if likely_config.use_default_standard:
                std_weights_df = self.actual_info_storage.get_default_weights_standard()
            else:
                std_weights_df = self.actual_info_storage.get_actual_weights_standard(**client_params)
                if std_weights_df is None:
                    std_weights_df = self.actual_info_storage.get_default_weights_standard()
            # _, std_weights_df = StandartsManager.get_standard_weights(**client_params)
            standards = convert_to_kg(std_weights_df['Weights'])

            if (likely_config.max_age is not None) and (standards.index.max() < likely_config.max_age):
                print(colorstr('yellow', f"Standard for {client_label} max index = {standards.index.max()} "
                                         f"< {likely_config.max_age} (config.max_age))"))

            house_groups = client_group.groupby(house_match_columns)

            for house_label, house_groups in house_groups:
                house_data = house_groups.set_index(age_column)[weights_column]
                house_data.name = house_label

                house_data_adj = adjust_standard_to_values(standard=standards,
                                                           initial_values=house_data,
                                                           **likely_config.__dict__)
                if (likely_config.max_age is not None) and (house_data_adj.index.max() > likely_config.max_age):
                    house_data_adj = house_data_adj[:likely_config.max_age]
                house_likely_base = house_groups.iloc[0][self.weights_format.house_index.get_columns()]
                house_likely = pd.DataFrame([house_likely_base] * len(house_data_adj),
                                            columns=self.weights_format.get_columns())

                house_likely[age_column] = house_data_adj.index.values
                house_likely[weights_column] = house_data_adj.values

                df_output = pd.concat([df_output, house_likely])
        df_output[self.weights_format.weight_src.src_name] = WEIGHTS_SRC_TYPE['Likely_targets']
        return df_output

    def save(self, df: pd.DataFrame, storage: TargetWeightsStorage, weights_postfix: str):
        """
        Save weights df to storage. will set  weights_postfix from input argument,
        but weights src types will take from df

        :param df: df of weights (obtained after self.combine() or other df with format self.weights_format)
        :param storage: storage to be updated
        :param weights_postfix: weights_postfix for weights to be saved
        :return: None
        """
        df_to_save = df.copy()
        df_to_save[self.weights_format.weight_src.postfix] = weights_postfix
        for (src_name, weights_postfix), group in df_to_save.groupby([self.weights_format.weight_src.src_name,
                                                                      self.weights_format.weight_src.postfix]):
            filters = init_filter_from_devices(group)
            storage.delete_target_weights(src_name=src_name, weights_postfix=weights_postfix, filters=filters)

        storage.update_target_weights(df_to_save, self.weights_format)
