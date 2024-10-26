import warnings
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')

from bdm2.constants.global_setup.data import device_match_columns
from bdm2.constants.global_setup.data_columns import (
    min_chicken_count_column,
    usable_for_train_column,
    tilt_column,
    missing_column,
)
from bdm2.logger import build_logger


class FiltrationColumns:
    min_chicken_column_name: str = min_chicken_count_column
    usable_for_train_column_name: str = usable_for_train_column
    tilt_column_name: str = tilt_column
    missing_column_name: str = missing_column


@dataclass
class FiltrationParams(FiltrationColumns):
    work_dir: str
    need_filter_by_std: bool
    need_filter_absent_target: bool
    need_only_usable_for_train: bool
    need_filter_by_reliability: bool
    target_feature_name_for_filtration: str
    filtration_by_std_gby: List[str]
    min_chicken_count: int = 0
    filter_std_interval: float = 1.0
    rolling_window: int = 5
    min_target_houses_count: int = 8
    mean_derivative_impact_coef: float = 0.3
    tilt_max_value: float = 3.0
    missing_max_value: float = 0.1
    reliability_min_value: float = 0.5
    reliability_columns: List[str] = field(default_factory=lambda: [])
    min_house_datapoints_to_drop: float = 7
    min_raw_max_age_to_extrapolate: float = 20
    summary_fname: str = "filtration_summary.csv"
    critical_filters: List[Dict[str, Any]] = field(default_factory=lambda: [])


class DataFilter:
    def __init__(
            self,
            filtration_params: FiltrationParams,
            age_column_name: str,
            logger: Optional[Logger] = None,
            vis: bool = False,
    ):
        self.filtration_params = filtration_params
        self.vis = vis
        self.age_column_name = age_column_name
        if logger is None:
            logger = build_logger(build_logger(file_name=f"{Path(__file__)}", save_log=False))
        self.logger: Logger = logger

        work_dir_path = Path(self.filtration_params.work_dir)
        if not work_dir_path.exists():
            work_dir_path.mkdir()
            self.logger.info(f"{self.filtration_params.work_dir} was created")

    def filter_by_target_density_stdev(self, df: pd.DataFrame) -> pd.DataFrame:
        loc_df = df.reset_index() if None not in pd.Index(df.index).names else df.copy()
        df_output = pd.DataFrame(df.iloc[:0])

        for label, f_group in loc_df.groupby(
                self.filtration_params.filtration_by_std_gby
        ):
            means = (
                f_group.sort_values(self.age_column_name)[
                    [
                        self.age_column_name,
                        self.filtration_params.target_feature_name_for_filtration,
                    ]
                ]
                .rolling(
                    self.filtration_params.rolling_window,
                    on=self.age_column_name,
                    center=True,
                    min_periods=1,
                )
                .mean()
                .groupby(self.age_column_name)
                .mean()[self.filtration_params.target_feature_name_for_filtration]
            )
            stdevs = (
                f_group.sort_values(self.age_column_name)[
                    [
                        self.age_column_name,
                        self.filtration_params.target_feature_name_for_filtration,
                    ]
                ]
                .rolling(
                    self.filtration_params.rolling_window,
                    on=self.age_column_name,
                    center=True,
                    min_periods=1,
                )
                .std()
                .groupby(self.age_column_name)
                .mean()[self.filtration_params.target_feature_name_for_filtration]
            )
            means_diff = means.rolling(
                self.filtration_params.rolling_window, center=True, min_periods=1
            ).std()

            std_weights = (
                    1
                    - (means_diff - means_diff.min())
                    / (means_diff.max() - means_diff.min())
                    * self.filtration_params.mean_derivative_impact_coef
            )
            f_group_f = f_group[
                (
                        f_group[self.filtration_params.target_feature_name_for_filtration]
                        > (
                                means[f_group[self.age_column_name]]
                                - self.filtration_params.filter_std_interval
                                * stdevs[f_group[self.age_column_name]]
                                * std_weights[f_group[self.age_column_name]]
                        )
                )
                & (
                        f_group[self.filtration_params.target_feature_name_for_filtration]
                        < (
                                means[f_group[self.age_column_name]]
                                + self.filtration_params.filter_std_interval
                                * stdevs[f_group[self.age_column_name]]
                                * std_weights[f_group[self.age_column_name]]
                        )
                )
                ]
            df_output = pd.concat([df_output, f_group_f])
        return df_output

    def filter_by_min_device_datapoints(
            self, df: pd.DataFrame, count_by_columns: List[str] = device_match_columns
    ) -> pd.DataFrame:
        loc_df = (
            df.reset_index()
            if len([c for c in df.index.names if c is not None])
            else df.copy()
        )

        valuable_devices_by_count = (
                loc_df.groupby(count_by_columns).count()
                > self.filtration_params.min_house_datapoints_to_drop
        ).max(axis=1)
        valuable_devices_by_count = valuable_devices_by_count[
            valuable_devices_by_count == True
            ]
        valuable_devices_by_max_age = (
                loc_df.groupby(count_by_columns).max()[self.age_column_name]
                > self.filtration_params.min_raw_max_age_to_extrapolate
        )
        valuable_devices_by_max_age = valuable_devices_by_max_age[
            valuable_devices_by_max_age == True
            ]
        union_valuable_index = valuable_devices_by_count.index.intersection(
            valuable_devices_by_max_age.index
        )

        output_df = (
            loc_df.set_index(count_by_columns).loc[union_valuable_index].reset_index()
        )
        initial_index_names = [c for c in df.index.names if c is not None]
        if len(initial_index_names):
            output_df = output_df.set_index(initial_index_names)
        return output_df

    def visualize_filtered_data(
            self, df: pd.DataFrame, df_filtered: pd.DataFrame, title: str = "Filtering"
    ):
        plt.figure()
        plt.subplot(211)
        target_ages = [7, 14, 21, 28, 35]
        df_mean = df.groupby(self.age_column_name).mean()
        plt.scatter(
            df[self.age_column_name].values,
            df[self.filtration_params.target_feature_name_for_filtration].values,
            label="full",
        )
        plt.plot(
            df_mean[self.age_column_name].values,
            df_mean[self.filtration_params.target_feature_name_for_filtration].values,
        )

        df_filtered_mean = df_filtered.groupby(self.age_column_name).mean()
        plt.scatter(
            df_filtered[self.age_column_name].values,
            df_filtered[
                self.filtration_params.target_feature_name_for_filtration
            ].values,
            label="after filtering",
        )
        plt.plot(
            df_filtered_mean[self.age_column_name].values,
            df_filtered_mean[
                self.filtration_params.target_feature_name_for_filtration
            ].values,
        )

        filt_diff = (
                            df_filtered_mean.set_index(self.age_column_name)[
                                self.filtration_params.target_feature_name_for_filtration
                            ]
                            - df_mean.set_index(self.age_column_name)[
                                self.filtration_params.target_feature_name_for_filtration
                            ]
                    ).abs() / df_mean[self.filtration_params.target_feature_name_for_filtration]
        mean_abs_diff = round(100 * filt_diff.mean(), 1)

        for a in target_ages:
            plt.axvline(a)

        plt.xlabel(self.age_column_name)
        plt.ylabel(self.filtration_params.target_feature_name_for_filtration)
        plt.grid(True)
        plt.ylim(0)
        plt.title(f"{title}. mean diff: {mean_abs_diff}%")
        plt.legend()
        plt.tight_layout()

        plt.subplot(212)
        check_filtration_gb = ["farm", "breed_type", "gender"]
        farms_count_raw = df.groupby(check_filtration_gb).count()[
            self.filtration_params.target_feature_name_for_filtration
        ]
        farms_count_filter = df_filtered.groupby(check_filtration_gb).count()[
            self.filtration_params.target_feature_name_for_filtration
        ]
        filter_percent_by_farm = (1 - farms_count_filter / farms_count_raw).to_frame(
            name="percent"
        )
        filter_percent_by_farm["label"] = list(
            map(lambda x: "_".join(x), filter_percent_by_farm.index)
        )
        plt.scatter(
            filter_percent_by_farm["label"], filter_percent_by_farm["percent"] * 100
        )
        plt.title(f"percent of filtered datapoints by farm")
        plt.ylabel("percent of filtered datapoints , %")
        plt.xticks(rotation=90)
        plt.axhline(50, c="r", label="critical value for warning")
        plt.ylim(0, 100)
        plt.legend()
        plt.tight_layout()

        to_much_filtration = filter_percent_by_farm[
            filter_percent_by_farm["percent"] > 0.5
            ]
        for f in to_much_filtration.index:
            warnings.warn(
                f'{f} filtered too much ({to_much_filtration.loc[f, "percent"] * 100:.1f}%)'
            )

    def filter_by_min_count(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.filtration_params.min_chicken_count != 0:
            if not len(df):
                self.logger.error("all data filtered previously by other params!\n"
                                  "could not filter by min_chicken_count, len(dataset=0)!")
            return df[df[FiltrationColumns.min_chicken_column_name]
                      >= self.filtration_params.min_chicken_count]

        else:
            self.logger.info(
                f"Filtration by min count will be skipped"
            )
            return df

    def filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info(f"initial {len(df)} records in df")
        if self.filtration_params.need_filter_by_std:
            df = self.filter_by_target_density_stdev(df)
            self.logger.info(
                f"filtration by target density stdev is done. {len(df)} records left"
            )

        if self.filtration_params.need_filter_absent_target:
            df = df[
                ~df[self.filtration_params.target_feature_name_for_filtration].isna()
            ]
            self.logger.info(f"absent target filtering is done. {len(df)} records left")

        if self.filtration_params.need_only_usable_for_train:
            if self.filtration_params.usable_for_train_column_name in df.columns:
                df = df[df[self.filtration_params.usable_for_train_column_name]]
                self.logger.info(
                    f"only usable for train filtering is done. {len(df)} records left"
                )
            else:
                self.logger.info(
                    f"WARNING! {self.filtration_params.usable_for_train_column_name}"
                    f" not in df.columns! Filtration by usability will be skipped"
                )

        if self.filtration_params.need_filter_by_reliability:
            reliable = df[self.filtration_params.reliability_columns].sum(axis=1) / len(
                self.filtration_params.reliability_columns
            )
            df = df[reliable >= self.filtration_params.reliability_min_value]
            self.logger.info(f"filter by reliability is done. {len(df)} records left")

        if len(self.filtration_params.critical_filters):
            for critical_filter in self.filtration_params.critical_filters:
                for col, condition in critical_filter.items():
                    df = df.query(f"{col} {condition}")
                    self.logger.info(
                        f"filtration by critical filter: {col} {condition} is done. {len(df)} records left"
                    )

        df = self.filter_by_min_device_datapoints(df)
        self.logger.info(
            f"min house datapoints filtering is done. {len(df)} records left"
        )
        df = self.filter_by_min_count(df)
        self.logger.info(f"min count filtering is done. {len(df)} records left")

        if self.vis:
            self.visualize_filtered_data(df)

        return df
