import copy
import logging
import os
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from tqdm import tqdm

from bdm2.data_handling.generated_data.features_stats.components.calculation.utils import get_stats_on_features, \
    lrstdev_coefs_from_iqr
from bdm2.data_handling.generated_data.features_stats.components.common.files_processing import \
    process_running_stats_on_features
from bdm2.data_handling.generated_data.features_stats.components.common.general import prepare_paths_info
from bdm2.data_handling.generated_data.features_stats.components.common.helpers import concat_df, get_age_from_string, \
    get_regex_or
from bdm2.data_handling.generated_data.features_stats.components.common.utils import extract_feature_settings
from bdm2.data_handling.generated_data.features_stats.components.const.names import StatisticsColumnsConstants
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.explicits.explicit_manager import get_explicit_files, \
    get_explicit_files_froms3


def proceed_cloud_explicits(
        feature_settings,
        group_by_cols: List[str],
        boundary_shifts,
        small_combinations_threshold: int,
        datapoints_num_thresh: int,
        iqr_boundary_shift: float,
        iqr_percentiles,
        # selected_dirs: List[str],
        features,
        or_pattern_cycle: str,
        or_pattern_house: str,
        _explicit_files_glob_pattern: str,
        ages,
        filters: Filter,
        logger: logging.Logger,
        devices_slice: pd.DataFrame,
        # main_config,
        *args, **kwargs
) -> Tuple[pd.DataFrame, List[int]]:
    all_explicits_info = pd.DataFrame()
    replaced_ages: List[int] = []

    all_files = []
    ages_map_full = {}
    explicits_map_full = {}

    for _, device in devices_slice.iterrows():
        try:
            tmp_explicits_s3path, brddevice_b, ages_map, explicits_map \
                = get_explicit_files_froms3(device, filters=None)

            all_files.extend(tmp_explicits_s3path)
            for k, v in ages_map.items():
                ages_map_full.setdefault(k, v)
            for k, v in explicits_map.items():
                explicits_map_full.setdefault(k, v)
            break
        except Exception as e:
            logger.warning(f"Failed to process device: {e}")
            continue

    if not all_files:
        raise ValueError("No explicit files found")

    all_explicits_info['path'] = all_files
    house_s3_pattern = get_regex_or(list(set([i.split('/')[3] for i in all_explicits_info['path'].values.tolist()])))
    all_explicits_info = prepare_paths_info(all_explicits_info, {'cycle': or_pattern_cycle, 'house': house_s3_pattern})

    renaming_dict = devices_slice[["house_id", "house"]].drop_duplicates()
    house_mapping = renaming_dict.set_index('house_id')['house'].to_dict()
    all_explicits_info['house'] = all_explicits_info['house'].map(house_mapping)
    all_explicits_info['age'] = all_explicits_info['path'].map(ages_map_full)

    all_explicits_info.dropna(inplace=True)

    # all_explicits_info[StatisticsColumnsConstants.age_colname] = all_explicits_info['path'].apply(
    #     lambda x: get_age_from_string(x))

    filtered_explicits_info = all_explicits_info.copy()
    for group_name in group_by_cols:
        cur_filter_values = getattr(filters, f"{group_name}s")
        if cur_filter_values:
            logger.info(f"Filtering by {group_name}s: {cur_filter_values}")
            filtered_explicits_info = filtered_explicits_info[
                filtered_explicits_info[group_name].isin(cur_filter_values)]

    real_explicit_stats = pd.DataFrame()

    for age in ages:
        age_subset = filtered_explicits_info[filtered_explicits_info[StatisticsColumnsConstants.age_colname] == age]
        if age_subset.empty:
            logger.warning(f"No data for age {age}. Skipping.")
            continue

        if set(group_by_cols).intersection(age_subset.columns):
            grouped_iterator = age_subset.groupby(group_by_cols)

            use_small_combinations_iqr = len(grouped_iterator) < small_combinations_threshold
            if use_small_combinations_iqr:
                logger.warning(
                    f"Number of groups ({len(grouped_iterator)}) is less than threshold ({small_combinations_threshold}). Using small combination IQR.")

            for group_names, group in tqdm(grouped_iterator, total=len(grouped_iterator), desc=f"Processing age {age}"):
                # TODO: тащить из словаря нужный эксплисит
                explicit_key = group['path'].values[0]
                explicit_df = explicits_map_full[explicit_key]
                # age_feature_values = concat_df(group['path'], show_progress=False)
                tmp_info_dict = get_stats_on_features(
                    age_feature_values=explicit_df,
                    age=age,
                    logger=logger,
                    features=features,
                    features_settings=feature_settings,
                    datapoints_num_thresh=datapoints_num_thresh,
                    gby=group_by_cols,
                    boundary_shifts=boundary_shifts,
                    iqr_boundary_shift=iqr_boundary_shift,
                    iqr_percentiles=iqr_percentiles,
                    group_names=group_names,
                    use_small_combinations_iqr=use_small_combinations_iqr
                )
                if tmp_info_dict:
                    real_explicit_stats = pd.concat([real_explicit_stats, pd.DataFrame([tmp_info_dict])],
                                                    ignore_index=True)
        else:
            use_small_combinations_iqr = len(age_subset) < small_combinations_threshold
            if use_small_combinations_iqr:
                logger.warning(
                    f"Number of rows ({len(age_subset)}) is less than threshold ({small_combinations_threshold}). Using small combination IQR.")

            logger.info("No group by columns. Calculating statistics globally.")

            age_feature_values = concat_df(age_subset['path'], show_progress=True)

            age_feature_values_global = pd.DataFrame()
            for i in age_subset['path']:
                explicit_df = explicits_map_full[i]
                age_feature_values_global = pd.concat([age_feature_values_global, explicit_df])

            tmp_info_dict = get_stats_on_features(
                age_feature_values=age_feature_values_global,
                age=age,
                logger=logger,
                features=features,
                features_settings=feature_settings,
                datapoints_num_thresh=datapoints_num_thresh,
                gby=group_by_cols,
                boundary_shifts=boundary_shifts,
                iqr_boundary_shift=iqr_boundary_shift,
                iqr_percentiles=iqr_percentiles,
                group_names=[],
                use_small_combinations_iqr=use_small_combinations_iqr
            )
            if tmp_info_dict:
                real_explicit_stats = pd.concat([real_explicit_stats, pd.DataFrame([tmp_info_dict])], ignore_index=True)

        replaced_ages.append(age)

    return real_explicit_stats, replaced_ages


def proceed_raw_explicits(
        feature_settings,
        group_by_cols: List[str],
        boundary_shifts,
        small_combinations_threshold: int,
        datapoints_num_thresh: int,
        iqr_boundary_shift: float,
        iqr_percentiles,
        selected_dirs: List[str],
        features,
        or_pattern_cycle: str,
        or_pattern_house: str,
        _explicit_files_glob_pattern: str,
        ages,
        filters: Filter,
        logger: logging.Logger,
        devices_slice: pd.DataFrame,
        main_config,
        *args, **kwargs
) -> Tuple[pd.DataFrame, List[int]]:
    all_explicits_info = pd.DataFrame()
    replaced_ages: List[int] = []

    all_files = []
    for _, device in devices_slice.iterrows():
        try:
            tmp_dir, tmp_explicits = get_explicit_files(device, main_config, filters=None, useRolled=False)
            tmp_files = [os.path.join(tmp_dir, s) for s in tmp_explicits]
            all_files.extend(tmp_files)
        except Exception as e:
            logger.warning(f"Failed to process device: {e}")
            continue

    if not all_files:
        raise ValueError("No explicit files found")

    all_explicits_info['path'] = all_files
    all_explicits_info = prepare_paths_info(all_explicits_info, {'cycle': or_pattern_cycle, 'house': or_pattern_house})

    all_explicits_info.dropna(inplace=True)

    all_explicits_info[StatisticsColumnsConstants.age_colname] = all_explicits_info['path'].apply(
        lambda x: get_age_from_string(x))

    filtered_explicits_info = all_explicits_info.copy()
    for group_name in group_by_cols:
        cur_filter_values = getattr(filters, f"{group_name}s")
        if cur_filter_values:
            logger.info(f"Filtering by {group_name}s: {cur_filter_values}")
            filtered_explicits_info = filtered_explicits_info[
                filtered_explicits_info[group_name].isin(cur_filter_values)]

    real_explicit_stats = pd.DataFrame()

    for age in ages:
        age_subset = filtered_explicits_info[filtered_explicits_info[StatisticsColumnsConstants.age_colname] == age]
        if age_subset.empty:
            logger.warning(f"No data for age {age}. Skipping.")
            continue

        if set(group_by_cols).intersection(age_subset.columns):
            grouped_iterator = age_subset.groupby(group_by_cols)

            use_small_combinations_iqr = len(grouped_iterator) < small_combinations_threshold
            if use_small_combinations_iqr:
                logger.warning(
                    f"Number of groups ({len(grouped_iterator)}) is less than threshold ({small_combinations_threshold}). Using small combination IQR.")

            for group_names, group in tqdm(grouped_iterator, total=len(grouped_iterator), desc=f"Processing age {age}"):
                age_feature_values = concat_df(group['path'], show_progress=False)
                tmp_info_dict = get_stats_on_features(
                    age_feature_values=age_feature_values,
                    age=age,
                    logger=logger,
                    features=features,
                    features_settings=feature_settings,
                    datapoints_num_thresh=datapoints_num_thresh,
                    gby=group_by_cols,
                    boundary_shifts=boundary_shifts,
                    iqr_boundary_shift=iqr_boundary_shift,
                    iqr_percentiles=iqr_percentiles,
                    group_names=group_names,
                    use_small_combinations_iqr=use_small_combinations_iqr
                )
                if tmp_info_dict:
                    real_explicit_stats = pd.concat([real_explicit_stats, pd.DataFrame([tmp_info_dict])],
                                                    ignore_index=True)
        else:
            use_small_combinations_iqr = len(age_subset) < small_combinations_threshold
            if use_small_combinations_iqr:
                logger.warning(
                    f"Number of rows ({len(age_subset)}) is less than threshold ({small_combinations_threshold}). Using small combination IQR.")

            logger.info("No group by columns. Calculating statistics globally.")
            age_feature_values = concat_df(age_subset['path'], show_progress=True)
            tmp_info_dict = get_stats_on_features(
                age_feature_values=age_feature_values,
                age=age,
                logger=logger,
                features=features,
                features_settings=feature_settings,
                datapoints_num_thresh=datapoints_num_thresh,
                gby=group_by_cols,
                boundary_shifts=boundary_shifts,
                iqr_boundary_shift=iqr_boundary_shift,
                iqr_percentiles=iqr_percentiles,
                group_names=[],
                use_small_combinations_iqr=use_small_combinations_iqr
            )
            if tmp_info_dict:
                real_explicit_stats = pd.concat([real_explicit_stats, pd.DataFrame([tmp_info_dict])], ignore_index=True)

        replaced_ages.append(age)

    return real_explicit_stats, replaced_ages


def process_agg_explicits(
        gby: List[str],
        small_combinations_threshold: int,
        boundary_shifts,
        datapoints_num_thresh: int,
        features_settings,
        iqr_boundary_shift: float,
        iqr_percentiles,
        boundaries: str,
        features,
        selected_dirs: List[str],
        or_pattern_cycle: str,
        or_pattern_house: str,
        ages: Union[np.ndarray, List[int]],
        _runnung_stats_explicit_glob_pattern: str,
        logger: logging.Logger,
        *args,
        **kwargs
) -> Tuple[pd.DataFrame, List[int]]:
    house_dirs = [Path(d).parent for d in selected_dirs]
    running_stats_files = []

    for folder in house_dirs:
        tmp_files = list(folder.rglob(_runnung_stats_explicit_glob_pattern))
        if len(tmp_files) == 1:
            running_stats_files.append(str(tmp_files[0]))
        else:
            logger.exception(
                f"Unexpected number of running stats files in {folder}. Expected 1, found {len(tmp_files)}.")

    all_explicits_info = pd.DataFrame({'path': running_stats_files})
    all_explicits_info = prepare_paths_info(all_explicits_info, {'cycle': or_pattern_cycle, 'house': or_pattern_house})

    all_explicits_info.dropna(inplace=True)

    logger.info(
        "Using aggregated stats. This may cause significant differences between real and calculated ranges due to reliance on normal distribution.")

    agg_explicit_stats = pd.DataFrame()
    replaced_ages: List[int] = []

    for group_names, group in all_explicits_info.groupby(gby):
        use_small_combinations_iqr = len(group) < small_combinations_threshold
        if use_small_combinations_iqr:
            logger.warning(
                f"Number of files ({len(group)}) is less than threshold ({small_combinations_threshold}). Using small combination IQR.")

        for path in group['path']:
            tmp_df = pd.read_csv(path, sep=';', engine='c')
            if tmp_df.empty:
                logger.warning(f"Empty running stats DataFrame at {path}.")
                continue

            tmp_explicit_stats = process_running_stats_on_features(
                running_stats_filepath=path,
                ages=ages,
                logger=logger,
                features=features,
                boundaries=boundaries,
                boundary_shifts=boundary_shifts,
                gby=gby,
                datapoints_num_thresh=datapoints_num_thresh,
                features_settings=features_settings,
                iqr_boundary_shift=iqr_boundary_shift,
                iqr_percentiles=iqr_percentiles,
                group_names=group_names,
                sep=';',
                replaced_ages=replaced_ages,
                use_small_combinations_iqr=use_small_combinations_iqr
            )
            if tmp_explicit_stats is not None:
                agg_explicit_stats = pd.concat([agg_explicit_stats, tmp_explicit_stats], ignore_index=True)

    if agg_explicit_stats.empty:
        raise ValueError(f"No data collected from running stats. Check paths: {running_stats_files}")

    return agg_explicit_stats, list(set(replaced_ages))


# Example usage:
if __name__ == "__main__":
    # Configuration and setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Example data (replace with actual data)
    feature_settings = {}  # Example placeholder
    group_by_cols = []  # Example placeholder
    boundary_shifts = {}  # Example placeholder
    small_combinations_threshold = 5  # Example placeholder
    datapoints_num_thresh = 100  # Example placeholder
    iqr_boundary_shift = 1.5  # Example placeholder
    iqr_percentiles = (25, 75)  # Example placeholder
    selected_dirs = []  # Example placeholder
    features = {}  # Example placeholder
    or_pattern_cycle = ""  # Example placeholder
    or_pattern_house = ""  # Example placeholder
    _explicit_files_glob_pattern = "*.csv"  # Example placeholder
    ages = [20, 30, 40]  # Example placeholder
    filters = Filter()  # Example placeholder
    devices_slice = pd.DataFrame()  # Example placeholder
    main_config = {}  # Example placeholder

    try:
        result, replaced_ages = proceed_raw_explicits(
            feature_settings=feature_settings,
            group_by_cols=group_by_cols,
            boundary_shifts=boundary_shifts,
            small_combinations_threshold=small_combinations_threshold,
            datapoints_num_thresh=datapoints_num_thresh,
            iqr_boundary_shift=iqr_boundary_shift,
            iqr_percentiles=iqr_percentiles,
            selected_dirs=selected_dirs,
            features=features,
            or_pattern_cycle=or_pattern_cycle,
            or_pattern_house=or_pattern_house,
            _explicit_files_glob_pattern=_explicit_files_glob_pattern,
            ages=ages,
            filters=filters,
            logger=logger,
            devices_slice=devices_slice,
            main_config=main_config
        )
        logger.info(f"Processed raw explicits. Result shape: {result.shape}, Replaced ages: {replaced_ages}")

        # Example usage of process_agg_explicits
        agg_result, replaced_ages = process_agg_explicits(
            gby=[],
            small_combinations_threshold=5,
            boundary_shifts={},
            datapoints_num_thresh=100,
            features_settings={},
            iqr_boundary_shift=1.5,
            iqr_percentiles=(25, 75),
            boundaries='20 30 40',
            features={},
            selected_dirs=[],
            or_pattern_cycle='',
            or_pattern_house='',
            ages=[20, 30, 40],
            _runnung_stats_explicit_glob_pattern='*.csv',
            logger=logger
        )
        logger.info(f"Processed aggregated explicits. Result shape: {agg_result.shape}, Replaced ages: {replaced_ages}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


def update_explicit_boundaries(
        real_explicit_stats: pd.DataFrame,
        cols_to_ignore: List[str],
        boundaries: str,  # Изменили имя параметра на boundaries
        features: List[str],
        feature_settings,
        logger: logging.Logger,
        weights_col: str = 'total'
) -> pd.DataFrame:
    """
    Обновляет границы для статистики на основе данных и определенного типа границ.

    :param real_explicit_stats: DataFrame с исходными статистиками.
    :param cols_to_ignore: Колонки, которые нужно игнорировать при расчетах.
    :param boundaries: Тип границ ('extreme' или 'weighted').
    :param features: Словарь с настройками функций.
    :param logger: Логгер для записи сообщений.
    :param weights_col: Колонка с весами для расчетов.
    :return: DataFrame с обновленными границами.
    @param weights_col:
    @param features:
    @param boundaries:
    @param cols_to_ignore:
    @param logger:
    @param feature_settings:
    """
    cols_for_series = [i for i in real_explicit_stats.columns if i not in cols_to_ignore]

    # Вычисление средних значений по возрастам
    explicit_stats_by_age = real_explicit_stats.groupby(StatisticsColumnsConstants.age_colname).apply(
        lambda x: pd.Series([np.average(x[v], weights=x[weights_col]) for v in cols_for_series])
    )
    explicit_stats_by_age.columns = cols_for_series

    # Обновление границ
    lr_cols = real_explicit_stats.filter(regex='.*lower_range').columns
    ur_cols = real_explicit_stats.filter(regex='.*upper_range').columns
    min_range_df = real_explicit_stats.groupby(StatisticsColumnsConstants.age_colname).min()[lr_cols]
    max_range_df = real_explicit_stats.groupby(StatisticsColumnsConstants.age_colname).max()[ur_cols]
    explicit_stats_by_age[lr_cols] = min_range_df[lr_cols]
    explicit_stats_by_age[ur_cols] = max_range_df[ur_cols]

    # Обновление коэффициентов
    replaced_explicit_stats = copy.deepcopy(explicit_stats_by_age)
    for feature in features:

        tmp_settings = extract_feature_settings(features_settings=feature_settings,
                                                feature=feature)

        if tmp_settings["adapt"] is False:
            logger.info(f"Skipping stats calculation for feature {feature} due to adapt == {tmp_settings['adapt']}")
            continue

        if boundaries == 'extreme':
            tmp_lstdev_coefs, tmp_rstdev_coefs = lrstdev_coefs_from_iqr(
                explicit_stats_by_age=explicit_stats_by_age,
                feature=feature, boundaries=boundaries
            )
        elif boundaries == 'weighted':
            tmp_lstdev_coefs = explicit_stats_by_age[f"{feature}_lstdev_coef"]
            tmp_rstdev_coefs = explicit_stats_by_age[f"{feature}_rstdev_coef"]
        else:
            logger.exception(
                f"Unrecognized boundaries type for lstdev/rstdev calculation: {boundaries}; Using iqr values to calculate them")
            tmp_lstdev_coefs, tmp_rstdev_coefs = lrstdev_coefs_from_iqr(
                explicit_stats_by_age=explicit_stats_by_age,
                feature=feature, boundaries=boundaries
            )

        replaced_explicit_stats[f"{feature}_lstdev_coef"] = tmp_lstdev_coefs
        replaced_explicit_stats[f"{feature}_rstdev_coef"] = tmp_rstdev_coefs

    return replaced_explicit_stats
