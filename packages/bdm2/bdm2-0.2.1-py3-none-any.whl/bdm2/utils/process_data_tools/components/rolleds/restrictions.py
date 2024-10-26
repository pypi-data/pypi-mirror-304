import datetime
import logging
import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Iterable

import numpy as np
import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'scipy',
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

scipy = checker.get_module('scipy')
plt = checker.get_module('matplotlib.pyplot')

from bdm2.constants.global_setup.data import (
    device_match_columns,
    standards_match_columns,
    max_age,
)
from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.utils.process_data_tools.components.explicits import explicit_manager
from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.collecting.rolled import (
    RolledCollectingParams,
)

from bdm2.utils.process_data_tools.components.distributions import distribution_utils
from bdm2.utils.process_data_tools.data_clasterization import reduce_data
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import (
    ActualClientsInfoStorage,
)
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import (
    PostgresDevicesStorage,
)

# from src.utils.schemas.models.postgres_devices_storage import PostgresDevicesStorage

# from BIRDOO_IP.storages.devices.postgres_devices_storage import PostgresDevicesStorage
# from BIRDOO_IP.storages.actual_clients_info_storage.actual_clients_info_storage import ActualClientsInfoStorage

from bdm2.utils.process_data_tools.components.birdoo_filter import (
    Filter,
    init_filter_from_devices,
)


@dataclass
class FeatureExtrapolationParams:
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    max_cv: Optional[float] = None  #
    # For some features (ex. volume) it is important to keep cv of distribution.
    # For example if we extrapolate distribution for age 20 to age 5 - it is not good as result distrib will be
    # too wide for age 5
    # But for such features as reliability it is ok
    keep_cv: bool = False
    #
    shift_to_target: bool = False
    mean_values_smooth_window: Optional[int] = 1


class FeaturesRestrictions(Dict[str, FeatureExtrapolationParams]):
    @property
    def restriction_as_df(self) -> pd.DataFrame:
        return pd.DataFrame([self[c].__dict__ for c in self], index=list(self.keys())).T

    @property
    def max_cv_as_series(self) -> pd.Series:
        restrictions_df = self.restriction_as_df
        if "max_cv" not in restrictions_df.index:
            return pd.Series(dtype=float)
        return restrictions_df.loc["max_cv"]

    @property
    def min_value_as_series(self) -> pd.Series:
        restrictions_df = self.restriction_as_df
        if "min_value" not in restrictions_df.index:
            return pd.Series(dtype=float)
        return restrictions_df.loc["min_value"]

    @property
    def max_value_as_series(self) -> pd.Series:
        restrictions_df = self.restriction_as_df
        if "max_value" not in restrictions_df.index:
            return pd.Series(dtype=float)
        return restrictions_df.loc["max_value"]


global_feature_restrictions = FeaturesRestrictions(
    {
        "mass_corr": FeatureExtrapolationParams(
            min_value=0.01, max_value=10, max_cv=0.5, keep_cv=True, shift_to_target=True
        ),
        "volume_norm_corr": FeatureExtrapolationParams(
            min_value=0.01, max_value=20, max_cv=0.5, keep_cv=True, shift_to_target=True
        ),
        "min_axis_norm_corr": FeatureExtrapolationParams(
            min_value=0.01,
            max_value=100,
            max_cv=0.5,
            keep_cv=True,
            shift_to_target=True,
        ),
        "max_axis_norm_corr": FeatureExtrapolationParams(
            min_value=0.01,
            max_value=100,
            max_cv=0.5,
            keep_cv=True,
            shift_to_target=True,
        ),
        "region_dim_norm": FeatureExtrapolationParams(
            min_value=0.01,
            max_value=100,
            max_cv=0.5,
            keep_cv=True,
            shift_to_target=True,
        ),
        "height": FeatureExtrapolationParams(
            min_value=0.01,
            max_value=50,
            max_cv=0.5,
            keep_cv=True,
            shift_to_target=True,
            mean_values_smooth_window=3,
        ),
        "shape_correction_coef": FeatureExtrapolationParams(
            min_value=0.5,
            max_value=1.5,
            max_cv=0.5,
            keep_cv=False,
            shift_to_target=False,
        ),
        "density_correction_coef": FeatureExtrapolationParams(
            min_value=0.5,
            max_value=1.5,
            max_cv=0.5,
            keep_cv=False,
            shift_to_target=False,
        ),
        "doc_weight": FeatureExtrapolationParams(
            min_value=0.00,
            max_value=1,
            max_cv=0.5,
            keep_cv=False,
            shift_to_target=False,
        ),
        "pos_x_pix": FeatureExtrapolationParams(
            min_value=-1, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "pos_y_pix": FeatureExtrapolationParams(
            min_value=-1, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "sitting_score": FeatureExtrapolationParams(
            min_value=-1, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "reliability": FeatureExtrapolationParams(
            min_value=0, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "private_reliability": FeatureExtrapolationParams(
            min_value=0, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "common_reliability": FeatureExtrapolationParams(
            min_value=0, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "tilt_reliability": FeatureExtrapolationParams(
            min_value=0, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
        "missing_reliability": FeatureExtrapolationParams(
            min_value=0, max_value=1, max_cv=0.5, keep_cv=False, shift_to_target=False
        ),
    }
)


@dataclass
class Distrib2Extrapolate:
    """
    Constructor arguments:

    :param data: DataFrame of datapoints, where columns are the all features, that should be extrapolated
    :param age: corresponded age of data. Object of Distrib2Extrapolate should contain data only for one age
    :param shifted_data: modified data after shifting to target mean and applying statistical_restrictions
    :param statistical_restrictions: dict of FeatureExtrapolationParams with max/min values, max cv information
        for each freature
    :param weight: degree of impact of distribution (used in extrapolation function)
    """

    data: pd.DataFrame
    age: int
    shifted_data: Optional[pd.DataFrame] = None
    weight: float = 1


class RolledCollector:
    """
    Class for extending aggregated by day mean feature values with rolled. So for one age will be matched rolled data
    of specified features.

    Usage examples:

    1. Full matching. For all unique rows in input data will be matched all real rolled values.
    2. Matching with reducing. The same as full matching but control number of rolled samples for each inpur raw
    3. Extrapolation. Quite difficult

    """

    def __init__(
            self,
            params: RolledCollectingParams,
            logger: Optional,
            feature_restrictions: FeaturesRestrictions,
            statistics_storage: ActualClientsInfoStorage,
    ):

        self.params: RolledCollectingParams = params
        self.create_folder()
        self.logger = logger
        self.feature_restrictions = feature_restrictions
        self.statistics_storage = statistics_storage

        self.logger.info(f"{self.__class__.__name__} initialization.")
        self.logger.info(f"Params:\n{str(self.params)}")

    def create_folder(self):
        save_dir = self.params.work_dir

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            self.logger.info(f"{save_dir} was created")

        log_dir = os.path.dirname(
            os.path.join(self.params.work_dir, self.params.log_folder)
        )

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            self.logger.info(f"{log_dir} was created")

    @staticmethod
    def reduce_rolled_data(
            df: pd.DataFrame,
            gb_columns: List[str],
            reduce_by: List[str],
            reduce_target_column: str,
            reduce_target_count: int,
            reduce_round_val: int,
            logger: Optional,
    ) -> pd.DataFrame:
        """
        Reduce gb_columns groups of df to target reduce_target_count.
        Do it smart to save dependensies of reduce_by columns and reduce_target_column

        :param df:
        :param gb_columns:
        :param reduce_by:
        :param reduce_target_column:
        :param reduce_target_count:
        :param reduce_round_val:
        :return:
        """

        output_explicit_df = df.iloc[:0]
        for l, _group in df.groupby(gb_columns):
            group = _group.dropna(
                subset=reduce_by + [reduce_target_column], axis=0, how="any"
            )
            if len(group) <= reduce_target_count:
                output_explicit_df = pd.concat(
                    [output_explicit_df, group], ignore_index=True
                )
            elif any(pd.isna(group[reduce_by + [reduce_target_column]]).any(axis=1)):
                logger.warning(
                    f"There are nan values in {l} group. Them will be dropped"
                )
                output_explicit_df = pd.concat(
                    [output_explicit_df, group], ignore_index=True
                )
            else:
                decrease_rate = reduce_target_count / len(group)
                # group_to_process = group.loc[~pd.isna(group[[reduce_by+[reduce_target_column]]]).any(axis=1)]
                age_group_red = reduce_data(
                    group,
                    by=reduce_by,
                    target=reduce_target_column,
                    round_val=reduce_round_val,
                    decrease_rate=decrease_rate,
                    n_attempts=3,
                    verbose=True,
                )
                output_explicit_df = pd.concat(
                    [output_explicit_df, age_group_red], ignore_index=True
                )
        return output_explicit_df

    @staticmethod
    def extend_df_with_rolled(
            df: pd.DataFrame,
            index_columns: List[str],
            age_column: str,
            engine_name_column: str,
            results_postfix_column: str,
            features: List[str],
            feature_restrictions: Optional[FeaturesRestrictions],
            rolled_age_column: str,
            rolled_track_id_column: str,
            rolled_sess_id_column: str,
            gby_track_reliability: str,
            keep_mean_values: bool = False,  # only if feature_restrictions=None
            mean_feature_postfix: str = "_mean",
            min_count: int = 0,
            logger: Optional = None,
    ):
        """
        1. Check if engine_name_column and results_postfix_column are in df. as it is important to know
           for which engine to take rolled files
        2. Define features_to_collect from explicits. gby_track_reliability and rolled_track_id_column
           will be added automatically, as required for group by track
        3. Get rolled files for each index_columns group inside (engine, results_postfix) group and group them by track.
        4. Match rolled data to index_columns group by age.

            .. note::
                if feature was in input df it will be gropped and replaced with rolled values

        5. If keep_mean_values, define features, that has target mean values {feature}_{mean_feature_postfix} in df
            and shift distributions to target mean values if, feature_restrictions allow to do it .


        :param df: collected df to be extended with rolled ( for each farm/cycle/house/device/age will be merged
            correspondent reduced rolled data

        # :param index_columns: GlobalConfig.device_match_columns or GlobalConfig.house_match_columns
        :param age_column: age_column in input df
        :param engine_name_column: column in df with engine name that will be used in MainConfig initialization
            (to retrieve rolled data)
        :param results_postfix_column: column in df with correspondent results postfix

        :param features: features to be added from rolled. (i.e. volume_norm_corr, reliability, etc. not mean!!)
        :param feature_restrictions: to check which features could be shifted

        :param rolled_age_column: age column of rolled files (always 'daynum' by default)
        :param rolled_track_id_column: column for grouping by track (always 'Track_ID' by default)
        :param gby_track_reliability: reliability column to be use as weight for grouping by track
           (in most cases should be taken from GlobalConfig.group_by_methods[active_group_by_method])

        :param keep_mean_values: shift rolled to target mean values if feature_restrictions allow to do it
        :param mean_feature_postfix: postfix of column that will bw used as target for shifting
        :return:
        """

        # Checks
        vis = False
        if logger is None:
            logger = logging.getLogger()

        if (
                engine_name_column not in df.columns
                or results_postfix_column not in df.columns
        ):
            raise ValueError(
                f"Any of [{engine_name_column}, "
                f"{results_postfix_column}] not in df]"
            )

        # Load local devices' info for getting 'path' information
        devices_storage = PostgresDevicesStorage()
        devices = devices_storage.get_devices(
            filters=Filter(), output_format=devices_storage.inner_format
        )
        devices_format = devices_storage.inner_format

        missed_columns = [c for c in device_match_columns if c not in df.columns]
        union_columns = [c for c in device_match_columns if c in df.columns]
        if len(missed_columns):
            df = pd.merge(df, devices[device_match_columns], on=union_columns)
        # define features to be collected from rolled
        features_to_collect = features + [rolled_age_column, rolled_track_id_column]
        logger.info(f"features to collect from {features_to_collect}")

        if gby_track_reliability not in features_to_collect:
            features_to_collect.append(gby_track_reliability)

        # collect rolled data
        output_df = pd.DataFrame()

        dts = []
        n_devices_processed = 0
        for (engine, results_postfix), engine_df in df.groupby(
                [engine_name_column, results_postfix_column]
        ):

            logger.info(f"collecting rolled files for engine{engine}{results_postfix}")
            config = EngineConfig()
            config.set_another_engine_version(
                version=engine, results_postfix=results_postfix
            )

            union_index_columns = [c for c in index_columns if c in engine_df.columns]
            for gr_label, group in engine_df.groupby(union_index_columns):

                assert all(
                    group.groupby(age_column).size() == 1
                ), f"Group {gr_label} has duplicated ages"

                start_dt = datetime.datetime.now()
                gr_filters = init_filter_from_devices(group, age_column=age_column)

                # collect rolled data
                explicit_df = explicit_manager.get_all_features_df_from_explicits(
                    devices=devices,
                    engine_config=config,
                    filters=gr_filters,
                    useRolled=True,
                    add_device_params=True,
                    dropFiltered=True,
                )

                collected_features = [c for c in features if c in explicit_df.columns]
                if len(collected_features) != len(features):
                    not_collected_features = [
                        c for c in features if c not in explicit_df.columns
                    ]
                    logger.info(
                        "red",
                        f"Not all features were collected for {gr_label}: "
                        f"{not_collected_features}",
                    )

                if explicit_df is None:
                    logger.info("yellow", f"explicit_df for {gr_label} is None")
                    continue
                if explicit_df.empty:
                    logger.info("yellow", f"explicit_df for {gr_label} is empty")
                    continue
                if len(explicit_df) < min_count:
                    logger.info(
                        f"{gr_label} has too low samples count. will be skipped as not robust"
                    )
                    continue
                logger.info("Defining sess id")
                explicit_df[rolled_sess_id_column] = explicit_manager.define_sess_ids(
                    explicit_df
                )

                logger.info(
                    f"{len(explicit_df[rolled_sess_id_column].unique())} sessions were found"
                )
                # Group by track
                logger.info("Grouping by track")
                initial_size = len(explicit_df)
                explicit_df = explicit_manager.means_by(
                    explicit_df,
                    group_by_columns=[
                                         age_column,
                                         rolled_track_id_column,
                                         rolled_sess_id_column,
                                     ]
                                     + device_match_columns,
                    weight_coefs_column=gby_track_reliability,
                    add_count=True,
                    count_column="track_count",
                ).reset_index()

                logger.info(f"{initial_size} -> {len(explicit_df)}")
                #  rename columns
                if age_column != rolled_age_column:
                    explicit_df = explicit_df.rename(
                        columns={rolled_age_column: age_column}
                    )

                # shift means to save mean values as in input df data
                if keep_mean_values and feature_restrictions is not None:
                    explicit_df_mean = explicit_df.groupby(age_column).mean()
                    device_group_mean = group.groupby(age_column).mean()
                    # get features that has {feature}_mean column in df and need to be shifted
                    features_to_shift = [
                        f
                        for f in collected_features
                        if f"{f}{mean_feature_postfix}" in group.columns
                    ]
                    logger.info(
                        f"features to be shifted to mean values: {features_to_shift}"
                    )

                    # get correspondent mean values
                    target_features_to_shift = [
                        f"{f}{mean_feature_postfix}" for f in features_to_shift
                    ]

                    fig, axes = plt.subplots(len(target_features_to_shift))
                    if not isinstance(axes, Iterable):
                        axes = [axes]
                    f_ind = 0
                    # shift each feature
                    for f_to_shift, target_f_to_shift in zip(
                            features_to_shift, target_features_to_shift
                    ):
                        # do not shift if not necessary
                        if (
                                feature_restrictions is not None
                                and f_to_shift in feature_restrictions
                        ):
                            if not feature_restrictions[f_to_shift].shift_to_target:
                                logger.info(f"{f_to_shift} will not be shifted ")
                                f_ind += 1
                                continue
                        logger.info(
                            f"shifting {f_to_shift} to {target_f_to_shift} values"
                        )
                        mean_diff = (
                                device_group_mean[target_f_to_shift]
                                - explicit_df_mean[f_to_shift]
                        )
                        # do not change if no explicit_df_mean for age
                        mean_diff = mean_diff.fillna(0)
                        age_indexes = explicit_df[age_column]

                        axes[f_ind].plot(
                            explicit_df.groupby(age_column).mean()[f_to_shift],
                            label="initial rolled",
                        )
                        axes[f_ind].plot(
                            device_group_mean[target_f_to_shift], label="target mean"
                        )
                        # shifting
                        explicit_df[f_to_shift] = (
                                explicit_df[f_to_shift] + mean_diff.loc[age_indexes].values
                        )

                        axes[f_ind].plot(
                            explicit_df.groupby(age_column).mean()[f_to_shift],
                            label="shifted",
                        )
                        axes[f_ind].set_title(f_to_shift)
                        axes[f_ind].legend()
                        f_ind += 1
                    if vis:
                        plt.show()
                    else:
                        plt.close(fig)

                # =============== match rolled to group by age ====================
                # drop columns to be replaced
                union_columns = list(
                    set(collected_features).intersection(group.columns)
                )
                if len(union_columns):
                    _group = group.drop(columns=union_columns)
                else:
                    _group = group.copy()

                match_cols = [
                    c for c in index_columns + [age_column] if c in _group.columns
                ]
                cols_to_match = [
                    c for c in collected_features + index_columns + [age_column]
                ]
                # merge rolled data to group (df part)
                explicit_df = pd.merge(
                    _group, explicit_df[cols_to_match], on=match_cols, how="left"
                )

                if output_df.empty:
                    output_df = explicit_df.copy()
                else:
                    output_df = pd.concat([output_df, explicit_df], ignore_index=True)

                end_dt = datetime.datetime.now()
                dt = (end_dt - start_dt).total_seconds()
                dts.append(dt)
                n_devices_processed += 1
            #     # TODO:REMOVE
            #     break
            # break

        logger.info(
            "blue",
            f"\n{n_devices_processed} devices were processed.\n"
            f"Mean dt for device processing: {np.round(np.mean(dts), 3)} s\n",
        )
        new_columns = [c for c in output_df.columns if c not in df.columns]
        return output_df[list(df.columns) + new_columns]  # to save columns order

    @staticmethod
    def get_extrapolated_distribution(
            distributions: List[Distrib2Extrapolate],
            target_distrib_restrictions: FeaturesRestrictions,
            target_age: int,
            target_mean: pd.Series,
            default_keep_cv: bool = True,
            vis: bool = False,
    ) -> pd.DataFrame:
        """
        Generate 1 interpolated/extrapolated distribution, according to all utils distributions.
        Weight of each distribution is considered as 1/distance of distributions' age to target_age. The far
        distribution age is the less impact it has


        :param target_distrib_restrictions:
        :param distributions:
        :param target_age:
        :param target_mean:
        :param default_keep_cv:
        :param vis:
        :return:
        """

        # define shifted distributions and set weight of each distribution according to target age
        weights_sum: float = 0.0

        max_values = target_distrib_restrictions.max_value_as_series.dropna()
        min_values = target_distrib_restrictions.min_value_as_series.dropna()

        for i, d in enumerate(distributions):
            # assert set(d.data.columns) == set(target_mean.index)

            # === define weight
            if target_age == d.age:
                distributions[i].weight = 1
            else:
                distributions[i].weight = 1 / abs(target_age - d.age)

            weights_sum += distributions[i].weight

            # === define target distribution parameters
            mean_d = d.data.mean(axis=0)
            std_d = d.data.std(axis=0)
            cv_d = std_d / mean_d

            # as default do not change std of distributions
            target_scale_coefs = pd.Series(1, index=d.data.columns)

            # do not shift as default
            _target_mean = mean_d.copy()

            # Iterate by features to correct distributions
            for f in cv_d.index:
                # check if need to correct std with target_scale_coefs
                if f in target_distrib_restrictions:
                    if target_distrib_restrictions[f].shift_to_target:
                        _target_mean[f] = target_mean[f]
                    if target_distrib_restrictions[f].max_cv is not None:
                        cv_d[f] = (
                            target_distrib_restrictions[f].max_cv
                            if target_distrib_restrictions[f].max_cv < cv_d[f]
                            else cv_d[f]
                        )
                    if target_distrib_restrictions[f].keep_cv:
                        target_std = _target_mean[f] * cv_d[f]
                        if pd.isnull(std_d[f]) or std_d[f] == 0:
                            target_scale_coefs[f] = 1
                        else:
                            target_scale_coefs[f] = target_std / std_d[f]
                elif default_keep_cv:
                    target_std = _target_mean[f] * cv_d[f]
                    if pd.isnull(std_d[f]) or std_d[f] == 0:
                        target_scale_coefs[f] = 1
                    else:
                        target_scale_coefs[f] = target_std / std_d[f]

            target_scale_coefs = target_scale_coefs.fillna(1)

            # shift data
            shifted_data = (d.data - mean_d) * target_scale_coefs + _target_mean

            # drop data that is out of boundaries by any of features
            union_index = list(set(min_values.index).intersection(shifted_data.columns))
            if len(union_index):
                is_ok = (
                        (shifted_data[union_index] >= min_values[union_index])
                        | shifted_data[union_index].isna()
                ).all(axis=1)
                is_ok = is_ok * (
                        (shifted_data[union_index] >= min_values[union_index])
                        | shifted_data[union_index].isna()
                ).all(axis=1)
                shifted_data = shifted_data[is_ok]

            # apply shifted_data
            distributions[i].shifted_data = shifted_data.copy()

        # Collect final distribution from shifted distributions
        final_distribution = pd.DataFrame(columns=target_mean.index, dtype=float)
        for d in distributions:
            r = np.round(d.weight / weights_sum, 2)
            n_samples = int(len(d.shifted_data) * r)
            final_distribution = pd.concat(
                [final_distribution, d.shifted_data.sample(n_samples)],
                ignore_index=True,
            )

        # vis target distribution and base ones
        if vis:
            axes = {}
            for feature in target_mean.index:
                axes[feature] = distribution_utils.AxesParams(
                    label=feature, xlabel="age", ylabel="count"
                )

            for d in distributions:
                mean_v = d.data.mean(axis=0).round(3)
                std_v = d.data.std(axis=0).round(3)
                cv_v = (std_v / mean_v * 100).round(1)

                for feature in target_mean.index:
                    axes[feature].distributions.append(
                        distribution_utils.Distribution(
                            label=f"age {d.age}, mean={mean_v[feature]}, CV={cv_v[feature]}%",
                            data=d.data[feature],
                        )
                    )
            mean_v = final_distribution.mean(axis=0).round(3)
            std_v = final_distribution.std(axis=0).round(3)
            cv_v = (std_v / mean_v * 100).round(1)

            for feature in target_mean.index:
                axes[feature].distributions.append(
                    distribution_utils.Distribution(
                        label=f"target age {target_age}, mean={mean_v[feature]}, CV={cv_v[feature]}%",
                        data=final_distribution[feature],
                    )
                )

            distribution_utils.plot_hist(axes_list=list(axes.values()), init_axes=True)
            plt.tight_layout()
            plt.show()

        return final_distribution

    def extrapolate(
            self, df: pd.DataFrame, gby_columns: List[str], features: List[str]
    ) -> pd.DataFrame:
        """
        extrapolate distributions for each gby_columns group in df

        .. note::
            Each gby_columns group will be sent to extrapolate_distributions(). It means that distributions will be
            interpolated by gby_columns+[age_column]

        :param df: collected df
        :param gby_columns: common values are Device/House identification columns
        :return:
        """
        time_delays = []
        df_output = df.iloc[:0].copy()
        gby_columns_full = [c for c in gby_columns]
        gby_columns_full += [c for c in standards_match_columns if c not in gby_columns]

        for label, group in df.groupby(gby_columns_full):
            self.logger.info(f"extrapolating {label}")

            # try to get available statistics for extrapolation mean values
            label_s = pd.Series(list(label), index=gby_columns_full)
            available_statistics = self.statistics_storage.get_actual_statistics(
                client=label_s["client"],
                breed_type=label_s["breed_type"],
                gender=label_s["gender"],
            )
            start_df = datetime.datetime.now()
            extrapolated_rolled_df = self.extrapolate_distributions(
                group,
                features=features,
                feature_restriction=self.feature_restrictions,
                extrapolated_flag_column=self.params.extrapolated_flag_column,
                max_age=self.params.extr_max_age,
                age_column=self.params.age_column,
                feature_statistics=available_statistics,
                mean_values_smooth_window=self.params.mean_values_smooth_window,
                distrib_count_to_extrapolate=self.params.distrib_count_to_extrapolate,
                apply_extrapolation_to_raw_datapoints=self.params.apply_extrapolation_to_raw_datapoints,
                logger=self.logger,
            )

            end_dt = datetime.datetime.now()
            dt = (end_dt - start_df).total_seconds()
            self.logger.info(f"extrapolate_distributions takes: {dt}")
            time_delays.append(dt)
            df_output = pd.concat(
                [df_output, extrapolated_rolled_df], ignore_index=True
            )

        self.logger.info(f"initial_rolled_df size: {len(df)}")
        self.logger.info(f"extrapolated_rolled_df size: {len(df_output)}")
        return df_output

    @staticmethod
    def extrapolate_distributions(
            df: pd.DataFrame,
            features: List[str],
            max_age: int,
            age_column: str,
            extrapolated_flag_column: str,
            feature_restriction: FeaturesRestrictions,
            distrib_count_to_extrapolate: int = 5,
            mean_values_smooth_window: int = 1,
            feature_statistics: Optional[pd.DataFrame] = None,
            apply_extrapolation_to_raw_datapoints: bool = False,
            vis_stat: bool = False,
            logger: Optional = None,
    ):
        """
        Get df that was extended with rolled and extrapolate distributions for all ages in range [0:max_age].

        .. note::
            input df should contain only data for one cycle-house/device sequence as will be fully grouped by age only

        Check which ages are not in df and which ages have only one sample (most probably extrapolated data)
        Extrapolation flag will be used for indicating ags that should be extrapolated

        The whole df will be grouped by age_column and then extrapolate all features' distributions. For each age
        will be chosen the closest raw data ages (ages that has rolled) number of the closest ages = smooth_window

        .. note::
            All the columns of df that are not in features will be filled with the most common value of the column

        :param df: df with matched rolled features. required columns: age_column, features
        :param features: features (from rolled files) to be extrapolated
        :param max_age:
        :param age_column:
        :param extrapolated_flag_column: used for indication that distribution extrapolation is required for this age
        :param feature_restriction:
        :param distrib_count_to_extrapolate: define number of the closest ages to be used for extrapolation, better to be odd
        :param mean_values_smooth_window: define number of the closest ages to be used for extrapolation, better to be odd
        :param feature_statistics: df with feature statistics. Should contain {feature}_mean columns
            to be used for extrapolation
        :param apply_extrapolation_to_raw_datapoints: if true, use extrapolation even for existed rolled data.
            It will take rolled for the specified age with maximum weight, but also will add samples from close ones
        :param vis_stat:
        :param logger:
        :return:
        """

        if logger is None:
            logger = build_logger(file_name=f"{Path(__file__)}", save_log=False)

        if max_age is None:
            max_age = df[age_column].max()

        logger.info(f"Rolled extrapolation max_age = {max_age}")
        full_index_range = np.arange(0, max_age + 1)

        # make df to be full indexed
        _df = pd.DataFrame(full_index_range, columns=[age_column], dtype=int)
        _df = pd.merge(_df, df, on=age_column, how="left")

        # df_mean_by_age_statistics
        _df_by_age = explicit_manager.means_by_age(_df, age_column, "").set_index(
            age_column
        )

        # Check if params.extrapolated_flag_column in df (usually appeared after extrapolation module).
        # if not, then check number of samples for each age, and if len(samples)==1 -> set as extrapolated (as could not
        # be extended with rolled)
        # extrapolated_flag indicates
        if extrapolated_flag_column not in _df:
            is_extrapolated: pd.Series = _df.groupby(age_column).size() == 1

            index = _df[age_column].values

            logger.info(
                "red",
                f"NO {extrapolated_flag_column} in df. Will be defined by number "
                f"of age group",
            )
            _df[extrapolated_flag_column] = is_extrapolated.loc[index].values

        # ============== DEFINE STATISTICS FOR INTERPOLATION ====================================================
        # define features, that need to be extrapolated.
        features_to_shift = [
            f
            for f in features
            if f in global_feature_restrictions
               and global_feature_restrictions[f].shift_to_target
        ]

        # defining mean values or features (that are rolled)
        df_mean_features = df.groupby(age_column)[features_to_shift].mean()

        # extrapolate each mean values or features  to full_index
        ext_feature_mean_statistics = pd.DataFrame(
            index=full_index_range, columns=df_mean_features.columns
        )

        fig, axes = plt.subplots(len(features_to_shift))
        if not isinstance(axes, Iterable):
            axes = [axes]

        for ind, col in enumerate(df_mean_features.columns):
            # Check if possible to extrapolate
            # as for some deviuces it could be, that the whole column is nan
            df_mean_features_not_na = df_mean_features[col].dropna()
            if len(df_mean_features_not_na) == 0:
                logger.info(f"df for {col} has only nan values. Can not extrapolate")
                continue
            # Try to define marget mean value for all requires age interval
            if (
                    (feature_statistics is None)
                    or (f"{col}_mean" not in feature_statistics)
                    or not all(
                [
                    age in feature_statistics.index.values
                    for age in ext_feature_mean_statistics.index.values
                ]
            )
            ):
                # Do scipy InterpolatedUnivariateSpline extrapolation
                try:
                    s = scipy.interpolate.InterpolatedUnivariateSpline(
                        x=df_mean_features_not_na.index.values,
                        y=df_mean_features_not_na.values,
                        k=1,
                    )
                    ext_feature_mean_statistics[col] = s(
                        ext_feature_mean_statistics.index.values
                    )
                    if (
                            mean_values_smooth_window > 2
                            and mean_values_smooth_window % 2 == 1
                    ):
                        ext_feature_mean_statistics[col] = (
                            ext_feature_mean_statistics[col]
                            .rolling(
                                mean_values_smooth_window, min_periods=1, center=True
                            )
                            .mean()
                        )
                    logger.info(
                        f"Statistics for {col} was generated by scipy.interpolate.InterpolatedUnivariateSpline"
                    )
                except Exception as e:
                    logger.error(
                        f"{col} ({ind}) has error during statistics extrapolation "
                        f"by InterpolatedUnivariateSpline:\n{e}"
                    )
            else:
                # get statistics based on statistics curve (simple extrapolator... sorry, not simple)
                try:
                    extr_feature_s = adjust_standard_to_values(
                        feature_statistics[col + "_mean"],
                        df_mean_features[col],
                        vis=False,
                        smooth_window=mean_values_smooth_window,
                        useFirstStandardValue=True,
                        useLastStandardValue=False,
                        average=5,
                        extra_title=col,
                    )
                    ext_feature_mean_statistics[col] = extr_feature_s.loc[
                        ext_feature_mean_statistics[col].index
                    ]
                    logger.info(
                        f"Statistics for {col} was generated by simple interpolator based on feature_statistics"
                    )
                except Exception as e:
                    logger.error(
                        f"{col} ({ind}) has error during statistics' simple extrapolation:\n{e}"
                    )

            axes[ind].plot(
                ext_feature_mean_statistics.index.values,
                ext_feature_mean_statistics[col].values,
                label="extrapolated",
            )
            axes[ind].plot(
                df_mean_features.index.values, df_mean_features[col].values, label="raw"
            )
            axes[ind].legend()
        if vis_stat:
            plt.show()
        else:
            plt.close(fig)

        # ========================================================================================================
        # Define ages for which distribution extrapolation will be performed
        # NOte, _df has full index range here [0:max_age]
        ages_raw = _df[_df[extrapolated_flag_column] == False][age_column].unique()
        # ages_to_extrapolate = _df[_df[self.params.extrapolated_flag_column] == True][self.params.age_column].unique()

        # ========================================================================================================
        # Iterate by age.
        # iterate even by NOT extrapolated data to apply smooth - shift mean (using another mean)
        df_extrapolated = df.iloc[:0].copy()
        df_by_ages = _df.groupby(age_column)

        # for age, main_group in _df_by_age.groupby(age_column):
        for age, row in _df_by_age.iterrows():
            age_stat = ext_feature_mean_statistics.loc[age]
            # collect distributions to be used in extrapolation
            distribs_to_interpolate = []

            distribution_mix_mode = apply_extrapolation_to_raw_datapoints or (
                    age not in ages_raw
            )
            if distribution_mix_mode:
                # define closest raw ages
                dist = pd.Series(abs(ages_raw - age), index=ages_raw)
                n_closest = distrib_count_to_extrapolate
                if age not in ages_raw and n_closest > 1:
                    n_closest -= (
                        1  # as age will have distance 0 and always will be included
                    )
                ages_to_use_for_extrapolation = list(
                    dist.sort_values().index[:n_closest]
                )

                for age1 in ages_to_use_for_extrapolation:
                    age_group1 = df_by_ages.get_group(age1)
                    d2e = Distrib2Extrapolate(data=age_group1[features], age=int(age1))
                    distribs_to_interpolate.append(d2e)
            else:
                d2e = Distrib2Extrapolate(
                    data=df_by_ages.get_group(age)[features], age=int(age)
                )

                # add distribution to extrapolation sequences
                distribs_to_interpolate.append(d2e)

            # GET EXTRAPOLATED DISTRIBUTION
            extrapolated_distribution = RolledCollector.get_extrapolated_distribution(
                distribs_to_interpolate,
                target_distrib_restrictions=feature_restriction,
                target_age=int(age),
                target_mean=age_stat,
                vis=False,
            )

            # add age information and append to df_extrapolated
            extrapolated_distribution[age_column] = age
            extrapolated_distribution = pd.merge(
                extrapolated_distribution,
                row.drop(features).to_frame().T,
                left_on=age_column,
                right_index=True,
            )
            df_extrapolated = pd.concat(
                [df_extrapolated, extrapolated_distribution], ignore_index=True
            )

        # fill NaNs
        df_extrapolated = df_extrapolated.apply(
            lambda x: x.fillna(x.value_counts().index[0]) if len(x.dropna()) > 0 else x
        )

        return df_extrapolated

    def check_extrapolated_rolled_data(
            self, df_initial: pd.DataFrame, df_output: pd.DataFrame
    ):
        """
        check dataset extrapolated datapoints. Some visualization, etc.
        """

        # draw pipes and compare mean values og generated data and initial data

        # calculate error of mean values (not for extrapolated data)

        df_summary = pd.DataFrame()
        df_initial_by_age = (
            df_initial.groupby(self.params.match_index + [self.params.age_column])
            .mean()
            .groupby(self.params.age_column)
            .size()
        )
        df_output_by_age = (
            df_output.groupby(self.params.match_index + [self.params.age_column])
            .size()
            .groupby(self.params.age_column)
            .mean()
        )
        fig_count, ax_count = plt.subplots(2)
        ax_count[0].scatter(df_initial_by_age.index.values, df_initial_by_age)
        ax_count[0].set_xlabel(self.params.age_column)
        ax_count[0].set_title("initial count by day")
        ax_count[1].scatter(df_output_by_age.index.values, df_output_by_age)
        ax_count[1].set_title("output mean count by day")
        ax_count[1].set_xlabel(self.params.age_column)

        plt.show()

        for (g_l, group), (g_o_l, group_output) in zip(
                df_initial.groupby(self.params.match_index),
                df_output.groupby(self.params.match_index),
        ):
            assert g_l == g_o_l

            fig_mean, axes_mean = plt.subplots(len(self.params.features), 1)
            fig_std, axes_std = plt.subplots(len(self.params.features), 1)
            for f_inf, f in enumerate(self.params.features):
                axes_mean[f_inf].plot(
                    group.groupby(self.params.age_column).mean()[f], label="initial"
                )
                axes_mean[f_inf].plot(
                    group_output.groupby(self.params.age_column).mean()[f],
                    marker=".",
                    label="output",
                )
                if f + "_mean" in group.columns:
                    axes_mean[f_inf].plot(
                        group.groupby(self.params.age_column).mean()[f + "_mean"],
                        label="target mean",
                    )
                axes_mean[f_inf].set_title(f)
                axes_mean[f_inf].legend()

                axes_std[f_inf].plot(
                    group.groupby(self.params.age_column).std()[f], label="initial"
                )
                axes_std[f_inf].plot(
                    group_output.groupby(self.params.age_column).std()[f],
                    marker=".",
                    label="output",
                )
                axes_std[f_inf].set_title(f)
                axes_std[f_inf].legend()

            plt.tight_layout()
            plt.show()

        pass

    @staticmethod
    def add_group_label(
            df: pd.DataFrame, index_cols: List[str], label_colname: str = "group_label"
    ):
        """
        Update input df with adding label_colname

        :param df:
        :param indexes:
        :param label_colname:
        :return:
        """
        if not all([c in df.reset_index().columns for c in index_cols]):
            raise ValueError("add_group_label: Not all index_cols are in df")
        df[label_colname] = (
            df[index_cols].astype(str).apply(lambda x: "_".join(x), axis=1)
        )

    def run(
            self, df: pd.DataFrame, summary_df_fname: Optional[str], vis: bool = False
    ) -> pd.DataFrame:
        """
        Use df. for each engine_name/results_postfix group define config. and for each device in subgroup load
        correspondent rolled data. Then this data grouped by track and then reduced to decrease number of samples.

        :param df:
        :return:
        """
        self.logger.info(f"Initial df size: {len(df)}")
        if not os.path.exists(self.params.work_dir):
            os.makedirs(self.params.work_dir)
        # ====================== CHECK ===============================
        unique_indexes = [
            c
            for c in self.params.match_index + [self.params.age_column]
            if c in df.columns
        ]
        assert (
                df.duplicated(unique_indexes).sum() == 0
        ), "Input df has duplicated by match_index columns that are supposed to be unique"

        summary_df = df[unique_indexes].set_index(unique_indexes)
        # ===================== COLLECTING ===========================
        self.logger.info("magenta", "Extending df with rolled")
        extended_df = self.extend_df_with_rolled(
            df,
            index_columns=self.params.match_index,
            age_column=self.params.age_column,
            rolled_age_column=self.params.rolled_age_column,
            features=self.params.features,
            feature_restrictions=self.feature_restrictions,
            engine_name_column=self.params.engine_name_column,
            results_postfix_column=self.params.results_postfix_column,
            rolled_track_id_column=self.params.rolled_track_id_column,
            rolled_sess_id_column=self.params.rolled_sess_id_column,
            gby_track_reliability=self.params.gby_track_reliability,
            keep_mean_values=self.params.keep_mean_values,
            mean_feature_postfix="_mean",
            logger=self.logger,
        )
        # NOTE: AFTER extend_df_with_rolled full GlobalConfig.device_match_columns are in df
        # So, will be used GlobalConfig.device_match_columns instead of self.params.match_index

        summary_df["extended_count"] = extended_df.groupby(unique_indexes).size()
        for f in self.params.features:
            if f in extended_df.columns:
                summary_df[f"extended_{f}_mean"] = extended_df.groupby(
                    unique_indexes
                ).mean()[f]
                summary_df[f"extended_{f}_std"] = extended_df.groupby(
                    unique_indexes
                ).std()[f]
            else:
                logging.warning(f"No {f} in extended_df")
        summary_df[f"extended_{self.params.reduce_target_column}_mean"] = (
            extended_df.groupby(unique_indexes).mean()[self.params.reduce_target_column]
        )
        self.logger.info(f"Extended df size: {len(extended_df)}")

        # ===================== REDUCING =============================
        if self.params.do_reducing:
            try:
                self.logger.info(
                    f"Reducing rolled_df (to {self.params.reduce_target_count} "
                    f"datapoints for each cycle-house-age group)"
                )
                # gby_cols = self.params.match_index + [ self.params.age_column]
                gby_cols = device_match_columns + [self.params.age_column]
                extended_reduced_df = self.reduce_rolled_data(
                    extended_df,
                    gb_columns=gby_cols,
                    reduce_by=self.params.reduce_by,
                    reduce_target_count=self.params.reduce_target_count,
                    reduce_target_column=self.params.reduce_target_column,
                    reduce_round_val=self.params.reduce_round_val,
                    logger=self.logger,
                )
            except Exception as e:
                self.logger.error(f"reduce_rolled_data error: {e}")
                extended_reduced_df = extended_df.copy()
            summary_df["reduced_count"] = extended_reduced_df.groupby(
                unique_indexes
            ).size()
            for f in self.params.features:
                if f in extended_reduced_df.columns:
                    summary_df[f"reduced_{f}_mean"] = extended_reduced_df.groupby(
                        unique_indexes
                    ).mean()[f]
                    summary_df[f"reduced_{f}_std"] = extended_reduced_df.groupby(
                        unique_indexes
                    ).std()[f]
                else:
                    logging.warning(f"No {f} in extended_reduced_df")
            summary_df[f"reduced_{self.params.reduce_target_column}_mean"] = (
                extended_reduced_df.groupby(unique_indexes).mean()[
                    self.params.reduce_target_column
                ]
            )
            self.logger.info(f"Extended reduced df size: {len(extended_reduced_df)}")
        else:
            extended_reduced_df = extended_df.copy()

        # ==================== EXTRAPOLATION =========================
        if self.params.do_extrapolation:

            try:
                self.logger.info(
                    (
                        "magenta",
                        f"Extrapolating reduced_rolled_df in range [0:{max_age}]",
                    )
                )
                extended_reduced_extr_df = self.extrapolate(
                    extended_reduced_df,
                    gby_columns=device_match_columns,
                    # self.params.match_index,
                    features=self.params.features,
                )

            except Exception as e:
                self.logger.error(f"extrapolate error: {e}")
                extended_reduced_extr_df = extended_reduced_df.copy()

            extrap_stat = (
                extended_reduced_extr_df.groupby(unique_indexes)
                .size()
                .to_frame("extended_reduced_extr_df_count")
            )
            summary_df = pd.merge(
                summary_df, extrap_stat, left_index=True, right_index=True, how="outer"
            )
            # summary_df['extended_reduced_extr_df_count'] = extended_reduced_extr_df.groupby(unique_indexes).size()
            for f in self.params.features:
                if f in extended_reduced_df.columns:
                    summary_df[f"extrapolated_{f}_mean"] = (
                        extended_reduced_extr_df.groupby(unique_indexes).mean()[f]
                    )
                    summary_df[f"extrapolated_{f}_std"] = (
                        extended_reduced_extr_df.groupby(unique_indexes).std()[f]
                    )
                else:
                    logging.warning(f"No {f} in extended_reduced_extr_df")

            summary_df[f"extrapolated_{self.params.reduce_target_column}_mean"] = (
                extended_reduced_extr_df.groupby(unique_indexes).mean()[
                    self.params.reduce_target_column
                ]
            )
            self.logger.info(
                f"Extended reduced extrapolated df size: {len(extended_reduced_extr_df)}"
            )

        else:
            extended_reduced_extr_df = extended_reduced_df.copy()

        extended_reduced_extr_df[self.params.age_column] = extended_reduced_extr_df[
            self.params.age_column
        ].astype(int)

        if vis:
            self.check_extrapolated_rolled_data(extended_df, extended_reduced_extr_df)
        if summary_df_fname is not None:
            summary_df.to_csv(summary_df_fname, sep=";")
            self.logger.info(
                f"summary_df was saved to {os.path.abspath(summary_df_fname)}"
            )
        return extended_reduced_extr_df
