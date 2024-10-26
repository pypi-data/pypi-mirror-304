import warnings
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')

from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values
from bdm2.constants.global_setup.data import (
    max_age,
    standards_match_columns,
    device_match_columns,
)
from bdm2.utils.process_data_tools.components.rolleds.restrictions import (
    global_feature_restrictions,
)
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import (
    PostgresActualClientsInfoStorage,
)
from bdm2.constants.global_setup.data_columns import age_column


@dataclass
class ExtrapolationParams:
    extrapolate_columns: list = field(default_factory=lambda: [])
    extrapolate_column_name: str = (
        ""  # TODO deprecate. but required for old experiments
    )
    age_column_name: str = age_column

    simple_extrapolation_ending_save_gap: int = 5

    # update models
    train_model: bool = False
    model_fname: str = r"volume_autoencoder.net"
    encoder_model_fname: str = r"volume_encoder.net"
    decoder_model_fname: str = r"volume_decoder.net"
    model_config: str = "10-3-10"
    split_model: bool = True

    postfix_after_simple_extrapolate: str = "_simple_extrapolate"
    postfix_after_autoencoder: str = "_autoencoded"
    postfix_raw: str = "_raw"

    freeze_columns: bool = True

    # postprocessing
    extrapolation_min_age: int = 0
    extrapolation_max_age: int = max_age
    smooth_window: int = 7
    use_autoencoder: bool = False
    vis: bool = False

    use_different_smooths: bool = False
    smooth_params: dict = field(default_factory=lambda: {})

    # TODO: Deprecated. All useges are out of module. no need to be inited in module

    extrapolated_df_fname: str = ""
    extrapolated_df_train_fname: str = ""
    extrapolated_df_test_fname: str = ""

    extrapolated_df_train_replaced: str = ""
    extrapolated_df_fname_train: str = ""
    # TODO: all above


class DataExtrapolatorMulti:
    def __init__(
            self,
            config: ExtrapolationParams,
            logger: Optional,
            statistics_storage: PostgresActualClientsInfoStorage,
    ):
        self.config = config
        self.statistics_storage = statistics_storage
        self.logger = logger

    def define_available_features(self, postfix: str = "") -> List[str]:
        return [x + postfix for x in global_feature_restrictions]

    def define_statistics(
            self, df: pd.DataFrame
    ) -> Dict[Tuple, Optional[pd.DataFrame]]:
        # ============== DEFINE STATISTICS FOR INTERPOLATION ====================================================
        # define features, that need to be extrapolated.
        self.logger.info(
            f"statistics_storage: {self.statistics_storage.__class__.__name__}"
        )
        standards: Dict[Tuple, Optional[pd.DataFrame]] = {}
        for (client, breed_type, gender), _ in df.groupby(standards_match_columns):

            available_statistics = self.statistics_storage.get_actual_statistics(
                client=client, breed_type=breed_type, gender=gender
            )

            available_st_weights = self.statistics_storage.get_actual_weights_standard(
                client=client, breed_type=breed_type, gender=gender
            )
            if available_statistics is None:
                available_statistics = self.statistics_storage.get_default_statistics()
                self.logger.info(
                    f"for {(client, breed_type, gender)} DEFAULT statistics will be used"
                )
            else:
                self.logger.info(
                    f"for {(client, breed_type, gender)} ACTUAL statistics will be used"
                )

            available_statistics["Weights"] = available_st_weights["Weights"]
            standards[(client, breed_type, gender)] = available_statistics
        return standards

    def prepare_temp_device_df(self, df_temp: pd.DataFrame) -> pd.DataFrame:
        df_temp = df_temp.set_index(self.config.age_column_name).reindex(
            range(self.config.extrapolation_min_age, self.config.extrapolation_max_age)
        )
        return df_temp

    def check_columns(self, df: pd.DataFrame, columns: list = None):
        if columns is not None:
            columns_temp = [x for x in columns if x in df.columns]
            if not len(columns_temp):
                raise KeyError(f"Invalid columns for dataset! Missing: {columns}")
            if len(columns_temp) < len(columns):
                diff = set(columns).difference(set(columns_temp))
                self.logger.warning(
                    f"Not all columns ind dataset columns for extrapolation. Missing: {diff}"
                )
                columns = columns_temp.copy()

        else:
            columns = [
                x
                for x in df.columns
                if x in self.define_available_features()
                   or x in self.define_available_features("_mean")
                   or "mass" in x
            ]

        if not len(columns):
            err_msg: str = (
                "Check the columns of the dataset. No extrapolation data found"
            )
            raise KeyError(err_msg)
        return columns

    def extrapolate_simple(
            self, df: pd.DataFrame, columns: list = None
    ) -> (pd.DataFrame, List):
        standards = self.define_statistics(df)

        df_output = df.iloc[:0].copy()

        # get active indexes
        active_indexes = list(
            set(device_match_columns)
            .intersection(df.reset_index().columns)
            .union(standards_match_columns)
        )

        for device, device_df in df.groupby(active_indexes):
            device_info = pd.Series(device, index=active_indexes)
            self.logger.info(f"Processing {device}")
            df_temp = self.prepare_temp_device_df(
                device_df
            )  # return df with full age range, age as index!!!
            flag_completeness: bool = True
            for column in columns:
                data_to_extrapolate = self.prepare_device_data(
                    device_df, column
                ).sort_index()
                if data_to_extrapolate.empty:
                    self.logger.warning(
                        f"Could not prepare data for extrapolation: {column}"
                    )
                    # flag_completeness = False
                    continue

                extrapolated = self.extrapolate_simple_device_data_column(
                    data_to_extrapolate, standards, device_info
                )
                if extrapolated.empty:
                    self.logger.warning(
                        f"Could not extrapolate data: {column}. Maybe no statistics for this feature"
                    )
                    # flag_completeness = False
                    continue

                df_temp[column] = extrapolated.copy()
            if flag_completeness:
                df_temp = df_temp.apply(
                    lambda x: (
                        x.fillna(x.value_counts().index[0])
                        if len(x.dropna()) > 0
                        else x
                    )
                )
                df_temp = df_temp.reset_index()  # reset index that is age
                df_output = pd.concat(
                    [df_output, df_temp.reset_index()], ignore_index=False
                )

        return df_output, columns

    def prepare_device_data(self, device_df: pd.DataFrame, column: str) -> pd.Series:

        data_to_extrapolate: pd.Series = device_df.reset_index().set_index(
            self.config.age_column_name
        )[column]
        if np.isnan(data_to_extrapolate.values).all(axis=0).item():
            warn_msg: str = f"encountered all nan values for feature={column}"
            self.logger.warning(warn_msg)
            return pd.Series(dtype=float)

        return data_to_extrapolate

    def spline(
            self, input_data: pd.Series, smooth_window: int, device_info: pd.Series
    ) -> pd.Series:
        # Do simple extrapolation
        name = str(input_data.name)
        if input_data.name in self.define_available_features(postfix="_mean"):
            name = name.split("_mean")[0]

        # min_range_y = global_feature_restrictions[name].min_value
        max_range_y = global_feature_restrictions[name].max_value
        if global_feature_restrictions[name].shift_to_target:
            return pd.Series(dtype=float)

        feature_mean_statistics_not_na = input_data.dropna()
        index = list(
            range(self.config.extrapolation_min_age, self.config.extrapolation_max_age)
        )

        ser = pd.Series([max_range_y] * self.config.extrapolation_max_age, index=index)
        if ser.index.max() < input_data.index.max():
            warnings.warn(
                f"adjust_standard_to_values could not work when standard is shorter then input_data. "
                f"max index for input_data: {input_data.index.max()}, "
                f"max index for standard: {ser.index.max()}. "
                f"To fix it, change ExtrapolationParams.extrapolation_max_age for higher value"
            )
        extrapolated = adjust_standard_to_values(
            ser,
            input_data,
            vis=self.config.vis,
            smooth_window=smooth_window,
            useFirstStandardValue=False,
            useLastStandardValue=False,
            average=self.config.simple_extrapolation_ending_save_gap,
            extra_title=str(device_info.values),
        )

        # s = scipy.interpolate.InterpolatedUnivariateSpline(x=feature_mean_statistics_not_na.index.values,
        #                                                    y=feature_mean_statistics_not_na.values,
        #                                                    k=1, bbox=[])
        # extrapolated = s(index)
        # extrapolated = pd.Series(extrapolated, index=index, name=input_data.name)
        # if smooth_window > 2 and smooth_window % 2 == 1:
        #     extrapolated = extrapolated.rolling(
        #         smooth_window,
        #         min_periods=1,
        #         center=True).mean()
        # extrapolated[extrapolated < min_range_y] = min_range_y
        # extrapolated[extrapolated > max_range_y] = max_range_y

        # plt.figure()
        # plt.scatter(input_data.index, input_data.values, label="raw values", c="orange")
        # plt.plot(extrapolated.index, extrapolated.values, label="spline", c="orange")
        return extrapolated

    def extrapolate_simple_device_data_column(
            self, data_to_extrapolate: pd.Series, standards: dict, device_info: pd.Series
    ):
        standard_series: pd.Series = pd.Series(dtype=float)
        # initial_index_cols = [c for c in device_df.index.names if c is not None]

        smooth_window = self.config.smooth_window  # global_feature_restrictions[
        # str(data_to_extrapolate.name).split("_mean")[0]].mean_values_smooth_window
        index = tuple(device_info[standards_match_columns])
        if "mass" in data_to_extrapolate.name and index in standards:
            standard_series = standards[index]["Weights"]
        elif (
                data_to_extrapolate.name in self.define_available_features()
                or data_to_extrapolate.name in self.define_available_features("_mean")
        ):

            # if feature not in index or something simular
            if (
                    index in standards
                    and data_to_extrapolate.name in standards[index].columns
            ):
                # check if we can execute standart extrapolation
                standard_series = standards[index][data_to_extrapolate.name]
        else:
            return pd.Series(dtype=float)

        if standard_series.empty:
            extrapolated = self.spline(data_to_extrapolate, smooth_window, device_info)

        else:
            extrapolated = adjust_standard_to_values(
                standard_series,
                data_to_extrapolate,
                vis=self.config.vis,
                smooth_window=smooth_window,
                useFirstStandardValue=False,
                useLastStandardValue=False,
                average=self.config.simple_extrapolation_ending_save_gap,
                extra_title=str(device_info.values),
            )

        if self.config.vis:
            plt.show()
        if not extrapolated.empty:
            extrapolated = extrapolated.loc[
                           self.config.extrapolation_min_age: self.config.extrapolation_max_age
                           ]
            extrapolated.index.name = self.config.age_column_name

        return extrapolated

    def add_freeze_columns(
            self, collected_df: pd.DataFrame, df: pd.DataFrame, columns: list
    ) -> pd.DataFrame:
        index = [c for c in df.index.names if c is not None]
        if len(index):
            df_temp = df.reset_index()
            collected_df_temp = collected_df.reset_index()
        else:
            df_temp = df.copy()
            collected_df_temp = collected_df.copy()

        match_index = [
            c
            for c in device_match_columns + [self.config.age_column_name]
            if c in df_temp
        ]

        df_temp.set_index(match_index, inplace=True)
        collected_df_temp.set_index(match_index, inplace=True)

        for column in columns:
            df_temp[column + self.config.postfix_raw] = collected_df_temp[column].copy()

        df_temp.reset_index(inplace=True)
        if len(index):
            df_temp.set_index(index, inplace=True)
        return df_temp

    def run(self, df: pd.DataFrame, columns: list = None):
        if df.empty:
            self.logger.info(f"df to extrapolate is empty")
            self.logger.info(f"df to extrapolate is empty")
            return df

        self.logger.info("RUN simple extrapolate")
        index_names = [c for c in df.index.names if c is not None]
        if len(index_names):
            loc_df = df.reset_index()
        else:
            loc_df = df.copy()
        columns = self.check_columns(df=loc_df, columns=columns)
        df_simple_extrapolated, columns = self.extrapolate_simple(
            df=df, columns=columns
        )
        if self.config.freeze_columns:
            self.logger.info("USE freeze columns")
            df_simple_extrapolated = self.add_freeze_columns(
                collected_df=df, df=df_simple_extrapolated, columns=columns
            )
        if len(index_names):
            df_simple_extrapolated.set_index(index_names, inplace=True)

        return df_simple_extrapolated
