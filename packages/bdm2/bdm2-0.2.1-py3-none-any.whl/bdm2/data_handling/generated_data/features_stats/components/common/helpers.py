import logging
import os
import pathlib
import re
import warnings
from pathlib import Path
from typing import List, Union, Optional, Dict, Any, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.collecting.explicit import load_explicit
from bdm2.utils.process_data_tools.components.explicits.explicit_manager import get_explicit_files

# declaring constants
_explicit_files_glob_pattern = r'*ForwardRunViz_explicit*.txt'
_runnung_stats_explicit_glob_pattern = r'*Running_stats\Stats_explicit*.txt'
_house_regex = '(House.?[a-zA-Z0-9]+)'
_age_pattern = '_age_\d{1,2}'


def get_age_from_string(string: str) -> Any:
    tmp_r = re.search(pattern='_age_\d{1,2}_', string=string)
    if tmp_r is None:
        return None
    substring = tmp_r.group(0)
    age = re.search(pattern='(\d{1,2})', string=substring)
    if age is None:
        return None

    return int(age.group(0))


def get_group_regex(string: str, pattern: str) -> str:
    """
    pattern here may be _house_regex
    """
    p = re.compile(pattern)
    r = p.search(string=string)
    if r is None:
        return ''
    else:
        return r.group(0)


def get_regex_or(strings: List[str], ) -> str:
    assert isinstance(strings, list)
    or_keyword_general = "(" + ")|(".join(strings) + ")"
    return or_keyword_general


def get_age_files(folder, age: int) -> List[str]:
    pattern = f"age_{age}_"
    ages = [i for i in os.listdir(folder) if pattern in i]
    f_to_read = [os.path.join(folder, i) for i in ages]
    return f_to_read


def concat_df(paths, sep=';', engine='c', show_progress: Optional[bool] = True) -> pd.DataFrame:
    real_df = pd.DataFrame()
    if show_progress:
        pbar = tqdm(paths, total=len(paths))
    else:
        pbar = paths
    # for f in paths:
    for f in pbar:
        if show_progress:
            pbar.set_postfix({f'using engine={engine}, sep={sep} loading file': f" {f}"})
        tmp_df = load_explicit(f)  # pd.read_csv(f, sep=sep, engine=engine)
        real_df = pd.concat([real_df, tmp_df], ignore_index=True)
        del tmp_df

    return real_df.reset_index(drop=True)


def group_files_by_pattern_from_paths(
        paths: List[str], group_pattern: str,
        logger: Optional[logging.Logger] = None) -> Tuple[Dict[str, List[str]], List[str]]:
    grouped_files = {}
    all_files = []
    for path in paths:
        current_group = get_group_regex(str(path), pattern=group_pattern)
        if current_group != '':
            if current_group not in grouped_files.keys():
                grouped_files[current_group] = []
                grouped_files[current_group].append(path)
                all_files.append(path)
            else:
                grouped_files[current_group].append(path)
                all_files.append(path)
        else:
            warn_msg = f"Cannot determine house for {path}; " + \
                       f"regex pattern based on selected devices is: {group_pattern}"
            if logger is not None:
                logger.warning(warn_msg)
            else:
                warnings.warn(warn_msg)

    return grouped_files, all_files


def group_files_by_pattern(paths: List[str], group_pattern: str,
                           files_pattern: str,
                           logger: Optional[logging.Logger] = None) -> Tuple[Dict[str, Any], List[str]]:
    grouped_files = {}
    all_files = []
    for path in paths:
        current_group = get_group_regex(str(path), pattern=group_pattern)
        if current_group != '':
            if current_group not in grouped_files.keys():
                grouped_files[current_group] = []
                found_files = [str(i) for i in list(Path(path).rglob(files_pattern))]
                grouped_files[current_group].extend(found_files)
                all_files.extend(found_files)
            else:
                found_files = [str(i) for i in list(Path(path).rglob(files_pattern))]
                grouped_files[current_group].extend(found_files)
                all_files.extend(found_files)
        else:
            warn_msg = f"Cannot determine house for {path}; " + \
                       f"regex pattern based on selected devices is: {group_pattern}"
            if logger is not None:
                logger.warning(warn_msg)
            else:
                warnings.warn(warn_msg)

    return grouped_files, all_files


def listdir(folderpath: str, pattern: str):  # -> List[pathlib.WindowsPath]:
    return list(Path(folderpath).rglob(pattern))


def group_by_age(files: List[Union[str, pathlib.WindowsPath]], age: int) -> Any:
    assert age >= 0 and isinstance(age, int) or isinstance(age,
                                                           np.int32), f"age must be >= 0 and of type 'int', got: {age}, {type(age)}"
    pattern = f"_age_{age}_"
    return [i for i in files if pattern in os.path.basename(str(i))]


# def sep_group_by_ages(grouped_files, ages: Union[np.ndarray, List[int]] = np.arange(0, 61, 1)):
#     groups_to_ages = {}
#     for group in grouped_files.keys():
#         current_files = grouped_files[group]
#         groups_to_ages[group] = {}
#         for age in ages:
#             tmp_r = group_by_age(files=current_files, age=age)
#             if len(tmp_r):
#                 groups_to_ages[group][age] = tmp_r
#                 if len(groups_to_ages[group][age]) == 0:
#                     # then del the key:
#                     del groups_to_ages[group][age]
#
#     # also make age-to-files mapping:
#     age_to_files = {}
#     for age in ages:
#         age_to_files[age] = []
#         tmp_r = group_by_age(files=all_files, age=age)
#         if len(tmp_r):
#             age_to_files[age].extend(tmp_r)
#         if len(age_to_files[age]) == 0:
#             # then del the key:
#             del age_to_files[age]
#
#     return groups_to_ages, age_to_files


def get_houses_to_ages(client, devices: pd.DataFrame,
                       engine_config: EngineConfig, filters: Filter,
                       logger: logging.Logger, ages: Union[np.ndarray, List[int]] = np.arange(0, 61, 1),
                       *args, **kwargs) -> Tuple[dict, dict]:
    # activeExplicitFolder = engine_config.ForwardRunViz_folder
    filters.clients = [client]
    devices_loc = filters.filter_devices(devices)
    u_h = list(devices_loc['house'].unique())
    or_pattern = get_regex_or(u_h)
    # selected_devices = [device for _, device in devices_loc.iterrows() if my_filters.check_device(device)]
    dirs_to_files = []
    for _, device in devices_loc.iterrows():
        try:
            if not filters.check_device(device):
                continue
            explicit_dir, explicit_files = get_explicit_files(device, engine_config, filters, useRolled=False)
            if len(explicit_files):
                dirs_to_files.append((explicit_dir, explicit_files))
        except Exception as E:
            logger.exception(E)
    selected_dirs = [i[0] for i in dirs_to_files]
    grouped_files, all_files = group_files_by_pattern(paths=selected_dirs,
                                                      group_pattern=or_pattern,
                                                      files_pattern=_explicit_files_glob_pattern,
                                                      logger=logger)
    assert len(grouped_files) > 0, f"There's no files found"
    # running_stats_dirs = [Path(i) / _running_stats_foldername for i in selected_dirs]
    groups_to_ages = {}
    for group in grouped_files.keys():
        current_files = grouped_files[group]
        groups_to_ages[group] = {}
        for age in ages:
            tmp_r = group_by_age(files=current_files, age=age)
            if len(tmp_r):
                groups_to_ages[group][age] = tmp_r

                if len(groups_to_ages[group][age]) == 0:
                    # then del the key:
                    del groups_to_ages[group][age]

    # also make age-to-files mapping:
    age_to_files = {}
    for age in ages:
        age_to_files[age] = []
        tmp_r = group_by_age(files=all_files, age=age)
        if len(tmp_r):
            age_to_files[age].extend(tmp_r)
        if len(age_to_files[age]) == 0:
            # then del the key:
            del age_to_files[age]

    return groups_to_ages, age_to_files

# activeExplicitFolder = my_engine_config.ForwardRunViz_folder
# my_filters.clients = [client]
# devices_loc = my_filters.filter_devices(devices)
# # devices[devices.client.isin([client])]
# u_h = list(devices_loc['house'].unique())
# or_pattern = get_regex_or(u_h)
#
# # import functools
# # retrieve_house = functools.partial(get_house, pattern=or_pattern)
#
# # selected_devices = [device for _, device in devices_loc.iterrows() if my_filters.check_device(device)]
# dirs_to_files = []
# for _, device in devices_loc.iterrows():
#     try:
#         if not filters.check_device(device):
#             continue
#         # explicit_dir = my_engine_config.local_results_dir + "\\" + device.path + "\\" + activeExplicitFolder
#         explicit_dir, explicit_files = get_explicit_files(device, my_engine_config, filters, useRolled=False)
#         if len(explicit_files):
#             dirs_to_files.append((explicit_dir, explicit_files))
#     except Exception as E:
#         logger.exception(E)
#
# # Note: when use_percentage['how'] == 'raw' - you use explicit_files rather than dir
# #   now you have to use only dirs because in such dirs should be 'Running_stats' folders so
# selected_dirs = [i[0] for i in dirs_to_files]
# running_stats_dirs = [Path(i) / _running_stats_foldername for i in selected_dirs]
# existing_running_stats = [i / _stats_explicits_filename for i in running_stats_dirs if (i / _stats_explicits_filename).exists()]
# # now you can group them by houses
# grouped_stats_files = {}
# for run_stats_path in existing_running_stats:
#     c_house = get_house(str(run_stats_path), pattern=or_pattern)
#     if c_house != '':
#         if c_house in grouped_stats_files.keys():
#             grouped_stats_files[c_house] = []
#             grouped_stats_files[c_house] .append(str(run_stats_path))
#         else:
#             grouped_stats_files[c_house].append(str(run_stats_path))
#     else:
#         logger.warning(f"Cannot determine house for {run_stats_path}; " + \
#                        f"regex pattern based on selected devices is: {or_pattern}")
