import copy
import os.path
import random
import time
import warnings
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import yaml
from pandas.errors import SettingWithCopyWarning

from bdm2.constants.global_setup.data import max_age
from bdm2.constants.global_setup.encoders import GenderEncoder
from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.constants.global_setup.env import EC2_HOST_PROD, EC2_USER_PROD, EC2_KEY_PROD, EC2_ENGINE_FOLDER_PATH_PROD
from bdm2.constants.global_setup.server_paths import statistics_fname, statistics_server_dir
from bdm2.data_handling.generated_data.features_stats.components.calculation.utils import negative_check, \
    out_of_bounds_check, use_interpolation, check_feature_mean_difference
from bdm2.data_handling.generated_data.features_stats.components.common.explicits import proceed_raw_explicits, \
    process_agg_explicits, update_explicit_boundaries, proceed_cloud_explicits
from bdm2.data_handling.generated_data.features_stats.components.common.feature import FeatureColNames
from bdm2.data_handling.generated_data.features_stats.components.common.general import get_dirs_to_files, check_path, \
    SMALL_COMB_IQR_KEY
from bdm2.data_handling.generated_data.features_stats.components.common.helpers import get_regex_or, \
    _explicit_files_glob_pattern, _runnung_stats_explicit_glob_pattern
from bdm2.data_handling.generated_data.features_stats.components.params.features import FeaturesParams
from bdm2.data_handling.generated_data.features_stats.components.params.local import LocalWayParams
from bdm2.data_handling.generated_data.features_stats.components.params.universal import UniversalParams
from bdm2.data_handling.generated_data.standard.components import standards_manager
from bdm2.logger import build_logger
from bdm2.utils.linux.shell_connector import ShellHandler
from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.engine.engine_manager import get_engine_statistics, get_params
from bdm2.utils.process_data_tools.components.res_df.components.file_manager import FilenameManager
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage

warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)  # UserWarning


class StatisticsGenerator:
    def __init__(self,
                 features_params,
                 universal_params,
                 local_way_params,
                 need2use_local_way):
        self.all_features = None
        self.features_params: FeaturesParams = features_params
        self.universal_params: UniversalParams = universal_params
        self.local_way_params: LocalWayParams = local_way_params
        self.need2use_local_way: bool = need2use_local_way
        self.logger = build_logger(file_name=f"{Path(__file__)}", save_log=False)

    def print_all_features(self):
        all_features = self.features_params.geom_group + self.features_params.behaviour_group
        all_features.append(self.features_params.volume_name)
        self.logger.info("input features for generating stats:")
        for beh_feature in self.features_params.behaviour_group:
            self.logger.info("\t{}: {}".format(beh_feature,
                                               "filterable" if self.features_params.settings4behaviour[
                                                   "isFilterable"]
                                               else "not filterable"))

        for beh_feature in self.features_params.geom_group:
            self.logger.info("\t{}: {}".format(beh_feature,
                                               "filterable" if self.features_params.settings4geom["isFilterable"]
                                               else "not filterable"))
        self.logger.warning("\t{}: {}".format(self.features_params.volume_name,
                                              "filterable" if self.features_params.settings4volume["isFilterable"]
                                              else "not filterable"))

        return all_features

    def generate_statistics_from_mean_and_ideal_curve(self,
                                                      engine_cfg: EngineConfig,
                                                      feature: str,
                                                      feature_col,
                                                      filters: Filter,
                                                      n_all_houses_perf_stdevs,
                                                      n_individual_house_stdevs,
                                                      res_df_postfix: str = "",
                                                      count_filter_value: int = 1000, ):
        res_fname = engine_cfg.local_results_dir + "\\" + FilenameManager.get_res_fname(feature,
                                                                                        engine_cfg.get_engine_postfix(),
                                                                                        res_df_postfix)
        self.logger.info(
            f"Using res_df to get temporary ideal stats which may be used for future interpolation (if there will be "
            f"no real data")
        if not os.path.exists(res_fname):
            print("No res_df file {}".format(res_fname))
            return None

        res_df = pd.read_csv(res_fname, sep=";")
        res_df = filters.filter_res_df_csv(res_df)
        prev_len: int = len(res_df)
        self.logger.debug(f"not filtered res_df: {res_df.shape}")
        res_df = res_df[res_df['count'] > count_filter_value]
        self.logger.info(f"res_df after filtering: {res_df.shape}")
        self.logger.info(
            f"removed {prev_len - len(res_df)} lines using res_df['count'] > {count_filter_value};\n" + \
            f"in %: {(prev_len - len(res_df)) / prev_len}")
        feature_statistcis = pd.DataFrame(index=np.arange(0, max_age + 1))
        if f'{feature}_mean' not in res_df.columns:
            print(f"No {feature} in {res_fname}")
            return None

        gender = get_params(engine_cfg.engine_snapshot_dir + "\\" + engine_cfg.main_params_filename,
                            "ObjectQualityEstimatorParams_gender")
        if gender is None:
            raise ValueError(f"Could not defibe gender from engine snapshot in {engine_cfg.local_results_dir}")
        try:
            gender = GenderEncoder.gender_decoder(int(float(gender)))
        except Exception as e:
            print(e)
            return feature_statistcis
        house_perfomance_mean = res_df.groupby('age').mean()[f'{feature}_mean']
        house_perfomance_stdev = res_df.groupby('age').std()[f'{feature}_mean']
        ideal_cv_filename, ideal_cv = StandartsManager.get_ideal_cv_curve_for_gender(gender)
        if ideal_cv is None or ideal_cv.empty:
            print(f"No {ideal_cv_filename} file")
            return feature_statistcis

        individual_house_stdev = house_perfomance_mean * ideal_cv.loc[house_perfomance_mean.index, 'CV']

        # divide on n_individual_house_stdevs as no possibility to set n_stdevs for running filtration
        global_stdev = (
                               n_all_houses_perf_stdevs * house_perfomance_stdev
                               + n_individual_house_stdevs * individual_house_stdev) / n_individual_house_stdevs

        feature_statistcis[feature_col.mean] = house_perfomance_mean
        feature_statistcis[feature_col.std] = global_stdev

        if feature == self.features_params.volume_name:
            will_be_filtered = self.features_params.settings4volume["isFilterable"]
        elif feature in self.features_params.geom_group:
            will_be_filtered = self.features_params.geom_group["isFilterable"]
        else:
            will_be_filtered = self.features_params.behaviour_group["isFilterable"]

        feature_statistcis[f"{feature}_filterable"] = int(will_be_filtered)
        return feature_statistcis

    def get_settings_for_feature(self, feature):
        if feature == self.features_params.volume_name:
            return self.features_params.settings4volume
        elif feature in self.features_params.geom_group:
            return self.features_params.settings4geom
        elif feature in self.features_params.behaviour_group:
            return self.features_params.settings4behaviour

    # @staticmethod
    def _interpolate_stat_df(self, features: List[str], stat_df, spline_order=2, rolling_window=7,
                             min_stdev_percent=0.1) -> pd.DataFrame:
        for feature in features:
            # fill nan
            if feature + "_mean" not in stat_df.columns:
                print(f"{feature} is not in statistics")
                continue
            interpolated_mean = stat_df[feature + "_mean"].interpolate(method='spline', order=spline_order,
                                                                       limit_direction="both")
            # smooth
            interpolated_mean = interpolated_mean.rolling(rolling_window, center=True, min_periods=1).mean()
            stat_df[feature + "_mean"] = interpolated_mean

            stdev_coef = stat_df[feature + "_stdev"] / interpolated_mean
            interpolated_stdev = use_interpolation(stdev_coef,
                                                   spline_order,
                                                   min_stdev_percent,
                                                   interpolated_mean,
                                                   rolling_window)

            stat_df[feature + "_stdev"] = interpolated_stdev

            feature_params = self.get_settings_for_feature(feature)
            if isinstance(feature_params, dict):
                stat_df[feature + "_filterable"] = int(feature_params["isFilterable"])

        return stat_df

    @staticmethod
    def propagate_coefficients(ages: List[int], coefficients: List[float],
                               max_age: int, min_age: int = 0) -> List[float]:

        assert len(ages) == len(coefficients), "Ages and coefficients arrays should have equal length"
        assert all(age >= 0 for age in ages), "Ages should be positive"
        assert all(coeff > 0 for coeff in coefficients), "Coefficients should be positive"
        sorted_ages = sorted(ages)
        assert sorted_ages == ages, "Ages must be sorted"

        result = []
        # first fill container with given coefficient till the first age from min age:
        current_age: int = min_age
        current_coef: float = coefficients[0]
        # for a in range(current_age, ages[0], 1):
        #     result.append(coefficients[0])
        # then iterate over the target rest
        for next_age, next_coef in zip(ages, coefficients):
            age_diff: int = next_age - current_age + 1
            coef_values: np.ndarray = np.linspace(start=current_coef, stop=next_coef, num=age_diff)[:-1]
            result.extend(coef_values.tolist())
            current_age = next_age
            current_coef = next_coef
        # result.append(coefficients[-1])
        # iterate over the last input age till the max:
        for _ in range(current_age, max_age, 1):
            result.append(coefficients[-1])

        assert len(result) == max_age - min_age, f""

        return result

    def define_engine_config_local(self):
        engine_config = EngineConfig()
        engine_config.set_another_engine_version(self.universal_params.engine_postfix,
                                                 self.local_way_params.results_postfix,
                                                 self.universal_params.client)

        assert os.path.exists(engine_config.local_results_dir), f"could not find local result folder!\n" \
                                                                f"{engine_config.local_results_dir}"

        return engine_config

    def set_up_correct_mean_coef(self):
        if type(self.universal_params.mean_coef) == float or type(self.universal_params.mean_coef) == int:
            self.universal_params.mean_coef = [self.universal_params.mean_coef, self.universal_params.mean_coef]
        elif type(self.universal_params.mean_coef) == tuple or type(self.universal_params.mean_coef) == list:
            if len(self.universal_params.mean_coef) == 1:
                self.universal_params.mean_coef = [self.universal_params.mean_coef[0],
                                                   self.universal_params.mean_coef[0]]
            else:
                self.logger.info(f'provided list/tuple {self.universal_params.mean_coef} of mean_coef is ok')
        assert len(
            self.universal_params.mean_coef) == 2, \
            f'Please provide list or tuple of 2 for mean coef since ' \
            f'the first value is used for left coef and the second for the right'

    def get_ages(self):
        if self.universal_params.use_np is True:

            assert len(self.universal_params.ages) in [2, 3], f"Provide ages as two-elements or three " + \
                                                              f"elements array for using numpy arange"
            if len(self.universal_params.ages) == 2:
                return np.arange(self.universal_params.ages[0], self.universal_params.ages[1])
            elif len(self.universal_params.ages) == 3:
                return np.arange(self.universal_params.ages[0], self.universal_params.ages[1],
                                 self.universal_params.ages[2])
            else:
                raise RuntimeError(f"Unknown ages number when using numpy arrange")
        else:
            return self.universal_params.ages

    def get_local_stat(self, engine_config):
        if self.local_way_params.statistics_fname is not None:
            self.logger.info(f"Using statistics from {self.local_way_params.statistics_fname}")
            statistics_df_init = pd.read_csv(self.local_way_params.statistics_fname, sep=None, engine='python')
        else:
            statistics_df_init = get_engine_statistics(engine_config, True)
        return statistics_df_init

    def collect_real_stat_from_local_engine_res(self, engine_config):
        filters = Filter()
        statistics_df = pd.DataFrame()
        for feature in self.all_features:
            self.logger.info(f"Processing {feature}")
            feature_settings = self.get_settings_for_feature(feature)
            # collecting from local
            if not feature_settings["mean_stdev_from_src"]:
                feature_stat = \
                    self.generate_statistics_from_mean_and_ideal_curve(
                        engine_config,
                        feature=feature,
                        filters=filters,
                        n_all_houses_perf_stdevs=self.universal_params.StaticParams.n_all_houses_perf_std,
                        n_individual_house_stdevs=self.universal_params.StaticParams.n_individual_house_std,
                        res_df_postfix=self.local_way_params.res_df_postfix)

                if feature_stat is None:
                    raise FileExistsError(f"feature_stat for {feature} is None")
                statistics_df = pd.concat([statistics_df, feature_stat], axis=1)
        return statistics_df

    def interpolate_stat(self, real_statistics_df, statistics_df_init):
        # SAME IN CLOUD AND LOCAL WAY!
        statistics_df = self._interpolate_stat_df(
            list(self.all_features),
            real_statistics_df,
            spline_order=self.universal_params.StaticParams.spline_order,
            rolling_window=self.universal_params.smooth_window,
            min_stdev_percent=self.universal_params.StaticParams.min_stdev_percent)

        right_side_df = statistics_df_init[
            set(statistics_df_init.columns).difference(set(statistics_df.columns))].copy()
        statistics_df[right_side_df.columns] = right_side_df
        statistics_df.index = right_side_df.index
        return statistics_df.reset_index()

    def set_up_custom_stat_values(self, feature,
                                  feature_col,
                                  statistics_df, statistics_df_init):

        feature_df = statistics_df.filter(regex=(f'.*{feature}.*'))
        if feature_df.empty:
            uniform_range: Tuple[float, ...] = (0.0, 0.01)
            warn_msg: str = f"for feature={feature} there's no values in the standard; filling them with randomly " \
                            f"uniformed values in range {uniform_range}"
            self.logger.error(warn_msg)

            # set mean to 1 and std to 0.01:
            feature_df[feature_col.mean] = 0.01
            statistics_df_init[feature_col.mean] = 0.01
            #
            feature_df[feature_col.std] = 0.30
            statistics_df_init[feature_col.std] = 0.01
            feature_df[feature_col.l_std_coef] = 1.
            statistics_df_init[feature_col.l_std_coef] = 0.01
            feature_df[feature_col.r_std_coef] = 1.
            statistics_df_init[feature_col.r_std_coef] = 0.01
        return feature_df, statistics_df_init

    def use_law(self, feature_df, feature_col, feature):
        if self.local_way_params.law == 'multiplicative':
            # create masks for each case:
            feature_df.loc[:, 'min_feature_mask'] = feature_df['min_feature_from_std'] < (
                    feature_df[feature_col.mean] / self.universal_params.mean_coef[0])
            feature_df.loc[:, 'max_feature_mask'] = feature_df['max_feature_from_std'] > (
                    feature_df[feature_col.mean] * self.universal_params.mean_coef[1])

            feature_df.loc[feature_df['min_feature_mask'],
            feature_col.l_std_coef] = (feature_df[feature_col.mean] -
                                       feature_df[feature_col.mean] /
                                       self.universal_params.mean_coef[0]) / feature_df[
                                          feature_col.std]
            feature_df.loc[feature_df['max_feature_mask'], feature_col.r_std_coef] = (
                                                                                             feature_df[
                                                                                                 feature_col.mean] *
                                                                                             self.universal_params.mean_coef[
                                                                                                 1] -
                                                                                             feature_df[
                                                                                                 feature_col.mean]
                                                                                     ) / feature_df[feature_col.std]

        elif self.local_way_params.law == 'additive':
            # create masks for each case:
            for mean in self.universal_params.mean_coef:
                assert all([mean > 0,
                            mean < 1]) is True, f"all of mean_coef elements when use 'additive' law must be " \
                                                f"between 0 and 1 (!)"
            feature_df.loc[:, 'min_feature_mask'] = feature_df['min_feature_from_std'] < (
                    feature_df[f"{feature}_mean"] * (1 - self.universal_params.mean_coef[0]))
            feature_df.loc[:, 'max_feature_mask'] = feature_df['max_feature_from_std'] > (
                    feature_df[f"{feature}_mean"] * (1 + self.universal_params.mean_coef[1]))

            feature_df.loc[feature_df['min_feature_mask'],
            feature_col.l_std_coef] = (feature_df[feature_col.mean] * (
                self.universal_params.mean_coef[0])) / feature_df[feature_col.std]

            feature_df.loc[feature_df['max_feature_mask'],
            feature_col.r_std_coef] = (feature_df[feature_col.mean] * (
                self.universal_params.mean_coef[1])) / feature_df[feature_col.std]

        else:
            raise ValueError(f"Please provide law for shift calculating either 'multiplicative' or 'additive'")
        return feature_df

    def prepare_feature_process(self,
                                feature, feature_df, feature_col,
                                statistics_df_init, is_filtrable, n_left_stdev, df_output):
        feature_df_to_concat_1 = pd.DataFrame()

        if n_left_stdev is None:
            if feature_df.filter(regex=(f'.*_lstdev_coef')).empty:
                assert n_left_stdev is not None, f"Please provide n_left_stdev value for " + \
                                                 f"{feature} \n or set use_form_src_file to " \
                                                 f"False to use source file from MainConfig"
        else:

            feature_df.loc[:, feature_col.l_std_coef] = n_left_stdev

        feature_df.loc[:, 'min_feature_from_std'] = feature_df[feature_col.mean] - feature_df[
            feature_col.l_std_coef] * feature_df[feature_col.std]

        feature_df.loc[:, 'max_feature_from_std'] = feature_df[feature_col.mean] + feature_df[
            feature_col.r_std_coef] * feature_df[feature_col.std]

        # -------- multiplicative, addictive -----------
        feature_df = self.use_law(feature_df, feature_col, feature)
        # -------- ROUNDING -----------
        feature_df = self.rounding(feature_df, feature_col)

        # -------- some regex check -----------
        all_feature_cols = statistics_df_init.filter(regex=f'.*{feature}.*').columns
        for col in all_feature_cols:
            feature_df_to_concat_1[col] = feature_df[col]

        # check the rest of the columns:
        if statistics_df_init.filter(
                regex=f'{feature}_rstdev.*').empty:  # or feature_df_init.filter(regex=f'{feature.name}_rstdev.*').empty
            feature_df_to_concat_1 = pd.concat(
                [feature_df_to_concat_1, feature_df.filter(regex=f'{feature}_rstdev.*')], axis=1)
        if statistics_df_init.filter(
                regex=f'{feature}_lstdev.*').empty:  # or feature_df_init.filter(regex=f'{feature.name}_lstdev.*').empty
            feature_df_to_concat_1 = pd.concat(
                [feature_df_to_concat_1, feature_df.filter(regex=f'{feature}_lstdev.*')], axis=1)

        # check for isFilterable flag:

        filter_col = f"{feature}_filterable"
        if is_filtrable:
            feature_df_to_concat_1[filter_col] = np.ones(61, dtype=np.int32)
        else:
            feature_df_to_concat_1[filter_col] = np.zeros(61, dtype=np.int32)

        df_output = pd.concat([df_output, feature_df_to_concat_1], axis=1)

        return feature_df, statistics_df_init, df_output

    @staticmethod
    def rounding(feature_df, feature_col: FeatureColNames):
        feature_df.loc[:, feature_col.l_std_coef] = feature_df[
            feature_col.l_std_coef].round(2)
        feature_df.loc[:, feature_col.r_std_coef] = feature_df[
            feature_col.r_std_coef].round(2)
        return feature_df

    def work_with_explicits(self, filters, engine_config, ages):

        # reserve flag:
        loaded_explicit_stats: bool = False
        real_explicit_stats: Optional[pd.DataFrame] = None
        tmp_explicits_fp: Optional[Union[str, Path]] = None

        t0 = time.time()
        # TODO: remove law and iterate over ages and then over features
        self.logger.debug("\n" + '*' * 50 + '\n' + '***** USING DATA TO CALIBRATE STATISTICS *****' + '\n')

        small_combinations_ages: List[int] = self.universal_params.small_combinations_ages
        small_combinations_boundary_shifts: List[int] = self.universal_params.small_combinations_boundary_shifts
        small_comb_bound_shifts_list: List[float] = \
            self.propagate_coefficients(ages=small_combinations_ages,
                                        coefficients=small_combinations_boundary_shifts,
                                        max_age=max_age)
        self.logger.warning(
            f"inserted {small_comb_bound_shifts_list} as a list of "
            f"boundary shifts for small combinations under the {SMALL_COMB_IQR_KEY} kwy")

        if not loaded_explicit_stats:

            filters.clients = [self.universal_params.client]

            devices = PostgresDevicesStorage()
            devices_loc = devices.get_devices(filters)
            uniques = list(devices_loc['cycle'].dropna().unique())
            or_pattern_cycle = get_regex_or(uniques)

            unique_houses = list(devices_loc['house'].dropna().unique())
            or_pattern_house = get_regex_or(unique_houses)
            dirs_to_files = get_dirs_to_files(devices_loc=devices_loc, filters=filters,
                                              main_config=engine_config, logger=self.logger, useRolled=False)
            selected_dirs = [i[0] for i in dirs_to_files]

            if self.universal_params.how == 'raw':
                # todo: ВЕРНУТЬ ТУТ proceed_explicits
                real_explicit_stats, replaced_ages = proceed_raw_explicits(
                    feature_settings=self.features_params,
                    group_by_cols=self.universal_params.StaticParams.gby,
                    boundary_shifts=self.universal_params.small_combinations_boundary_shifts,
                    small_combinations_threshold=self.universal_params.small_combinations_threshold,
                    datapoints_num_thresh=self.local_way_params.datapoints_num_thresh,
                    iqr_boundary_shift=self.universal_params.iqr_boundary_shift,
                    iqr_percentiles=self.universal_params.iqr_percentiles,
                    selected_dirs=selected_dirs,
                    features=self.all_features,
                    or_pattern_cycle=or_pattern_cycle,
                    or_pattern_house=or_pattern_house,
                    _explicit_files_glob_pattern=_explicit_files_glob_pattern,
                    ages=ages, filters=filters,
                    logger=self.logger,
                    devices_slice=devices_loc,
                    main_config=engine_config)

                self.logger.info(
                    f'\nStatistics calculation using data completed in {(time.time() - t0) / 60:.3f} minutes')
                self.logger.warning(
                    f"Individually adapted days: {', '.join([str(i) for i in list(replaced_ages)])}")

            elif self.universal_params.how == 'fast':
                real_explicit_stats, replaced_ages = process_agg_explicits(
                    boundaries=self.universal_params.StaticParams.boundaries,
                    gby=self.universal_params.StaticParams.gby,
                    small_combinations_threshold=self.universal_params.small_combinations_threshold,
                    boundary_shifts=self.universal_params.small_combinations_boundary_shifts,
                    datapoints_num_thresh=self.local_way_params.datapoints_num_thresh,
                    features=self.all_features,
                    features_settings=self.features_params,
                    selected_dirs=selected_dirs,
                    iqr_boundary_shift=self.universal_params.iqr_boundary_shift,
                    iqr_percentiles=self.universal_params.iqr_percentiles,
                    or_pattern_cycle=or_pattern_cycle,
                    or_pattern_house=or_pattern_house,
                    ages=ages,
                    _runnung_stats_explicit_glob_pattern=_runnung_stats_explicit_glob_pattern,
                    logger=self.logger,
                    devices_slice=devices_loc,
                    main_config=engine_config)

            else:
                raise NotImplementedError()

        else:
            real_explicit_stats = pd.read_csv(tmp_explicits_fp, sep=None, engine='python')

        if real_explicit_stats is None:
            raise NotImplementedError(f"Statistics from explicit hasn't been initialized yet")

        return real_explicit_stats, loaded_explicit_stats, tmp_explicits_fp

    def check_and_save_explicit_stat(self, real_explicit_stats,
                                     loaded_explicit_stats,
                                     tmp_explicits_fp):
        real_explicit_stats = real_explicit_stats.sort_values(by=['age'])

        if not loaded_explicit_stats:
            # generate name for the previous file
            new_explicits_fp = check_path(filepath=tmp_explicits_fp,
                                          prefix=datetime.now().strftime("%Y_%m_%d__%H_%M_%S"))

            try:
                old_fp = str(tmp_explicits_fp)
                if old_fp != new_explicits_fp:
                    # rename it
                    os.rename(old_fp, new_explicits_fp)
                    self.logger.info(f"Renamed old file {old_fp} -> {new_explicits_fp}; can be used for debug")
                # save at different path:
                real_explicit_stats.to_csv(tmp_explicits_fp, sep=';', index=False)
            except:
                pass

        # make sure you don't have negative values:
        lr_cols_p = real_explicit_stats.filter(regex='.*lower_range.*').columns
        prev_values = real_explicit_stats.loc[:, lr_cols_p].values
        # ---- check whether the lower range lower than zero or not:
        for c_col in lr_cols_p:
            real_explicit_stats.loc[:, c_col] = real_explicit_stats.loc[:, c_col].apply(
                lambda x: x if x > 0 else 0.)
        if not (real_explicit_stats.loc[:, lr_cols_p].values == prev_values).all():
            self.logger.warning(f"You have some negative values for lower_range (!) in statistics. " + \
                                f"It may be a sign of too high variance for the particular cycle-house combination")

        # again:

        if len(self.universal_params.StaticParams.gby) > 0:
            cols_to_ignore = self.universal_params.StaticParams.gby + ['total', 'age']
        else:
            self.logger.info(
                f"since {self.universal_params.StaticParams.gby} is empty statistics will be collected globally")
            cols_to_ignore = ['total', 'age']
        return real_explicit_stats, loaded_explicit_stats, tmp_explicits_fp, cols_to_ignore

    def check_and_save_explicit_stat_cloud(self, real_explicit_stats,
                                           loaded_explicit_stats,
                                           tmp_explicits_fp):
        if 'age' not in (real_explicit_stats.columns):
            real_explicit_stats.rename(columns={"age": "daynum"})
        real_explicit_stats = real_explicit_stats.sort_values(by=['age'])

        if not loaded_explicit_stats:
            # generate name for the previous file
            prefix_combo = "_".join(self.universal_params.engine_postfix.split('_')[2:5])
            stats_folder = Path(statistics_server_dir) / \
                           f"{prefix_combo}_" \
                           f"{str(datetime.now().date())}_p{random.randint(200, 5000)}"
            os.mkdir(stats_folder)
            tmp_explicits_fp = stats_folder / f"raw_{self.local_way_params.output_filename_postfix}"
            real_explicit_stats.to_csv(tmp_explicits_fp, sep=';')

        # make sure you don't have negative values:
        lr_cols_p = real_explicit_stats.filter(regex='.*lower_range.*').columns
        prev_values = real_explicit_stats.loc[:, lr_cols_p].values
        # ---- check whether the lower range lower than zero or not:
        for c_col in lr_cols_p:
            real_explicit_stats.loc[:, c_col] = real_explicit_stats.loc[:, c_col].apply(
                lambda x: x if x > 0 else 0.)
        if not (real_explicit_stats.loc[:, lr_cols_p].values == prev_values).all():
            self.logger.warning(f"You have some negative values for lower_range (!) in statistics. " + \
                                f"It may be a sign of too high variance for the particular cycle-house combination")

        # again:

        if len(self.universal_params.StaticParams.gby) > 0:
            cols_to_ignore = self.universal_params.StaticParams.gby + ['total', 'age']
        else:
            self.logger.info(
                f"since {self.universal_params.StaticParams.gby} is empty statistics will be collected globally")
            cols_to_ignore = ['total', 'age']
        return real_explicit_stats, loaded_explicit_stats, tmp_explicits_fp, cols_to_ignore

    def save_results(self, replaced_output, initial_used_stats, statistics_df_init, engine_config):
        datetime_format = "%Y_%m_%d__%H_%M_%S"
        dt_postfix = datetime.now().strftime(datetime_format)
        folder_name = '_'.join([self.local_way_params.output_folder_prefix, dt_postfix])
        save_dir = Path(engine_config.local_results_dir) / folder_name

        if not save_dir.exists():
            save_dir.mkdir()
            self.logger.info(f"created output dir {save_dir}")

        save_path = save_dir / self.local_way_params.output_filename_postfix
        splitter = '.'
        fname_parts = self.local_way_params.output_filename_postfix.split(splitter)
        save_no_data_path = save_dir / (
                splitter.join(fname_parts[:-1]) + '_no_explicit_data' + splitter + fname_parts[-1])

        try:
            final_output = replaced_output[statistics_df_init.columns]
        except Exception as E:
            self.logger.exception(
                f"Failed to reorder columns, probably due to different columns in the initial statistics file and "
                f"current: {E}")
            self.logger.warning(f"Final output will be saved with different order of the column due to exception above")
            final_output = replaced_output

        final_output.to_csv(save_path, sep=";", index=False)
        self.logger.info(f"Generated statistics using explicits saved to {save_path}")
        initial_used_stats.to_csv(save_no_data_path, sep=';', index=False)
        self.logger.info(f"Generated statistics with no real data saved at {save_no_data_path}")

        config_save_fp = save_dir / 'config.yaml'
        with open(config_save_fp, 'w') as tmp_file:
            yaml.safe_dump(config, tmp_file)
        self.logger.info(f"\nDumped config at the {config_save_fp}\n")

        return save_path

    def save_results_cloud(self, replaced_output, initial_used_stats, statistics_df_init, raw_stat_fp):
        datetime_format = "%Y_%m_%d__%H_%M_%S"
        dt_postfix = datetime.now().strftime(datetime_format)
        folder_name = '_'.join([self.local_way_params.output_folder_prefix, dt_postfix])
        # save_dir = Path(engine_config.local_results_dir) / folder_name
        output_fp = raw_stat_fp.parent
        if not output_fp.exists():
            output_fp.mkdir()
        self.logger.info(f"output dir: \n{output_fp}")

        save_path = output_fp / self.local_way_params.output_filename_postfix
        splitter = '.'
        fname_parts = self.local_way_params.output_filename_postfix.split(splitter)
        save_no_data_path = output_fp / (
                splitter.join(fname_parts[:-1]) + '_no_explicit_data' + splitter + fname_parts[-1])

        try:
            final_output = replaced_output[statistics_df_init.columns]
        except Exception as E:
            self.logger.exception(
                f"Failed to reorder columns, probably due to different columns in the initial statistics file and "
                f"current: {E}")
            self.logger.warning(f"Final output will be saved with different order of the column due to exception above")
            final_output = replaced_output

        final_output.index.name = 'ExpID'
        final_output.to_csv(save_path, sep=";")
        self.logger.info(f"Generated statistics using explicits saved to {save_path}")
        initial_used_stats.index.name = 'ExpID'
        initial_used_stats.to_csv(save_no_data_path, sep=';')
        self.logger.info(f"Generated statistics with no real data saved at {save_no_data_path}")

        config_save_fp = output_fp / 'config.yaml'
        with open(config_save_fp, 'w') as tmp_file:
            yaml.safe_dump(config, tmp_file)
        self.logger.info(f"\nDumped config at the {config_save_fp}\n")

        return save_path

    def check_out_of_bounds(self, replaced_output, all_features):
        before_bounds_check = replaced_output.copy()
        replaced_output = out_of_bounds_check(
            replaced_output,
            logger=self.logger,
            features=all_features,
            min_acceptable_value=1e-6,
            features_settings=self.features_params
        )
        return replaced_output

    def check_negative_values(self, replaced_output, all_features):
        if self.universal_params.StaticParams.update_negative_values:
            replaced_output_before_negative_check = replaced_output.copy()
            negative_check_cols = [f"{feature}_mean" for feature in all_features]
            replaced_output = negative_check(
                df=replaced_output_before_negative_check,
                logger=self.logger,
                cols_to_check=negative_check_cols,
                interpolate_params=self.universal_params.interpolation_params
            )
        return replaced_output

    def adjust_after_interpolation(self, replaced_output, replaced_explicit_stats, all_features):
        # rel_error_after_interpolation_df = (
        #         (replaced_explicit_stats - replaced_output[
        #             set(list(replaced_explicit_stats.columns)).intersection(replaced_output.columns)]) /
        #         replaced_output[
        #             set(list(replaced_explicit_stats.columns)).intersection(replaced_output.columns)]
        # ).dropna(how='all', axis=0).dropna(how='all', axis=1)

        common_columns = list(set(replaced_explicit_stats.columns).intersection(replaced_output.columns))

        # Выполняем расчеты, используя common_columns
        rel_error_after_interpolation_df = (
                (replaced_explicit_stats[common_columns] - replaced_output[common_columns]) /
                replaced_output[common_columns]
        ).dropna(how='all', axis=0).dropna(how='all', axis=1)

        rel_error_threshold = self.universal_params.StaticParams.rel_error_threshold

        for feature in all_features:
            tmp_mean_col = f"{feature}_mean"
            if tmp_mean_col in rel_error_after_interpolation_df.columns:
                should_adjust_mask = rel_error_after_interpolation_df[tmp_mean_col].abs() > rel_error_threshold
                if should_adjust_mask.sum() > 0:
                    exceeded_days = should_adjust_mask[should_adjust_mask == True].index.tolist()
                    self.logger.error(
                        f"{len(exceeded_days)} days ({' ,'.join([str(i) for i in exceeded_days])}) exceeding rel "
                        f"error threshold {rel_error_threshold} for the {tmp_mean_col}: " +
                        f"abs rel errors are {rel_error_after_interpolation_df.loc[exceeded_days, tmp_mean_col].round(6).values.tolist()}"
                    )

                    should_adjust_mask_reindexed = should_adjust_mask.reindex(
                        np.arange(0, len(replaced_output), 1)).fillna(False)
                    selected_outliers = replaced_explicit_stats.loc[should_adjust_mask, tmp_mean_col]
                    subtrahend = selected_outliers.reindex(
                        np.arange(selected_outliers.index.min(), len(replaced_output), 1))
                    next_idx_value = selected_outliers.index[-1] + 1
                    subtrahend[next_idx_value] = selected_outliers[selected_outliers.index[-1]]
                    subtrahend = subtrahend.fillna(0.)
                    tmp_diff = replaced_output.loc[0:, tmp_mean_col][1:] - subtrahend
                    mean_weight_threshold = None

                    if tmp_diff[next_idx_value] < 0:
                        mean_weight_threshold = replaced_output.loc[next_idx_value, tmp_mean_col]
                        self.logger.error(
                            f"for feature {feature} and column {tmp_mean_col} got real value from files exceeding the "
                            f"next value: " +
                            f"{subtrahend[next_idx_value]:.6f} > {replaced_output.loc[next_idx_value, tmp_mean_col]:.6f}. Interpolated value for the next day will be used as the threshold for the {next_idx_value - 1} day: {mean_weight_threshold:.6f}"
                        )

                    tmp_w = [
                        self.universal_params.StaticParams.adjusted_weights['interpolated'],
                        self.universal_params.StaticParams.adjusted_weights['real']
                    ]

                    weighted_mean = (replaced_output.loc[should_adjust_mask_reindexed, tmp_mean_col] * tmp_w[
                        0] + selected_outliers * tmp_w[1]) / sum(tmp_w)

                    if mean_weight_threshold is not None:
                        last_real_value = next_idx_value - 1
                        if weighted_mean[last_real_value] > mean_weight_threshold:
                            self.logger.warning(
                                f"at day {last_real_value} weighted mean {weighted_mean[last_real_value]:.6} exceeds the threshold from interpolated for the next day {next_idx_value}: " +
                                f"{mean_weight_threshold:.6} so replacing it..."
                            )
                            weighted_mean[last_real_value] = mean_weight_threshold

                    replaced_output.loc[should_adjust_mask_reindexed, tmp_mean_col] = weighted_mean
                    self.logger.info(f"Fixed days {exceeded_days} with weighted mean: {weighted_mean}")

        return replaced_output

    def handle_curves(self, tmp_standard_values, tmp_input_values, interpolated, feature, col):
        to_stack = []

        for i in range(self.universal_params.StaticParams.num_curves):
            tmp_std_slice = tmp_standard_values[:-i].copy()

            if len(tmp_std_slice) <= self.universal_params.StaticParams.min_datapoints_for_curve:
                self.logger.warning(
                    f"temporary slice of len {len(tmp_std_slice)}. breaking the loop due to small datapoints")
                break

            tmp_interpolated = self.perform_interpolation(tmp_input_values, tmp_std_slice)
            to_stack.append(tmp_interpolated)

        if len(to_stack) == 0:
            self.logger.warning(
                f"there's no curves to concat; debug it for {feature}, {col} due to small num of datapoints")
        else:
            stacked = np.array(to_stack)
            prev_interpolated = interpolated.copy()
            if 0 < len(stacked.shape) <= 2:
                interpolated = np.mean(stacked, axis=0)
                self.logger.warning(f"using mean from curves to get interpolated due to {len(to_stack)} num curves")
            else:
                interpolated = np.median(stacked, axis=0)
                self.logger.info(f"using median to get interpolated; num of curves: {len(to_stack)}")

            self.logger.info(
                f"Difference between median of {len(stacked)} "
                f"curves and simple interpolation is {(interpolated - prev_interpolated).mean():.3f} per datapoint for feature {feature} column = {col}")

        return interpolated

    def perform_interpolation(self, tmp_input_values, tmp_standard_values):
        useFirstStandardValue = self.universal_params.useFirstStandardValue
        use_last_standard_value = self.universal_params.useLastStandardValue

        return adjust_standard_to_values(
            standard=tmp_input_values,
            initial_values=tmp_standard_values,
            vis=False,
            smooth_window=self.universal_params.smooth_window,
            useFirstStandardValue=useFirstStandardValue,
            useLastStandardValue=use_last_standard_value,
            average=self.universal_params.average,
            extra_title=False
        )

    def interpolate_values(self, feature, feature_settings, replaced_output, tmp_w_init, all_features,
                           replaced_explicit_stats, df_output):
        cols_to_replace = [f"{feature}_mean", f"{feature}_stdev", f"{feature}_lstdev_coef", f"{feature}_rstdev_coef"]

        for feature in all_features:
            # feature_settings = get_feature_settings(feature)

            if not feature_settings["adapt"]:
                self.logger.info(
                    f"skipping stats calculation for feature {feature} due to adapt == {feature_settings['adapt']}"
                )
                continue

            for col in cols_to_replace:
                tmp_w = tmp_w_init.copy()
                if col not in replaced_explicit_stats.columns:
                    self.logger.exception(
                        f"Caught col {col} that doesn't exist in calculated explicits stats; check your code/files")
                    continue

                non_null = replaced_explicit_stats[col].dropna()
                if len(non_null) == 0:
                    self.logger.warning(f"Skipping {col} for feature {feature} due to all NaN values")
                    continue

                tmp_standard_values = non_null
                tmp_input_values = df_output[col]
                interpolated = self.perform_interpolation(tmp_input_values, tmp_standard_values)

                if self.universal_params.StaticParams.num_curves > 0:
                    interpolated = self.handle_curves(tmp_standard_values, tmp_input_values, interpolated, feature, col)

                indiv_weight = None  # Replace with actual weight logic if needed
                if indiv_weight is not None:
                    self.logger.warning(
                        f"individual_weight for feature={feature} "
                        f"is not None; using this over the general initial weight\n{tmp_w[1]} ---> {indiv_weight}")
                    tmp_w[1] = indiv_weight

                tmp_adjusted = (interpolated * tmp_w[0] + tmp_input_values * tmp_w[1]) / sum(tmp_w)
                replaced_output[col] = tmp_adjusted

        return replaced_output

    def initialize_and_check_weights(self, df_output):
        initial_used_stats = copy.deepcopy(df_output)
        replaced_output = copy.deepcopy(df_output)

        tmp_w_init = [
            self.universal_params.StaticParams.adjusted_weights['interpolated'],
            self.universal_params.StaticParams.adjusted_weights['previous']
        ]

        if tmp_w_init[0] < 0.5 * sum(tmp_w_init):
            self.logger.warning(
                f"You can't use less than 50% real values from explicits themselves; " +
                f"assigning it to 50% of the weights as the minima; got: {tmp_w_init}"
            )
            tmp_w_init[0] = tmp_w_init[1]
            self.logger.info(f"Completed: new weights are {tmp_w_init}")

        return replaced_output, tmp_w_init

    def generate_stat_local_way(self, filters: Filter):
        # TODO^ FINALLY - LOCAL WAY !
        engine_config = self.define_engine_config_local()
        self.set_up_correct_mean_coef()
        ages = self.get_ages()
        statistics_df_init = self.get_local_stat(engine_config)

        if self.local_way_params.use_res_df:
            self.logger.info("\nCollecting statistics from engine results")

            raw_engine_stat = self.collect_real_stat_from_local_engine_res(engine_config=engine_config)
            statistics_df = self.interpolate_stat(real_statistics_df=raw_engine_stat,
                                                  statistics_df_init=statistics_df_init)
        else:
            self.logger.info(
                f"\nres_df won't be used. Using {statistics_fname} as a temporary ideal stats")
            statistics_df = statistics_df_init.copy()

        df_output = pd.DataFrame()
        for feature in self.all_features:
            self.logger.info(f'Processing {feature}')

            # ------- #
            feature_settings = self.get_settings_for_feature(feature)
            feature_col = FeatureColNames(feature)
            n_left_stdev = feature_settings["n_left_stdev"]
            is_filtrable = feature_settings["isFilterable"]
            # ------- #

            feature_df, \
                statistics_df_init = self.set_up_custom_stat_values(feature=feature,
                                                                    feature_col=feature_col,
                                                                    statistics_df=statistics_df,
                                                                    statistics_df_init=statistics_df_init)

            feature_df, statistics_df_init, df_output = self.prepare_feature_process(
                feature=feature, feature_df=feature_df, feature_col=feature_col,
                statistics_df_init=statistics_df_init,
                is_filtrable=is_filtrable, n_left_stdev=n_left_stdev, df_output=df_output)

        # NOT FEATURES BUT EXPLICITS LEVEL HERE
        # WORK WITH SMALL COMBO AND EXPLICITS
        real_explicit_stats, loaded_explicit_stats, \
            tmp_explicits_fp = self.work_with_explicits(filters, engine_config, ages)

        real_explicit_stats, \
            loaded_explicit_stats, \
            tmp_explicits_fp, \
            cols_to_ignore = self.check_and_save_explicit_stat(
            real_explicit_stats=real_explicit_stats,
            loaded_explicit_stats=loaded_explicit_stats,
            tmp_explicits_fp=tmp_explicits_fp)

        # before anything else check explicits group by age:

        real_explicit_stats_before_mean_check = real_explicit_stats.copy()
        real_explicit_stats = check_feature_mean_difference(
            df=real_explicit_stats_before_mean_check,
            features=self.all_features,
            feature_settings=self.features_params,
            how=self.universal_params.StaticParams.mean_check_how,
            mean_diff_thresh=self.universal_params.StaticParams.mean_diff_thresh,
            gby=self.universal_params.StaticParams.gby,
            logger=self.logger)

        replaced_explicit_stats = update_explicit_boundaries(
            real_explicit_stats=real_explicit_stats,
            cols_to_ignore=cols_to_ignore,
            boundaries=self.universal_params.StaticParams.boundaries,
            features=self.all_features,
            logger=self.logger,
            weights_col='total',
            feature_settings=self.features_params)

        initial_used_stats = copy.deepcopy(df_output)
        replaced_output, tmp_w_init = self.initialize_and_check_weights(df_output)
        replaced_output = self.interpolate_values(feature=feature,
                                                  feature_settings=feature_settings,
                                                  replaced_output=replaced_output,
                                                  tmp_w_init=tmp_w_init,
                                                  all_features=self.all_features,
                                                  replaced_explicit_stats=replaced_explicit_stats,
                                                  df_output=df_output)
        replaced_output = self.adjust_after_interpolation(replaced_output, replaced_explicit_stats,
                                                          self.all_features)
        replaced_output = self.check_negative_values(replaced_output, self.all_features)
        replaced_output = self.check_out_of_bounds(replaced_output, self.all_features)
        save_path = self.save_results(engine_config=engine_config,
                                      replaced_output=replaced_output,
                                      initial_used_stats=initial_used_stats,
                                      statistics_df_init=statistics_df_init)

        return save_path

    def work_with_explicits_cloud(self, filters, engine_config, ages):
        # reserve flag:
        loaded_explicit_stats: bool = False
        real_explicit_stats: Optional[pd.DataFrame] = None
        tmp_explicits_fp: Optional[Union[str, Path]] = None

        t0 = time.time()
        # TODO: remove law and iterate over ages and then over features
        self.logger.debug("\n" + '*' * 50 + '\n' + '***** USING DATA TO CALIBRATE STATISTICS *****' + '\n')

        small_combinations_ages: List[int] = self.universal_params.small_combinations_ages
        small_combinations_boundary_shifts: List[int] = self.universal_params.small_combinations_boundary_shifts
        small_comb_bound_shifts_list: List[float] = \
            self.propagate_coefficients(ages=small_combinations_ages,
                                        coefficients=small_combinations_boundary_shifts,
                                        max_age=max_age)
        self.logger.warning(
            f"inserted {small_comb_bound_shifts_list} as a list of "
            f"boundary shifts for small combinations under the {SMALL_COMB_IQR_KEY} kwy")

        if not loaded_explicit_stats:

            filters.clients = [self.universal_params.client]

            devices = PostgresDevicesStorage()
            devices_loc = devices.get_devices(filters)
            uniques = list(devices_loc['cycle'].dropna().unique())
            or_pattern_cycle = get_regex_or(uniques)

            unique_houses = list(devices_loc['house'].dropna().unique())
            or_pattern_house = get_regex_or(unique_houses)
            dirs_to_files = get_dirs_to_files(devices_loc=devices_loc, filters=filters,
                                              main_config=engine_config, logger=self.logger, useRolled=False)
            selected_dirs = [i[0] for i in dirs_to_files]

            if self.universal_params.how == 'raw':
                # todo: ВЕРНУТЬ ТУТ proceed_explicits
                real_explicit_stats, replaced_ages = proceed_cloud_explicits(
                    feature_settings=self.features_params,
                    group_by_cols=self.universal_params.StaticParams.gby,
                    boundary_shifts=self.universal_params.small_combinations_boundary_shifts,
                    small_combinations_threshold=self.universal_params.small_combinations_threshold,
                    datapoints_num_thresh=self.local_way_params.datapoints_num_thresh,
                    iqr_boundary_shift=self.universal_params.iqr_boundary_shift,
                    iqr_percentiles=self.universal_params.iqr_percentiles,
                    selected_dirs=selected_dirs,
                    features=self.all_features,
                    or_pattern_cycle=or_pattern_cycle,
                    or_pattern_house=or_pattern_house,
                    _explicit_files_glob_pattern=_explicit_files_glob_pattern,
                    ages=ages, filters=filters,
                    logger=self.logger,
                    devices_slice=devices_loc,
                    main_config=engine_config)

                self.logger.info(
                    f'\nStatistics calculation using data completed in {(time.time() - t0) / 60:.3f} minutes')
                self.logger.warning(
                    f"Individually adapted days: {', '.join([str(i) for i in list(replaced_ages)])}")
            elif self.universal_params.how == 'fast':
                real_explicit_stats = self.get_stat_from_ec2()

            else:
                raise NotImplementedError()

        # else:
        #     real_explicit_stats = pd.read_csv(tmp_explicits_fp, sep=None, engine='python')

        if real_explicit_stats is None:
            raise NotImplementedError(f"Statistics from explicit hasn't been initialized yet")

        return real_explicit_stats, loaded_explicit_stats, tmp_explicits_fp

    def cloud_way_raw(self, filters):
        engine_config = self.define_engine_config_local()  # todo: ДРОПНУТЬ
        self.set_up_correct_mean_coef()
        ages = self.get_ages()
        statistics_df_init = self.get_local_stat(engine_config)

        self.logger.info(
            f"\nres_df won't be used. Using {statistics_fname} as a temporary ideal stats")
        statistics_df = statistics_df_init.copy()

        df_output = pd.DataFrame()
        for feature in self.all_features:
            self.logger.info(f'Processing {feature}')

            # ------- #
            feature_settings = self.get_settings_for_feature(feature)
            feature_col = FeatureColNames(feature)
            n_left_stdev = feature_settings["n_left_stdev"]
            is_filtrable = feature_settings["isFilterable"]
            # ------- #

            feature_df, \
                statistics_df_init = self.set_up_custom_stat_values(feature=feature,
                                                                    feature_col=feature_col,
                                                                    statistics_df=statistics_df,
                                                                    statistics_df_init=statistics_df_init)

            # feature, feature_df, statistics_df_init, is_filtrable, feature_col, n_left_stdev, df_outp
            feature_df, statistics_df_init, df_output = self.prepare_feature_process(
                feature=feature, feature_df=feature_df, feature_col=feature_col,
                statistics_df_init=statistics_df_init,
                is_filtrable=is_filtrable, n_left_stdev=n_left_stdev, df_output=df_output)

        # NOT FEATURES BUT EXPLICITS LEVEL HERE
        # WORK WITH SMALL COMBO AND EXPLICITS
        real_explicit_stats, loaded_explicit_stats, \
            tmp_explicits_fp = self.work_with_explicits_cloud(filters, engine_config, ages)

        real_explicit_stats, \
            loaded_explicit_stats, \
            tmp_explicits_fp, \
            cols_to_ignore = self.check_and_save_explicit_stat_cloud(
            real_explicit_stats=real_explicit_stats,
            loaded_explicit_stats=loaded_explicit_stats,
            tmp_explicits_fp=tmp_explicits_fp)
        # before anything else check explicits group by age:

        real_explicit_stats_before_mean_check = real_explicit_stats.copy()
        real_explicit_stats = check_feature_mean_difference(
            df=real_explicit_stats_before_mean_check,
            features=self.all_features,
            feature_settings=self.features_params,
            how=self.universal_params.StaticParams.mean_check_how,
            mean_diff_thresh=self.universal_params.StaticParams.mean_diff_thresh,
            gby=self.universal_params.StaticParams.gby,
            logger=self.logger)

        replaced_explicit_stats = update_explicit_boundaries(
            real_explicit_stats=real_explicit_stats,
            cols_to_ignore=cols_to_ignore,
            boundaries=self.universal_params.StaticParams.boundaries,
            features=self.all_features,
            logger=self.logger,
            weights_col='total',
            feature_settings=self.features_params)

        initial_used_stats = copy.deepcopy(df_output)
        replaced_output, tmp_w_init = self.initialize_and_check_weights(df_output)
        replaced_output = self.interpolate_values(feature=feature,
                                                  feature_settings=feature_settings,
                                                  replaced_output=replaced_output,
                                                  tmp_w_init=tmp_w_init,
                                                  all_features=self.all_features,
                                                  replaced_explicit_stats=replaced_explicit_stats,
                                                  df_output=df_output)
        replaced_output = self.adjust_after_interpolation(replaced_output, replaced_explicit_stats,
                                                          self.all_features)
        replaced_output = self.check_negative_values(replaced_output, self.all_features)
        replaced_output = self.check_out_of_bounds(replaced_output, self.all_features)
        save_path = self.save_results_cloud(raw_stat_fp=tmp_explicits_fp,
                                            replaced_output=replaced_output,
                                            initial_used_stats=initial_used_stats,
                                            statistics_df_init=statistics_df_init)

        return save_path

    def get_stat_from_ec2(self):

        # connection and required defining permission
        shell = ShellHandler(host=EC2_HOST_PROD, psw=EC2_KEY_PROD, user=EC2_USER_PROD)
        shell.stdin.write("sudo su " + '\n')

        self.logger.info(f"search for engine:   {self.universal_params.engine_postfix}")
        cmd_go2_engines = f'cd {EC2_ENGINE_FOLDER_PATH_PROD}/{self.universal_params.engine_postfix}'
        _ex1 = shell.execute(cmd=cmd_go2_engines)

        cmd_ls = 'ls -1\n'
        _ex1 = shell.execute(cmd=cmd_ls)[1]
        assert len(_ex1), f"no such engine on ec2 {self.universal_params.engine_postfix}"
        stat_file = [i for i in _ex1 if "Statistics" in i][0]

        cmd_read_stat_file = f"cat {stat_file}"
        res = shell.execute(cmd=cmd_read_stat_file)[1]

        line = ''
        for num, _ in enumerate(res):
            line += _

        stat_df = pd.read_csv(StringIO(line), sep=';')

        return stat_df

    def cloud_way_fast(self, filters: Filter):
        real_stat = self.get_stat_from_ec2()

        # engine_config = self.define_engine_config_local()  # todo: ДРОПНУТЬ
        self.set_up_correct_mean_coef()

    def run(self):
        self.all_features = self.print_all_features()
        filters = Filter()

        if self.need2use_local_way:
            self.logger.info(f"{' Local stats generation will be used, with reading local files.. ':-^70}")
            self.generate_stat_local_way(filters=filters)
        else:

            self.logger.info(f"{' Cloud way stats generation will be used.. ':-^70}")
            if self.universal_params.how == "fast":
                self.logger.info("..with reading engine stat from ec2")
                self.cloud_way_fast(filters=filters)
            if self.universal_params.how == "raw":
                self.logger.info("..with collecting real explicits stats from S3")
                self.cloud_way_raw(filters=filters)

            # fast ..with reading engine stat from ec2 - пока скип
            #    т.к. нет коннекта к прод ec2, мб ключ сменили
            # todo: пока что разветвления не делаем, чисто выводим инфу по how

            # коннект к s3


if __name__ == '__main__':
    # =============

    inp_cdg_fp = r"D:\PAWLIN\BDM2\birdoo-data-manager\bdm2\data_handling\generated_data\features_stats\generate_statistic.yaml"

    global config
    with open(inp_cdg_fp, 'r') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    features_params = FeaturesParams(**config['features_stats'])
    universal_params = UniversalParams(features_params=features_params,
                                       **config['universal_params'])

    local_way_params = LocalWayParams(**config['local_way_params'])
    # todo: click_params
    need2use_local_way = config['use_local_way']

    stat_generator = StatisticsGenerator(features_params,
                                         universal_params,
                                         local_way_params,
                                         need2use_local_way)
    stat_generator.run()
