import logging

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'scipy.stats',
    # 'numpy',
    # 'pandas',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

# np = checker.get_module('numpy')
# pd = checker.get_module('pandas')
stats = checker.get_module('scipy.stats')

import numpy as np
import pandas as pd
# import scipy.stats

from typing import Tuple, List, Dict, Any, Optional, Union
from bdm2.data_handling.generated_data.features_stats.components.common.utils import extract_feature_settings
from bdm2.data_handling.generated_data.features_stats.components.const.names import StatisticsColumnsConstants
from bdm2.data_handling.generated_data.features_stats.components.common.general import ExtraFeatures

# Constants
_DEFAULT_IQR_PERCENTILES: List[int] = [25, 75]
_DEFAULT_PERCENTILE_IQR_SHIFT: float = 1.5


def iqr_range(values: np.ndarray,
              percentiles: Optional[List[int]] = None,
              boundary_shift: float = _DEFAULT_PERCENTILE_IQR_SHIFT) -> Tuple[float, float]:
    """
    Calculate the interquartile range (IQR) and bounds based on the given percentiles and boundary shift.

    :param values: Array of values to calculate IQR.
    :param percentiles: List of percentiles for IQR calculation.
    :param boundary_shift: Factor to shift the IQR for boundary calculation.
    :return: Tuple containing the lower and upper bounds.
    """
    percentiles = percentiles or _DEFAULT_IQR_PERCENTILES
    q1, q3 = np.percentile(values, percentiles)
    iqr = q3 - q1
    lower_range = q1 - (boundary_shift * iqr)
    upper_range = q3 + (boundary_shift * iqr)
    return lower_range, upper_range


def iqr_range_from_dist(distribution: stats.rv_continuous,
                        percentiles: Optional[List[int]] = None,
                        boundary_shift: float = _DEFAULT_PERCENTILE_IQR_SHIFT) -> Tuple[float, float]:
    """
    Calculate the IQR and bounds based on a probability distribution.

    :param distribution: scipy.stats distribution object.
    :param percentiles: List of percentiles for IQR calculation.
    :param boundary_shift: Factor to shift the IQR for boundary calculation.
    :return: Tuple containing the lower and upper bounds.
    """
    percentiles = percentiles or _DEFAULT_IQR_PERCENTILES
    q1 = distribution.ppf(percentiles[0] / 100)
    q3 = distribution.ppf(percentiles[1] / 100)
    iqr = q3 - q1
    lower_range = q1 - (boundary_shift * iqr)
    upper_range = q3 + (boundary_shift * iqr)
    return lower_range, upper_range


def use_interpolation(stdev_coef,
                      spline_order,
                      min_stdev_percent,
                      interpolated_mean,
                      rolling_window):
    stdev_coef = stdev_coef.interpolate(method='spline', order=spline_order, limit_direction="both")
    stdev_coef[stdev_coef < min_stdev_percent] = min_stdev_percent
    interpolated_stdev = interpolated_mean * stdev_coef
    interpolated_stdev = interpolated_stdev.rolling(rolling_window * 2, center=True, min_periods=1).mean()
    interpolated_stdev = interpolated_stdev.rolling(rolling_window * 2, center=True, min_periods=1).mean()

    return interpolated_stdev


def interpolate_stat_df(features: List[ExtraFeatures], stat_df: pd.DataFrame,
                        spline_order: int = 2, rolling_window: int = 7,
                        min_stdev_percent: float = 0.1) -> pd.DataFrame:
    """
    Interpolate and smooth statistical data in a DataFrame.

    :param features: List of ExtraFeatures objects.
    :param stat_df: DataFrame containing statistical data.
    :param spline_order: Order of spline interpolation.
    :param rolling_window: Window size for rolling average smoothing.
    :param min_stdev_percent: Minimum standard deviation as a percentage.
    :return: DataFrame with interpolated and smoothed statistics.
    """
    for feature in features:
        feature_name = feature.name
        mean_col = f"{feature_name}_mean"
        stdev_col = f"{feature_name}_stdev"

        if mean_col not in stat_df.columns:
            print(f"{feature_name} is not in statistics")
            continue

        # Interpolate and smooth mean
        interpolated_mean = stat_df[mean_col].interpolate(method='spline', order=spline_order, limit_direction="both")
        interpolated_mean = interpolated_mean.rolling(rolling_window, center=True, min_periods=1).mean()
        stat_df[mean_col] = interpolated_mean

        # Calculate and smooth standard deviation
        stdev_coef = stat_df[stdev_col] / interpolated_mean

        interpolated_stdev = use_interpolation(stdev_coef,
                                               spline_order,
                                               min_stdev_percent,
                                               interpolated_mean,
                                               rolling_window)
        stat_df[stdev_col] = interpolated_stdev

        # Add filterable status
        stat_df[f"{feature_name}_filterable"] = int(feature.isFilterable)

    return stat_df


def negative_check(df: pd.DataFrame,
                   logger: logging.Logger,
                   interpolate_params: Optional[Dict[str, Any]] = None,
                   cols_to_check: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Check and replace negative values in the DataFrame.

    :param df: DataFrame to check.
    :param logger: Logger for logging warnings and errors.
    :param interpolate_params: Parameters for interpolation.
    :param cols_to_check: List of columns to check for negative values.
    :return: DataFrame with negative values replaced.
    """
    df = df.copy()
    cols_to_check = cols_to_check or list(df.columns)
    default_params = {
        'method': "polynomial",
        'order': 3,
        'limit_direction': "both",
        'downcast': "infer"
    }
    interpolate_params = interpolate_params or default_params

    for col in cols_to_check:
        if col not in df.columns:
            logger.warning(f"Column {col} does not exist in DataFrame")
            continue

        if (df[col] < 0).any():
            # Replace negative values with NaN and interpolate
            df[col] = df[col].apply(lambda x: np.nan if x < 0 else x)
            df[col] = df[col].interpolate(**interpolate_params)

            # Handle any remaining NaN values
            if df[col].isna().any():
                df[col] = df[col].bfill()

            # Ensure there are no remaining negative values
            if (df[col] < 0).any():
                df[col] = df[col].bfill()
                logger.error(f"Column {col} still contains negative values after interpolation")

            logger.warning(f"Column {col} had negative values replaced")

    return df


def out_of_bounds_check(df: pd.DataFrame,
                        logger: logging.Logger,
                        features: List[str],
                        features_settings: Any,
                        min_acceptable_value: float = 1e-6,
                        max_acceptable_value: Optional[float] = None) -> pd.DataFrame:
    """
    Check for values out of bounds and adjust as necessary.

    :param df: DataFrame to check.
    :param logger: Logger for logging warnings and errors.
    :param features: List of feature names to check.
    :param features_settings: Settings for features.
    :param min_acceptable_value: Minimum acceptable value for adjustments.
    :param max_acceptable_value: Maximum acceptable value for adjustments (not used in current implementation).
    :return: DataFrame with adjusted values.
    """
    df = df.copy()
    for feature in features:
        settings = extract_feature_settings(features_settings, feature)
        if settings is None or not settings.get("adapt", True):
            logger.info(f"Skipping out-of-bounds check for feature {feature} due to adapt == False")
            continue

        try:
            mean_col = f"{feature}_mean"
            stdev_col = f"{feature}_stdev"
            lstdev_col = f"{feature}_lstdev_coef"

            left_bound = df[mean_col] - df[lstdev_col] * df[stdev_col]
            decision_mask = left_bound < min_acceptable_value

            if decision_mask.any():
                logger.warning(f"Feature {feature} has {decision_mask.sum()} out-of-bounds values")
                left_bound[decision_mask] = min_acceptable_value
                df[lstdev_col] = (df[mean_col] - left_bound) / df[stdev_col]

                mean_rel_lstdev_diff = ((df[lstdev_col] - df[lstdev_col]) / df[lstdev_col]).mean()
                logger.info(f"Updated lstdev column for feature {feature}: mean difference {mean_rel_lstdev_diff:.6f}")

        except Exception as e:
            logger.exception(f"Failed out-of-bounds check for feature {feature}: {e}")

    return df


def _calculate_statistics(feature_values: pd.Series, settings: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate statistical metrics for a feature.

    :param feature_values: Series containing feature values.
    :param settings: Settings for feature calculations.
    :return: Dictionary with mean, standard deviation, and coefficients.
    """
    agg_method = settings.get("agg", 'mean')
    if agg_method == 'mean':
        curr_mean = feature_values.mean()
    elif agg_method == 'median':
        curr_mean = feature_values.median()
    elif agg_method == 'percentile':
        curr_mean = np.percentile(feature_values.dropna(), 50)
    else:
        raise NotImplementedError(f"Unsupported aggregation method: {agg_method}")

    curr_std = feature_values.std()
    discard_percent = round(settings.get("discard_percent", 0) / 2, 3)
    percentiles = [discard_percent, 100 - discard_percent]
    percentile_values = np.percentile(feature_values.dropna(), percentiles)
    stds = percentile_values - curr_mean

    return {
        "mean": curr_mean,
        "stdev": curr_std,
        "lstdev_coef": abs(stds[0]),
        "rstdev_coef": stds[1]
    }


def get_stats_on_features(
        age_feature_values: pd.DataFrame,
        age: int,
        logger: logging.Logger,
        features: Dict[str, ExtraFeatures],
        features_settings: Any,
        datapoints_num_thresh: int,
        gby: List[str],
        boundary_shifts: Dict[int, float],
        iqr_boundary_shift: float,
        iqr_percentiles: Optional[List[float]],
        group_names: Union[str, List[str], Tuple[str, ...]],
        use_small_combinations_iqr: bool) -> Optional[Dict[str, Any]]:
    """
    Compute statistics for features based on data for a given age.

    :param age_feature_values: DataFrame with feature values for a specific age.
    :param age: Age for which statistics are computed.
    :param logger: Logger for logging.
    :param features: Dictionary of features and their ExtraFeatures objects.
    :param features_settings: Settings for features.
    :param datapoints_num_thresh: Minimum number of data points required.
    :param gby: Columns to group by.
    :param boundary_shifts: Dictionary of boundary shifts for different ages.
    :param iqr_boundary_shift: IQR boundary shift value.
    :param iqr_percentiles: List of percentiles for IQR calculation.
    :param group_names: Names of the groups for the current age.
    :param use_small_combinations_iqr: Flag to use small combinations IQR.
    :return: Dictionary with computed statistics for each feature or None if not enough data points.
    """
    if len(age_feature_values) < datapoints_num_thresh:
        logger.warning(f"Data length {len(age_feature_values)} is less than threshold {datapoints_num_thresh} "
                       f"for age {age} and groups {gby} = {group_names}. Skipping.")
        return None

    assert set(age_feature_values['daynum']) == {age}, "Filtering error: daynum does not match the specified age."

    info_dict = {'age': age, 'total': len(age_feature_values.dropna(how='all'))}
    if isinstance(group_names, str):
        info_dict[gby[0]] = group_names
    elif isinstance(group_names, (list, tuple)):
        info_dict.update(dict(zip(gby, group_names)))
    else:
        raise NotImplementedError(f"Unknown type for group_names: {group_names}")

    for feature in features:
        if feature not in age_feature_values.columns:
            continue

        settings = extract_feature_settings(features_settings, feature)
        if settings is None or not settings.get("adapt", True):
            logger.info(f"Skipping statistics calculation for feature {feature} due to adapt == False")
            continue

        stats = _calculate_statistics(age_feature_values[feature], settings)

        info_dict.update({
            f"{feature}_mean": stats["mean"],
            f"{feature}_stdev": stats["stdev"],
            f"{feature}_lstdev_coef": stats["lstdev_coef"],
            f"{feature}_rstdev_coef": stats["rstdev_coef"]
        })

        boundary_shift = boundary_shifts.get(age,
                                             iqr_boundary_shift) if use_small_combinations_iqr else iqr_boundary_shift
        lower_range, upper_range = iqr_range(age_feature_values[feature].dropna(), iqr_percentiles, boundary_shift)

        if lower_range <= 0:
            logger.warning(f"Feature {feature} has lower_range <= 0. Adjusting to 1% and 99% percentiles.")
            lower_range, upper_range = np.percentile(age_feature_values[feature].dropna(), [1, 99])

        info_dict[f"{feature}_lower_range"] = abs(lower_range)
        info_dict[f"{feature}_upper_range"] = upper_range

        logger.info(f"Age: {age}; Feature: {feature}; Mean: {stats['mean']:.4f}; Stdev: {stats['stdev']:.4f}; "
                    f"Lstdev: {stats['lstdev_coef']:.4f}; Rstdev: {stats['rstdev_coef']:.4f}; "
                    f"Lower Range: {abs(lower_range):.3f}; Upper Range: {upper_range:.3f}")

    return info_dict


def check_feature_mean_difference(
        features: List,
        feature_settings,
        df: pd.DataFrame,
        logger,
        how: str = StatisticsColumnsConstants.default_mean_check_how,
        mean_diff_thresh: float = 2.,
        gby: List[str] = ['cycle', 'house']
) -> pd.DataFrame:
    """
    Проверяет разницу в средних значениях для функции и фильтрует данные по возрасту.

    :param features: Словарь с настройками функций.
    :param df: Входной DataFrame с необходимыми колонками.
    :param logger: Логгер для записи сообщений.
    :param how: Метод фильтрации данных ('any' или 'each').
    :param mean_diff_thresh: Порог разницы средних значений.
    :param gby: Колонки, по которым выполняется группировка.
    :return: DataFrame с отфильтрованными данными.
    """
    output_df = pd.DataFrame()
    initial_col_order = list(df.columns)

    # Определение всех колонок, связанных с функциями
    feature_cols = [df.filter(regex=f".*{feature}.*").columns for feature in features]
    feature_cols = [col for sublist in feature_cols for col in sublist]

    # Определение колонок, которые всегда будут отсутствовать
    always_missing_columns = [i for i in initial_col_order if i not in feature_cols]

    if 'ExpID' in df.columns:
        df.rename(columns={'ExpID': 'age'}, inplace=True)
    for age, age_group in df.groupby(StatisticsColumnsConstants.age_colname):
        external_break_flag = False
        age_stacked_df = pd.DataFrame()

        for feature in features:

            tmp_settings = extract_feature_settings(features_settings=feature_settings,
                                                    feature=feature)

            if tmp_settings["adapt"] is False:
                logger.info(
                    f"Skipping mean difference calc for feature {feature} due to adapt == {tmp_settings['adapt']}")
                continue

            feature_mean_name = f"{feature}_mean"
            max_value = age_group[feature_mean_name].max()
            min_value = age_group[feature_mean_name].min()
            difference = max_value / min_value

            if difference >= mean_diff_thresh:
                exception_msg = (
                    f"Got mean difference {difference:.4f} for max_value = {max_value:.4f} / {min_value:.4f} = min_value "
                    f"for feature = {feature} and {StatisticsColumnsConstants.age_colname} = {age}; {gby} values: {age_group[gby].values} ")
                if how == 'any':
                    exception_msg += f"Skipping all rows for the {StatisticsColumnsConstants.age_colname} = {age} due to how == {how}"
                    logger.error(exception_msg)
                    external_break_flag = True
                    break
                elif how == 'each':
                    exception_msg += f"Skipping rows only for current feature {feature} for the {StatisticsColumnsConstants.age_colname} = {age} due to how == {how}"
                    logger.error(exception_msg)
                    continue
                else:
                    logger.warning(
                        f"Got unknown behaviour for mean check: how == {how}; using default == {StatisticsColumnsConstants.default_mean_check_how}")
                    exception_msg += f"Skipping rows only for current feature {feature} for the {StatisticsColumnsConstants.age_colname} = {age} due to how == {how}"
                    logger.error(exception_msg)
                    continue

            age_feature_to_concat = age_group.filter(regex=f".*{feature}.*")
            age_stacked_df = pd.concat([age_stacked_df, age_feature_to_concat], axis=1)

        if external_break_flag:
            continue

        cols_difference = list(set(always_missing_columns).difference(set(age_stacked_df.columns)))
        age_stacked_df[cols_difference] = age_group[cols_difference]
        age_stacked_df = age_stacked_df.reset_index(drop=True)
        output_df = pd.concat([output_df, age_stacked_df], axis=0, ignore_index=True)

    old_order = [i for i in initial_col_order if i in output_df.columns]
    output_df = output_df[old_order]
    output_df = output_df.reset_index(drop=True)
    return output_df


def lrstdev_coefs_from_iqr(
        explicit_stats_by_age: pd.DataFrame,
        boundaries: str,
        feature: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    tmp_lstdev_coefs = (explicit_stats_by_age[f"{feature}_mean"] - explicit_stats_by_age[
        f"{feature}_lower_range"]) / explicit_stats_by_age[f"{feature}_stdev"]
    tmp_rstdev_coefs = (explicit_stats_by_age[f"{feature}_upper_range"] - explicit_stats_by_age[
        f"{feature}_mean"]) / explicit_stats_by_age[f"{feature}_stdev"]

    return tmp_lstdev_coefs, tmp_rstdev_coefs
