import copy
import warnings
from typing import Optional, Union

import numpy as np
import pandas as pd
from loguru import logger

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()
plt = checker.get_module('matplotlib.pyplot')


def adjust_standard_to_values(
        standard: pd.Series,
        initial_values: pd.Series,
        vis,
        smooth_window,
        useFirstStandardValue,
        useLastStandardValue,
        average: int = 1,
        extra_title=False,
        ax: Optional[Union[None, None]] = None,
        color: Optional[Union[str, bool]] = False,
        verbose: bool = False,
        *args,
        **kwargs,
) -> Union[pd.Series, None]:
    """
    Prerequisites:
    standard and values objects may not have the same length but avoid using duplicates in both -
        - it may lead to subtle errors
    standard values should be filled with no empty data in the index: if your last index (age) in the pd.Series object
        is 45 - your length must be 46 (remember: we're counting from 0).

    Adjust any standard curve to any values. Make curve pass through points. if smooth_window=1,
    all initial values will be keeped

    :param standard: standard curve with age as index
    :param initial_values: aim values with age as index
    :param vis: do visualization
    :param smooth_window: smooth your time series. Set 1 if you want to keep initial data points as they were
    :param useFirstStandardValue: if value for first point is absent, use standard value
    :param useLastStandardValue: if value for last point is absent, use standard value
    :param average: the number of previous days it should use (as a maximum possible)
    to get average of approximated time series. For example, You could use 30 as the last index in the values
    and then it will try to check if there's ages (indices) from 30-average to 30 in your values.index
    and from them interpolate.
    Interpolating behaviour:
        if it counts non-null more than 2 last days within range [last_values_day - average, average] -
            - it will take the median from interpolated lines
        if it counts non-null 2 last days within range [last_values_day - average, average] -
            - it will take the mean and you'll get the warning
        if it counts only 1 last day within range [last_values_day - average, average] -
            - it will use only the 1 curve (mean operation on the same time series) and you also get the warning
    :param ax: if you would like to plot it on some matplotlib axes object
    :param color: just to use matplotlib color for curve
    :return: pd.Series, updated curve
    """
    _interpolation_method: str = "linear"

    if initial_values is None:
        logger.info("values are None")
        return None
    if standard is None:
        logger.info("standard are None")
        return None

    values = copy.deepcopy(initial_values)
    values = values.dropna()
    # sort values by time index !
    values = values.sort_values(ascending=True)
    start_day = standard.index[0]

    end_day = standard.index[-1]
    # max_age = values.dropna().index[-1]
    # TODO: assert for `values.loc[start_day]` being non-null (via pd.isnull)
    if start_day not in values.index:
        if useFirstStandardValue:
            values.loc[start_day] = standard[start_day]
            values = values.sort_index()
        else:
            first_values_day = values.index[0]
            # TODO: assert for being non-null
            coef = standard[first_values_day] / values[first_values_day]
            values.loc[start_day] = standard[start_day] / coef
            values = values.sort_index()

    if useLastStandardValue:
        values.loc[end_day] = standard[end_day]
        values = values.sort_index()

    working_df = standard.to_frame("standard")
    working_df["standard"].combine_first(standard.rolling(5, center=True).mean())

    working_df["diff"] = working_df["standard"] - values
    # TODO: `0` divided by `0` == infinite so for any "relative" feature
    #   add machine epsilon: np.finfo(float).eps
    # === old code ===
    # working_df["diff_proc"] = (values - working_df["standard"]) / working_df["standard"]
    # === new code ===
    machine_eps: float = np.finfo(float).eps
    working_df["diff_proc"] = (values - working_df["standard"] + machine_eps) / (
            working_df["standard"] + machine_eps
    )
    # TODO: insert here interpolation using cycles: # DONE
    # TODO: add assertion for empty df since you're dealing with dropna.tail(n=1)
    if average > 1:
        # get the last "average" values:
        # last_values_for_averaging = working_df['diff'].dropna().tail(n=5)
        last_day = working_df["diff"].dropna().tail(n=1).index.item()  # .age
        # initial_values
        last_values_for_averaging = working_df["diff"][
            working_df.index <= last_day
            ].tail(n=average)
        # last_values_for_averaging = initial_values[initial_values.index <= last_day].tail(n=average)

        last_values_df = last_values_for_averaging.reset_index()
        last_values_df.columns = ["age", "diff"]

        if len(last_values_df) < average:
            warning_message = (
                    f"You have less last values ({len(last_values_df)} including dropna()"
                    + f"than set to use for averaging: {average}. This may lead to incorrect results"
            )
            warning_message += f"\nLast values are: {', '.join([str(i) for i in last_values_for_averaging.round(5).values])}. "
            warning_message += (
                f"Check if the last at least two values have the same tendency"
            )

        non_null_days = 0
        for row_num, row in last_values_df.iterrows():
            # get current age
            current_age = row.age
            # current_value = row['diff'].item()
            # TODO: check how pd.isnull will work
            if pd.isnull(row["diff"]) or current_age != (
                    last_day - average + row_num + 1
            ):
                continue
            # set all working_df['diff'] with index > current_age to np.nan:
            current_diff = working_df["diff"].copy()
            current_diff[current_diff.index > current_age] = np.nan
            # the same for diff_proc
            current_diff_proc = working_df["diff_proc"].copy()
            current_diff_proc[current_diff_proc.index > current_age] = np.nan

            working_df[f"diff_{row_num}"] = current_diff.interpolate(
                _interpolation_method
            )
            working_df[f"diff_proc_{row_num}"] = current_diff_proc.interpolate(
                _interpolation_method
            )
            non_null_days += 1
        # then aggregate all values:
        # logger.info("+")
        # TODO: mean with 2, median 3+
        # TODO: for non_null_days (if there's enough values (>= 2?)) to input as average #min_non_null_values_count
        if non_null_days > 1:
            if non_null_days > 2:
                working_df["diff"] = working_df.filter(regex="^diff_\d").median(axis=1)
                working_df["diff_proc"] = working_df.filter(
                    regex="^diff_proc_\d"
                ).median(axis=1)
            else:
                # warning_message = f"There's only non_null days satisfying condition " + \
                #                   f"{last_day - average + 1} <= age <= {last_day}. Will use mean instead of median"
                # warnings.warn(warning_message, category=UserWarning)
                working_df["diff"] = working_df.filter(regex="^diff_\d").mean(axis=1)
                working_df["diff_proc"] = working_df.filter(regex="^diff_proc_\d").mean(
                    axis=1
                )
        else:
            warning_message = (
                f"There's no non_null_days while checking. Will use initial one"
            )
            warnings.warn(warning_message, category=UserWarning)
            working_df["diff"] = working_df["diff"].interpolate(_interpolation_method)
            working_df["diff_proc"] = working_df["diff_proc"].interpolate(
                _interpolation_method
            )
    else:
        working_df["diff"] = working_df["diff"].interpolate(_interpolation_method)
        working_df["diff_proc"] = working_df["diff_proc"].interpolate(
            _interpolation_method
        )

    if smooth_window > 2 and smooth_window % 2 == 1:
        try:
            working_df["diff_proc"] = (
                working_df["diff_proc"]
                .rolling(smooth_window, center=True, min_periods=1)
                .mean()
            )

        except Exception as E:
            if verbose:
                warnings.warn(
                    f"Failed .rolling on series with exception: {E}",
                    category=RuntimeWarning,
                )

            shifts = int(np.floor(smooth_window / 2))
            indices = working_df["diff_proc"].iloc[shifts:-shifts].index
            working_df["diff_proc"].loc[indices] = (
                working_df["diff_proc"]
                .rolling(smooth_window, center=True, min_periods=1)
                .mean()
                .shift(-shifts)
                .loc[indices]
            )

    working_df["adjusted_standard"] = (
            working_df["standard"] * working_df["diff_proc"] + working_df["standard"]
    )
    # TODO: what is it supposed to be? why we assign initial values and do some strange check only up to 20 day?
    #   make a comment on it (now it's commented since it has no sense):
    # working_df['initial'] = initial_values
    # if sum(working_df.loc[:20,'initial'] - working_df.loc[:20,'adjusted_standard'])>0:
    #     pass

    return working_df["adjusted_standard"]
