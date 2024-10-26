import os
from typing import Union, Tuple, AnyStr, Optional
import copy

from brddb.utils.common import colorstr

from bdm2.constants.global_setup.data import WEIGHTS_SRC_TYPE
from bdm2.constants.global_setup.server_paths import actual_engines_info_path
from bdm2.data_handling.generated_data.chicken_weights.targets.targets_generators.components import SLTManager
from bdm2.data_handling.generated_data.common_components import manual_weights_manager
from bdm2.data_handling.generated_data.manual_weights_manager import get_all_manual_weights, get_all_adjusted_weights
from bdm2.data_handling.generated_data.standard.components import standards_manager
from bdm2.data_handling.generated_data.standard.components.standards_manager import get_actual_target_weights_postfix
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.slt_data_stuct import SLT_DATA_COLUMNS
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.postgres_actual_clients_info_storage import \
    PostgresActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.devices_storage import DevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.target_weights_storage import TargetWeightsStorage, \
    TargetWeightsColumnsNew

# manual_weights_manager

# from BIRDOO_IP import manual_weights_manager, BirdooUtils, SLTManager, standards_manager

import pandas as pd
import warnings


class LocalTargetWeightsStorage(TargetWeightsStorage):
    """
    Chicken weights storage on local server. Weights information stored in different files

    """

    def __init__(self,
                 device_storage: DevicesStorage,
                 units: str,
                 use_slt_timetable_for_slt: bool = False,
                 src_fname: str = actual_engines_info_path
                 ):

        TargetWeightsStorage.__init__(self, units, actual_info_storage=PostgresActualClientsInfoStorage())
        self._inner_format = TargetWeightsColumnsNew()
        self.device_storage = device_storage
        self.use_slt_timetable_for_slt = use_slt_timetable_for_slt  # Otherwise use PIWFHA.csv

    @property
    def inner_format(self) -> TargetWeightsColumnsNew:
        return TargetWeightsColumnsNew(**copy.deepcopy(self._inner_format.__dict__))

    def __get_manual_weights(self,
                             weights_postfix: Union[str, None],
                             filters: Filter) -> pd.DataFrame:
        """
        Collect all weights from Manuals{weights_postfix}.xlsx,
        Used for collecting DOC, Farmers, Targets
        if weights_postfix is None, will get actual TARGET weights postfix,
        as DOC and Farmers has always the same postfix (_Mahender_raw)

        Convert collected data to self._weights_format

        .. note::
            PLS, if want to get DOC or Farmers, specify weights_postfix as **_Mahender_raw**

        :param weights_postfix:
        :param filters:
        :return:
        """

        df_output = pd.DataFrame()
        target_devices = self.device_storage.get_houses(filters=filters)

        if len(target_devices) == 0:
            print(colorstr('red', f"NO devices after applying filters! CHECK FILTERS!!"))

        farm_column = self.device_storage.output_default_format.farm_name
        client_column = self.device_storage.output_default_format.client_name

        # s = target_devices[[farm_column, client_column]].drop_duplicates()
        for (client, farm), _ in target_devices.groupby([client_column, farm_column]):
            print(f"{farm}")
            farm_filters = copy.deepcopy(filters)
            farm_filters.clients = [client]
            farm_filters.farms = [farm]

            farm_weights_postfix = weights_postfix
            if farm_weights_postfix is None:
                farm_weights_postfix = get_actual_target_weights_postfix(client)
                if farm_weights_postfix is None:
                    print(colorstr('red', f"Warning! NO actual weights_postfix for {farm}"))
                    continue
                print(colorstr('blue', f"Warning! weights_postfix for {farm} was set as "
                                       f"actual_target_weights_postfix {farm_weights_postfix}"))

            tmp_df = get_all_manual_weights(client=farm,
                                            manual_postfix=farm_weights_postfix,
                                            filters=farm_filters,
                                            units=self.units,
                                            weight_postfix_column_name=self._inner_format.weights_postfix)

            df_output = pd.concat([df_output, tmp_df],
                                  ignore_index=True)

        df_output = df_output.rename(columns={
            'weight': self._inner_format.weight.weight,
            'age': self._inner_format.weight.age,
            'daynum': self._inner_format.weight.age
        })

        df_output = self.convert_to_output_format(df_output, target_format=self._inner_format)
        return df_output

    def __get_likely_weights(self,
                             weights_postfix: Union[str, None],
                             filters: Filter) -> pd.DataFrame:
        """
        Return Likely weight

        Convert collected data to self._weights_format

        :param weights_postfix:
        :param filters:
        :return:
        """

        df_output = pd.DataFrame()
        target_devices = self.device_storage.get_houses(filters=filters)

        farm_column = self.device_storage.output_default_format.farm_name
        client_column = self.device_storage.output_default_format.client_name

        for (client, farm), _ in target_devices.groupby([client_column, farm_column]):

            print(f"{farm}")
            farm_filters = copy.deepcopy(filters)
            farm_filters.clients = [client]
            farm_filters.farms = [farm]

            farm_weights_postfix = weights_postfix
            if farm_weights_postfix is None:
                farm_weights_postfix = get_actual_target_weights_postfix(client)
                if farm_weights_postfix is None:
                    print(colorstr('red', f"Warning! NO actual weights_postfix for {farm}"))
                    continue
                print(colorstr('blue', f"Warning! weights_postfix for {farm} was set as "
                                       f"actual_target_weights_postfix {farm_weights_postfix}"))

            df_output = pd.concat([df_output,
                                   get_all_adjusted_weights(client=farm,
                                                            manual_postfix=farm_weights_postfix,
                                                            filters=farm_filters,
                                                            units=self.units,
                                                            weight_postfix_column_name=self._inner_format.weights_postfix)],
                                  ignore_index=True)

        df_output = df_output.rename(columns={
            'weight': self._inner_format.weight.weight,
            'age': self._inner_format.weight.age,
            'daynum': self._inner_format.weight.age,
        })

        df_output = self.convert_to_output_format(df_output, target_format=self._inner_format)
        return df_output

    def __get_slt_weights(self,
                          weights_postfix: Union[str, None],
                          filters: Filter) -> pd.DataFrame:
        """

        :param weights_postfix:
        :param filters:
        :return:
        """

        df_output = pd.DataFrame(columns=SLT_DATA_COLUMNS.get_columns())
        target_devices = self.device_storage.get_houses(filters=filters)

        farm_column = self.device_storage.output_default_format.farm_name
        client_column = self.device_storage.output_default_format.client_name

        for (client, farm), _ in target_devices.groupby([client_column, farm_column]):
            if self.use_slt_timetable_for_slt:
                if weights_postfix is None:
                    weights_postfix = ""
                print('SLT weight will be obtained from SLT timetable')
                slt_df = SLTManager.load_slt_table(farm, filters, filename_postfix=weights_postfix)
            else:
                if weights_postfix is None:
                    weights_postfix = standards_manager.get_actual_PIWFHA_weights_postfix(client)
                piwfha_fname = SLTManager.get_piwfha_filename(farm, weights_postfix)
                print(f'SLT weight will be obtained from {piwfha_fname}')
                slt_df = SLTManager.load_piwfha_table(farm, filters, filename_postfix=weights_postfix)
                if slt_df.empty:
                    print(colorstr('red', f'WARNING! AS no data in {piwfha_fname} '
                                          f'will try to get info from SLT timetable'))
                    slt_df = SLTManager.load_slt_table(farm, filters, filename_postfix=weights_postfix)

            if slt_df.empty:
                continue

            # add to output df
            df_output = pd.concat([df_output, slt_df])

        df_output = df_output[SLT_DATA_COLUMNS.house_index.get_columns() + [SLT_DATA_COLUMNS.slt_timetable.slt_age,
                                                                            SLT_DATA_COLUMNS.slt_weight]]
        df_output = df_output.rename(columns={
            SLT_DATA_COLUMNS.slt_weight: self._inner_format.weight.weight,
            SLT_DATA_COLUMNS.slt_timetable.slt_age: self._inner_format.weight.age
        })
        if df_output.empty:
            return df_output

        df_output[self._inner_format.weights_postfix] = weights_postfix
        df_output = df_output[~df_output[self._inner_format.weight_value].isnull()]
        return df_output

    def __get_piwfha_weights(self,
                             weights_postfix: Union[str, None],
                             filters: Filter) -> pd.DataFrame:
        """

        :param weights_postfix:
        :param filters:
        :return:
        """

        df_output = pd.DataFrame()
        target_devices = self.device_storage.get_houses(filters=filters)
        farm_column = self.device_storage.output_default_format.farm_name
        client_column = self.device_storage.output_default_format.client_name
        s = target_devices[[farm_column, client_column]].drop_duplicates()
        for target_devices_item in s.iterrows():
            target_devices_item = target_devices_item[1]
            farm = target_devices_item[farm_column]
            client = target_devices_item[client_column]

            farm_weights_postfix = weights_postfix
            if farm_weights_postfix is None:
   
                farm_weights_postfix = standards_manager.get_actual_PIWFHA_weights_postfix(client)

            piwfha_df = SLTManager.load_piwfha_table(farm, filters, filename_postfix=farm_weights_postfix)
            if piwfha_df.empty:
                continue

            piwfha_df[self._inner_format.weights_postfix] = farm_weights_postfix
            # add to output df
            df_output = pd.concat([df_output, piwfha_df], ignore_index=True)

        if df_output.empty:
            return df_output
        df_output = df_output[SLT_DATA_COLUMNS.house_index.get_columns() +
                              [SLT_DATA_COLUMNS.slt_timetable.slt_age, SLT_DATA_COLUMNS.piwfha_weight,
                               self._inner_format.weights_postfix]]
        df_output = df_output.rename(columns={
            SLT_DATA_COLUMNS.piwfha_weight: self._inner_format.weight.weight,
            SLT_DATA_COLUMNS.slt_timetable.slt_age: self._inner_format.weight.age
        })

        return df_output

    def get_target_weights(self,
                           src_name: str,
                           weights_postfix: Optional[str],
                           filters: Filter,
                           output_df_format: Optional[TargetWeightsColumnsNew] = None) -> pd.DataFrame:

        if output_df_format is None:
            output_df_format = self.output_default_format
        assert src_name in WEIGHTS_SRC_TYPE.keys()

        weights_df = pd.DataFrame()

        if src_name == WEIGHTS_SRC_TYPE['Mahender']:
            print('red', 'WARNING! Mahender weights are deprecated, Farmers will be used instead')
            src_name = WEIGHTS_SRC_TYPE['Farmers']

        if src_name == WEIGHTS_SRC_TYPE['DOC']:
            """
            DOC do not have weights postfix (as always raw information)
            Local DOC weights are stored in _Mahender_raw.xlsx
            """
            if weights_postfix is None:
                weights_postfix = ""
            if weights_postfix != "":
                print(colorstr('red', 'WARNING! weights_postfix will not be used for Mahender. '
                                      '_Mahender_raw used as default in LocalStorage'))
            weights_postfix = ""
            weights_df = self.__get_manual_weights(weights_postfix='_Mahender_raw',
                                                   filters=filters)
            weights_df[self._inner_format.weights_postfix] = weights_postfix
            weights_df[self._inner_format.weights_src_name] = src_name
            # DOC - only 0 age
            if not weights_df.empty:
                weights_df = weights_df[weights_df[self._inner_format.weight.age] == 0]

        elif src_name == WEIGHTS_SRC_TYPE['Farmers']:
            """
            Farmers do not have weights postfix (as always raw information)
            Local Farmers weights are stored in _Mahender_raw.xlsx
            """
            if weights_postfix is None:
                weights_postfix = ""
            if weights_postfix != "":
                print(colorstr('red', 'WARNING! weights_postfix will not be used for Mahender. '
                                      '_Mahender_raw used as default in LocalStorage'))
            weights_postfix = ""
            weights_df = self.__get_manual_weights(
                weights_postfix="_Mahender_raw",
                filters=filters)
            weights_df[self._inner_format.weights_postfix] = weights_postfix
            weights_df[self._inner_format.weights_src_name] = src_name

            # Mahender - all except 0 age (that is DOC)
            if not weights_df.empty:
                weights_df = weights_df[weights_df[self._inner_format.weight.age] != 0]

        # SLT weights are stored in SLT timetable if .xlsx
        elif src_name == WEIGHTS_SRC_TYPE['SLT']:
            """
            SLT do not have weights postfix (as always raw information) but can be stored in PIWFHA file, 
            that has postfix
            Local SLT weights are stored in SLT timetables or PIWFHA files
            """
            if weights_postfix is None:
                weights_postfix = ""

            get_weights_postfix = weights_postfix

            weights_df = self.__get_slt_weights(
                filters=filters,
                weights_postfix=get_weights_postfix)
            if weights_postfix != "":
                weights_postfix = ""
                print(colorstr('red', f'WARNING! weights_postfix was set to "", '
                                      f'but data was obtained for get_weights_postfix = {get_weights_postfix} '))
            weights_df[self._inner_format.weights_postfix] = weights_postfix
            weights_df[self._inner_format.weights_src_name] = src_name

            # bad_slt_data = weights_df[~(~pd.isnull(weights_df[self._weights_format.weight.age]) * ~pd.isnull(
            #     weights_df[self._weights_format.weight.weight]))]
            bad_slt_data = weights_df[pd.isnull(weights_df[self._inner_format.weight.age])]

            for farm, farm_g in bad_slt_data.groupby(self._inner_format.farm):
                cycles_str = ", ".join(farm_g[self._inner_format.cycle].unique())
                print(f"{farm} has empty slt_age or slt_weight\n"
                      f"Check {cycles_str}")
                print(f"Check {SLTManager.get_slt_timetable_filename(client=farm, filename_postfix='')}")

        elif src_name == WEIGHTS_SRC_TYPE['PIWFHA']:
            weights_df = self.__get_piwfha_weights(
                filters=filters,
                weights_postfix=weights_postfix)
            weights_df[self._inner_format.weights_src_name] = src_name

        elif src_name == WEIGHTS_SRC_TYPE['Likely'] or src_name == WEIGHTS_SRC_TYPE['Likely_targets']:
            weights_df = self.__get_likely_weights(
                weights_postfix=weights_postfix,
                filters=filters)
            weights_df[self._inner_format.weights_src_name] = src_name

        elif src_name == WEIGHTS_SRC_TYPE['Manuals'] or src_name == WEIGHTS_SRC_TYPE['Targets']:
            # Targets = [DOC + PIWFHA + Corrected farmers ]
            weights_df = self.__get_manual_weights(filters=filters,
                                                   weights_postfix=weights_postfix)
            weights_df[self._inner_format.weights_src_name] = src_name

        else:
            print(f"No ways of obtaining {src_name}{weights_postfix} information defined")
            return weights_df
        initial_size = len(weights_df)
        if weights_df.empty:
            weights_df = pd.DataFrame(columns=self._inner_format.get_columns())

        weights_df = weights_df.dropna(subset=[self._inner_format.weight.age, self._inner_format.weight.weight])
        if len(weights_df) != initial_size:
            warnings.warn(
                f'Not all loaded data has not null {self._inner_format.weight.age} or {self._inner_format.weight.weight}')

        weights_df = self.convert_to_output_format(weights_df, target_format=output_df_format)

        weights_df = filters.filter_res_df_csv(weights_df, age_col=output_df_format.age)
        # weights_df = weights_df.loc[weights_df[output_df_format.weight.age] >= 0]
        if weights_df.empty:
            return pd.DataFrame(columns=output_df_format.get_columns())

        if self.units == WEIGHTS_UNITS['kg']:
            weights_df[output_df_format.weight.weight] = manual_weights_manager.convert_to_kg(
                weights_df.set_index(output_df_format.weight.age)[
                    output_df_format.weight.weight]).values

        elif self.units == WEIGHTS_UNITS['g']:
            weights_df[output_df_format.weight.weight] = manual_weights_manager.convert_to_g(
                weights_df.set_index(output_df_format.weight.age)[
                    output_df_format.weight.weight]).values

        weights_df = output_df_format.convert_df_types(weights_df)
        return weights_df

    def convert_to_input_format(self,
                                df: pd.DataFrame,
                                src_format: TargetWeightsColumnsNew) -> pd.DataFrame:

        union_columns = list(set(src_format.get_columns()).intersection(set(df.columns)))
        df_output = pd.DataFrame(columns=src_format.get_columns())
        df_output = pd.concat([df_output, df[union_columns]], ignore_index=True)
        df_output = src_format.convert_df_types(df_output)
        return df_output

    def convert_to_output_format(self,
                                 df: pd.DataFrame,
                                 target_format: TargetWeightsColumnsNew) -> pd.DataFrame:

        df_full = pd.DataFrame(columns=self._inner_format.get_columns())
        df_full = pd.concat([df_full, df])
        df_full = df_full[self._inner_format.get_columns()]

        df_output = pd.DataFrame(df_full.values, columns=target_format.get_columns())

        df_output = target_format.convert_df_types(df_output)
        return df_output

    def update_target_weights(self,
                              weights_df: pd.DataFrame,
                              input_df_format: TargetWeightsColumnsNew,
                              **kwargs
                              ):

        assert input_df_format.weights_src_name in weights_df.columns
        assert input_df_format.weights_postfix in weights_df.columns

        # assert src_name in WEIGHTS_SRC_TYPE.keys()
        weights_df_converted = self.convert_to_input_format(weights_df, input_df_format)
        for (src_name, weights_postfix), src_weights_df in weights_df.groupby([input_df_format.weight_src.src_name,
                                                                               input_df_format.weight_src.postfix]):
            # save to Manuals.xlsx
            if src_name in [WEIGHTS_SRC_TYPE['Mahender'],
                            WEIGHTS_SRC_TYPE['DOC'],
                            WEIGHTS_SRC_TYPE['Manuals'],
                            WEIGHTS_SRC_TYPE['Farmers'],
                            WEIGHTS_SRC_TYPE['Targets']
                            ]:

                for farm, farm_group in weights_df_converted.groupby(input_df_format.farm):
                    if src_name in [WEIGHTS_SRC_TYPE['Mahender'], WEIGHTS_SRC_TYPE['DOC'], WEIGHTS_SRC_TYPE['Farmers']]:
                        save_fname = manual_weights_manager.get_manual_weights_filename(farm, "_Mahender_raw")
                        existed_df = manual_weights_manager.get_all_manual_weights(farm, "_Mahender_raw")
                    else:
                        save_fname = manual_weights_manager.get_manual_weights_filename(farm, weights_postfix)
                        existed_df = manual_weights_manager.get_all_manual_weights(farm, weights_postfix)

                    df_to_dump = pd.concat([existed_df, farm_group],
                                           ignore_index=True).drop_duplicates(
                        subset=self._inner_format.house_index.get_columns() + [self._inner_format.weight.age],
                        keep='last')
                    manual_weights_manager.save_manual_data(df_to_dump, save_fname, round=self.round, units=self.units)
                    print(f'\nManual weights for {farm} were saved to {save_fname}')

            elif src_name in [WEIGHTS_SRC_TYPE['Likely'], WEIGHTS_SRC_TYPE['Likely_targets']]:
                for farm, farm_group in weights_df_converted.groupby(input_df_format.farm):
                    farm = str(farm)
                    save_folder = manual_weights_manager.get_adjusted_weights_folder(farm, weights_postfix)
                    for (cycle, house), cycle_group in farm_group.groupby(
                            [input_df_format.cycle, input_df_format.house]):
                        save_fname = os.path.join(save_folder,
                                                  manual_weights_manager.generate_fname_for_adjusted_weights(farm,
                                                                                                           cycle,
                                                                                                           house)
                                                  )
                        manual_weights_manager.save_adjusted_weights(
                            cycle_group.set_index(self._inner_format.weight.age)[self._inner_format.weight.weight],
                            save_fname,
                            round=self.round,
                            units=self.units)
                        print(f'\nLikely weights for {farm} were saved to {save_fname}')
                    union = pd.pivot(farm_group, index=input_df_format.age,
                                     columns=[input_df_format.cycle, input_df_format.house],
                                     values=input_df_format.weight_value)
                    union_fname = f"{farm}_standards.xlsx"
                    union.to_excel(os.path.join(save_folder, union_fname))
            else:
                warnings.warn(f"WARNING! No update function implement for {src_name}")

    def delete_target_weights(self,
                              src_name: str,
                              weights_postfix: str,
                              filters: Filter,
                              **kwargs):
        if src_name in [WEIGHTS_SRC_TYPE['Mahender'],
                        WEIGHTS_SRC_TYPE['DOC'],
                        WEIGHTS_SRC_TYPE['Manuals'],
                        WEIGHTS_SRC_TYPE['Farmers'],
                        WEIGHTS_SRC_TYPE['Targets']]:
            # define devices space to delete
            houses_to_delete = self.device_storage.get_houses(filters)
            weights_storage_format = self.output_default_format
            columns_to_compare = weights_storage_format.house_index.get_columns() + [weights_storage_format.age]
            # go only through farms that are in device space to delete
            for farm, _ in houses_to_delete.groupby(self.device_storage.output_default_format.farm_name):
                farm = str(farm)
                # define right file postfixes
                if src_name in [WEIGHTS_SRC_TYPE['Mahender'], WEIGHTS_SRC_TYPE['DOC'], WEIGHTS_SRC_TYPE['Farmers']]:
                    save_fname = manual_weights_manager.get_manual_weights_filename(farm, "_Mahender_raw")
                    existed_df = manual_weights_manager.get_all_manual_weights(farm, "_Mahender_raw")
                else:
                    save_fname = manual_weights_manager.get_manual_weights_filename(farm, weights_postfix)
                    existed_df = manual_weights_manager.get_all_manual_weights(farm, weights_postfix)
                # define data to be deleted
                df_to_delete = filters.filter_res_df_csv(existed_df, age_col='age')
                if df_to_delete.empty:
                    continue
                # get difference by  weights_storage_format.house_index.get_columns() + [weights_storage_format.age]
                df_to_dump = pd.concat([existed_df, df_to_delete], ignore_index=True)
                df_to_dump = df_to_dump.drop_duplicates(subset=columns_to_compare, keep=False)

                manual_weights_manager.save_manual_data(df_to_dump, save_fname, round=self.round, units=self.units)
                print(f'Manual weights for {farm} were saved to {save_fname}')
        elif src_name in [WEIGHTS_SRC_TYPE['Likely'],
                          WEIGHTS_SRC_TYPE['Likely_targets']]:  # define devices space to delete
            houses_to_delete = self.device_storage.get_houses(filters)
            weights_storage_format = self.output_default_format
            columns_to_compare = weights_storage_format.house_index.get_columns() + [weights_storage_format.age]
            # go only through farms that are in device space to delete
            for farm, farm_group in houses_to_delete.groupby(self.device_storage.output_default_format.farm_name):
                farm = str(farm)
                save_folder = manual_weights_manager.get_adjusted_weights_folder(farm, weights_postfix)
                for (cycle, house), cycle_group in farm_group.groupby([weights_storage_format.cycle,
                                                                       weights_storage_format.house]):
                    likely_weights_fname = os.path.join(save_folder,
                                                        manual_weights_manager.generate_fname_for_adjusted_weights(farm,
                                                                                                                 cycle,
                                                                                                                 house)
                                                        )
                    if os.path.exists(likely_weights_fname):
                        os.remove(likely_weights_fname)
                        print(f'Likely weights for {farm} {cycle} {house} were deleted')
        else:
            print(colorstr('red', 'bold',
                           f"No delete function implement for {src_name} in {self.__class__.__name__}"))
        return 0
