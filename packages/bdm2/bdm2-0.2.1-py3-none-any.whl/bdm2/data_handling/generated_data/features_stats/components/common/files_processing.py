import logging
import os
from typing import List, Dict, Optional, Any, Tuple

import numpy as np
import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'scipy.stats',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

stats = checker.get_module('scipy.stats')


from bdm2.data_handling.generated_data.features_stats.components.calculation.utils import iqr_range_from_dist
from bdm2.data_handling.generated_data.features_stats.components.common.general import ExtraFeatures
from bdm2.data_handling.generated_data.features_stats.components.common.utils import extract_feature_settings \
    as extract_settings

# Constants
_RUNNING_STATS_AGE_COL = 'Exp_ID'


def process_running_stats_on_features(
        running_stats_filepath: str,
        ages: List[int],
        logger: logging.Logger,
        features: Dict[str, ExtraFeatures],
        boundaries: Any,
        boundary_shifts: Dict[int, float],
        iqr_percentiles: List[float],
        gby: List[str],
        datapoints_num_thresh: int,
        features_settings: Any,
        iqr_boundary_shift: float,
        group_names: Tuple[str, ...],
        replaced_ages: List[int],
        use_small_combinations_iqr: bool,
        sep: Optional[str] = ';') -> Optional[pd.DataFrame]:
    """
    Обрабатывает статистику по фичам на основе ранее сохраненных данных в CSV файле.

    :param running_stats_filepath: Путь к файлу CSV с ранее сохраненными статистиками.
    :param ages: Список возрастов для обработки.
    :param logger: Логгер для записи сообщений.
    :param features: Словарь, где ключи - имена фичей, а значения - объекты ExtraFeatures.
    :param boundaries: Объект с границами для статистики.
    :param boundary_shifts: Словарь с изменениями границ для разных возрастов.
    :param iqr_percentiles: Список процентилей для расчета интерквартильного размаха.
    :param gby: Список имен колонок, по которым будет происходить группировка.
    :param datapoints_num_thresh: Минимальное количество точек данных для обработки.
    :param features_settings: Объект настроек фич, содержащий параметры для расчетов.
    :param iqr_boundary_shift: Значение смещения для интерквартильного размаха.
    :param group_names: Имена групп для текущего возраста.
    :param replaced_ages: Список возрастов, для которых статистики заменяются.
    :param use_small_combinations_iqr: Флаг использования малого количества комбинаций для расчета IQR.
    :param sep: Разделитель для CSV файла.
    :return: DataFrame с реальными явными статистиками по фичам для каждого возраста, или None, если возникла ошибка.
    """
    if not os.path.exists(running_stats_filepath):
        logger.exception(f"File {running_stats_filepath} doesn't exist")
        return None

    running_stats_file = pd.read_csv(running_stats_filepath, sep=sep, engine='python')
    if running_stats_file.empty:
        logger.exception(f"File {running_stats_filepath} is empty. Skipping it")
        return None

    real_explicit_stats = pd.DataFrame()
    available_ages = set(running_stats_file[_RUNNING_STATS_AGE_COL])
    intersection = set(ages).intersection(available_ages)

    if intersection != set(ages):
        logger.warning(f"Some ages do not exist in the file {running_stats_filepath}: "
                       f"{', '.join(map(str, set(ages).difference(available_ages)))}. Using only intersection.")

    for age in intersection:
        slice_df = running_stats_file[running_stats_file[_RUNNING_STATS_AGE_COL] == age]

        if slice_df.empty or len(slice_df) != 1 or slice_df['Total'].item() < datapoints_num_thresh:
            logger.warning(f"Skipping age {age} due to insufficient data or multiple entries")
            continue

        tmp_info_dict = {'age': age, 'total': slice_df['Total'].item()}
        tmp_info_dict.update(dict(zip(gby, group_names)))

        for feature in features:
            tmp_features_settings = extract_settings(features_settings, feature)
            if tmp_features_settings is None or not tmp_features_settings.get("adapt", True):
                logger.info(f"Skipping stats calc for {feature} due to adapt == False")
                continue

            curr_mean = slice_df[f"{feature}_mean"].item()
            curr_std = slice_df[f"{feature}_stdev"].item()

            if pd.isnull(curr_mean) or pd.isnull(curr_std):
                logger.exception(
                    f"NaN value for mean or std {curr_mean, curr_std} for {group_names}, age {age}. Skipping.")
                continue

            distribution = stats.norm(loc=curr_mean, scale=curr_std)
            diff = round(tmp_features_settings["discard_percent"] / 2, 3)
            percentiles = [diff, 100 - diff]
            percentile_values = np.array([distribution.ppf(p / 100) for p in percentiles])
            stds = percentile_values - curr_mean

            tmp_info_dict.update({
                f"{feature}_mean": curr_mean,
                f"{feature}_stdev": curr_std,
                f"{feature}_lstdev_coef": np.abs(stds[0]),
                f"{feature}_rstdev_coef": stds[1]
            })

            if use_small_combinations_iqr:
                boundary_shift = boundary_shifts[age]
                logger.warning(
                    f"For feature={feature} boundary shift was set to {boundary_shift} due to use_small_combinations_iqr")
            else:
                boundary_shift = iqr_boundary_shift

            lower_range, upper_range = iqr_range_from_dist(distribution, iqr_percentiles, boundary_shift)

            if lower_range <= 0:
                logger.warning(
                    f"Feature {feature}: Caught lower_range <= 0: {lower_range}; changing its value to 1% and upper to 99%.")
                lower_range, upper_range = np.percentile(slice_df[feature].dropna(), [1, 99])

            tmp_info_dict[f"{feature}_lower_range"] = abs(lower_range)
            tmp_info_dict[f"{feature}_upper_range"] = upper_range

        real_explicit_stats = real_explicit_stats.append(tmp_info_dict, ignore_index=True)

    return real_explicit_stats
