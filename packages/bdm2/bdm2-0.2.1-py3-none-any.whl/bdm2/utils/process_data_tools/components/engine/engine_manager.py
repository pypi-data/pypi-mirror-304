"""
Tools for managing engine

"""
import copy
import datetime
import filecmp
import logging
import os
import shutil
import subprocess
import time
import warnings
from typing import Dict, Any, Union, Optional

import pandas as pd
import yaml

from bdm2.constants.global_setup.bats import get_stat_header_bat, stat_header_filename, mklink_bat
from bdm2.constants.global_setup.data import not_critical_params
from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.constants.global_setup.env import SESS_ID, workdir
from bdm2.constants.global_setup.server_paths import server_workdir, extra_libs_link_name
from bdm2.utils.process_data_tools.utils import load_statistics_from_csv

logger = logging.getLogger(__name__)


class MainParamsKeyError(Exception):
    """
    Trying to get not existing param

    """

    pass


def get_engine_v(engine: str) -> str:
    """
    Extract engine version numbers part.
    Example:
        _v4.10.7.6_CGTHCM_ROSS_male_1805_final -> 4.10.7.6
    :param engine:
    :return:
    """
    v = engine.split('_')[1][1:]
    return v


def get_engine_v_ass_int(engine: str) -> int:
    """
    return engine version as int. Usefully for version comparison

    :param engine: Standard engine version. Format _v1.20.30.40.50
    :return: 120304050
    """

    v = list(map(int, (engine.split('_')[1])[1:].split('.')))
    k = 1000000000
    res = 0
    for el in v:
        res += el * k
        k /= 100
        if k < 1:
            break
    return int(res)


def update_bats(engine_dir: str) -> bool:
    """
    Update bat files of engine dir with local stored bat files. Actual bat files are stored in .\bats

    :param engine_dir: path to engine folder, where bat files should be replaced
    :return: true if updated successfully
    """
    try:
        for bat_file in os.listdir(os.path.dirname(__file__) + "\\" + "bats"):
            if bat_file.endswith('.bat'):
                shutil.copy2(os.path.dirname(__file__) + "\\" + "bats" + "\\" + bat_file, engine_dir)
        return True
    except:
        return False


def get_params(main_params_fname: str, param_name: str) -> Union[str, None]:
    """
    Get yaml param value from main_params.yaml. Return None if parameter not found

    :param main_params_fname: full path to main_params.yaml
    :param param_name: main_param key
    :return: main_param value
    """
    if not os.path.exists(main_params_fname):
        print("{} does not exists".format(main_params_fname))
        return None

    with open(main_params_fname, 'r') as stream:
        for line in stream.read().splitlines():
            cur_param_name = (line.split(": ")[0])
            if param_name == cur_param_name:
                value = line.split(": ")[-1].replace("\"", "")
                if value == '':
                    return None
                else:
                    return value
    return None


def set_new_params(main_params_fname, params_dict: Dict[str, Any]) -> bool:
    """
    Set new param or change value of existing param engine config (main_params.yml)

    :param main_params_fname: full path to .yml config file
    :param params_dict: params to be added/updated
    :return: True if success
    """
    if not os.path.exists(main_params_fname):
        print("{} does not exists".format(main_params_fname))
        return False

    lines = []

    params_dict_changes = copy.copy(params_dict)
    for p in params_dict_changes:
        params_dict_changes[p] = False

    with open(main_params_fname, 'r') as stream:
        for line in stream.read().splitlines():
            param_name = (line.split(": ")[0])
            if param_name in params_dict.keys():
                value = str(params_dict[param_name])
                new_line = ": ".join([param_name, value])
                new_line = new_line.replace("\\", "/")
                lines.append(new_line)
                print("Param {} was set to {}".format(param_name, value))
                params_dict_changes[param_name] = True
            else:
                lines.append(line)

    if not all(params_dict_changes.values()):
        param_names_bad = []
        for p in params_dict_changes:
            if params_dict_changes[p] == False:
                param_names_bad.append(p)
        warnings.warn(
            "No param :{}: in engine_config\nengine_config.yml will not be updated".format(", ".join(param_names_bad)))
        return False

    while True:
        try:
            with open(main_params_fname, 'w', encoding="ascii", newline='') as stream:
                for line in lines:
                    stream.write(line + "\n")
            break
        except:
            time.sleep(1)

    return True


def add_c_vector_to_df(engine_config: EngineConfig, age: int, df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cvector from engine to df

    :param engine_config: engine config with cvector file, that is declared in density_model_table
    :param age: for which age get cvector file
    :param df: src df
    :return: updated df
    """
    density_model_table_fname = get_params(engine_config.main_params_dir,
                                           "ObjectQualityEstimatorParams_density_model_table")
    if pd.isnull(density_model_table_fname):
        return df
    density_model_table_df = pd.read_csv(engine_config.engine_dir + "\\" + density_model_table_fname, sep=';',
                                         index_col=0)
    if density_model_table_df.empty:
        density_model_table_df = pd.read_csv(engine_config.engine_dir + "\\" + density_model_table_fname, sep=' ',
                                             index_col=0)
    if 'global_features_file' not in density_model_table_df.columns:
        print(f'{density_model_table_fname} in {engine_config.engine_dir} does not have an information about c-vector')
        return df
    try:
        global_features_file = engine_config.engine_dir + "\\" + density_model_table_df.loc[age, 'global_features_file']
    except KeyError as e:
        print(f"Can not obtain global_features_file for age {age}")
        return df
    except Exception as e:
        print(e)
        return df
    if not os.path.exists(global_features_file):
        print(f"No {global_features_file} in {engine_config.engine_dir}")
        return df

    try:
        global_features_df = pd.read_csv(global_features_file, sep=';', header=None, index_col=0)[1]
    except Exception as e:
        print(e)
        return df
    df_output = df.copy()
    for c in global_features_df.index:
        df_output[c] = global_features_df[c]
    return df_output


def get_engine_density(engine_config: EngineConfig, do_from_snapshot=False):
    """
    Return density fname and density df, if density set as file

    :param engine_config: src engine config
    :param do_from_snapshot: if True, get data from snapshot path , that is in results folder
    :return: density fname and density df
    """
    if do_from_snapshot:
        d_param = get_params(engine_config.engine_snapshot_dir
                             + "\\"
                             + os.path.basename(engine_config.main_params_dir),
                             "ObjectQualityEstimatorParams_densities_statistics_file")
        if d_param is None:
            return None, None
        engine_density_filename = engine_config.engine_snapshot_dir + "\\" + d_param
    else:
        d_param = get_params(engine_config.main_params_dir,
                             "ObjectQualityEstimatorParams_densities_statistics_file")
        if d_param is None:
            return None, None

        engine_density_filename = engine_config.engine_dir + "\\" + d_param

    if os.path.exists(engine_density_filename):
        res = pd.read_csv(engine_density_filename, sep=";", index_col=0)
        if res.empty:
            res = pd.read_csv(engine_density_filename, sep=" ", index_col=0)
        return engine_density_filename, res
    else:
        return None, None


def get_coding_params(engine_config: EngineConfig, do_from_snapshot=False) -> Optional[Dict[str, Any]]:
    """
    Return density fname and density df, if density set as file

    :param engine_config: src engine config
    :param do_from_snapshot: if True, get data from snapshot path , that is in results folder
    :return: density fname and density df
    """
    if do_from_snapshot:
        fname = os.path.join(engine_config.engine_snapshot_dir, 'OtherData', 'prediction_nets', 'coding_params.yaml')
    else:
        fname = os.path.join(engine_config.engine_dir, 'OtherData', 'prediction_nets', 'coding_params.yaml')

    if not os.path.exists(fname):
        return None

    coding_params = yaml.load(open(fname, 'r'), yaml.SafeLoader)
    return coding_params


def get_extra_features_fnames(engine_config: EngineConfig, age: int) -> Union[str, None]:
    """
    Get global_features_file for specified age

    :param engine_config: src engine config
    :param age: age
    :return: global_features fname or None if no information in density_model_table
    """
    d_param = get_params(engine_config.engine_snapshot_dir
                         + "\\"
                         + os.path.basename(engine_config.main_params_dir),
                         "ObjectQualityEstimatorParams_density_model_table")
    if d_param is None:
        return None
    density_model_table_fname = engine_config.engine_snapshot_dir + "\\" + d_param
    density_model_table_df = pd.read_csv(density_model_table_fname, sep=';', index_col=0)
    if len(density_model_table_df.columns) == 0:
        density_model_table_df = pd.read_csv(density_model_table_fname, sep=' ', index_col=0)
    try:
        return density_model_table_df.loc[age]['global_features_file']
    except:
        print(f'Could not obtain global_features_files for age {age}')
        return None


def get_density_model_and_featuremask_fnames(engine_config: EngineConfig, age: int) -> [Optional[str], Optional[str]]:
    """
    Get path to density model and feature mask for specified age

    :param engine_config: src engine config
    :param age: age
    :return: path to density model and feature mask for specified age
    """
    d_param = get_params(engine_config.engine_dir_on_server
                         + "\\"
                         + os.path.basename(engine_config.main_params_dir),
                         "ObjectQualityEstimatorParams_density_model_table")
    if d_param is None:
        return None, None
    density_model_table_fname = os.path.join(engine_config.engine_dir_on_server, d_param)
    density_model_table_df = pd.read_csv(density_model_table_fname, sep=';', index_col=0)
    if len(density_model_table_df.columns) == 0:
        density_model_table_df = pd.read_csv(density_model_table_fname, sep=' ', index_col=0)
    try:
        return density_model_table_df.loc[age]['Model_filename'], \
            density_model_table_df.loc[age]['Selected_features_filename']
    except Exception as e:
        print(f'Could not obtain density model for age {age}: {e}')
        return None, None


def get_distance_model_and_featuremask_fnames(engine_config: EngineConfig, age: int) -> [Optional[str], Optional[str]]:
    """
    Get path to distance model and feature mask for specified age

    :param engine_config: src engine config
    :param age: age
    :return: path to distance model and feature mask for specified age
    """
    d_param = get_params(engine_config.engine_dir_on_server
                         + "\\"
                         + os.path.basename(engine_config.main_params_dir),
                         "ObjectQualityEstimatorParams_distance_model_table")
    if d_param is None:
        return None, None
    distance_model_table_fname = os.path.join(engine_config.engine_dir_on_server, d_param)
    distance_model_table_df = pd.read_csv(distance_model_table_fname, sep=';', index_col=0)
    if len(distance_model_table_df.columns) == 0:
        distance_model_table_df = pd.read_csv(distance_model_table_fname, sep=' ', index_col=0)
    try:
        return distance_model_table_df.loc[age]['Model_filename'], \
            distance_model_table_df.loc[age]['Selected_features_filename']
    except Exception as e:
        print(f'Could not obtain distance model for age {age}: {e}')
        return None, None


def get_shape_corrector_model_and_featuremask_fnames(engine_config: EngineConfig, age: int) -> [str, str]:
    """
    Get path to shape_corrector model and feature mask for specified age

    :param engine_config: src engine config
    :param age: age
    :return: path to shape_corrector model and feature mask for specified age
    """
    d_param = get_params(engine_config.engine_dir_on_server
                         + "\\"
                         + os.path.basename(engine_config.main_params_dir),
                         "ObjectQualityEstimatorParams_shape_model_table")
    if d_param is None:
        return None, None
    shape_model_table_fname = os.path.join(engine_config.engine_dir_on_server, d_param)
    shape_model_table_df = pd.read_csv(shape_model_table_fname, sep=';', index_col=0)
    if len(shape_model_table_df.columns) == 0:
        shape_model_table_df = pd.read_csv(shape_model_table_fname, sep=' ', index_col=0)
    try:
        return shape_model_table_df.loc[age]['Model_filename'], \
            shape_model_table_df.loc[age]['Selected_features_filename']
    except Exception as e:
        print(f'Could not obtain density model for age {age}: {e}')
        return None, None


def get_engine_statistics(engine_config: EngineConfig, do_from_snapshot=False) -> Union[pd.DataFrame, None]:
    """
    Get statistics from engine_config

    :param engine_config:  src engine config
    :param do_from_snapshot: if True, get data from snapshot path , that is in results folder
    :return: statistics df or None if statistics file is not found
    """
    if do_from_snapshot:
        d_param_file_path = os.path.join(
            engine_config.engine_snapshot_dir,
            os.path.basename(engine_config.main_params_dir)
        )

        d_param = get_params(d_param_file_path,
                             "ObjectQualityEstimatorParams_experiment_feature_statistics_file")
        if d_param is None:
            return None
        engine_stats_filename = os.path.join(engine_config.engine_snapshot_dir, d_param)
    else:
        d_param = get_params(os.path.join(engine_config.engine_dir_on_server, engine_config.main_params_filename),
                             "ObjectQualityEstimatorParams_experiment_feature_statistics_file")
        if d_param is None:
            return None

        engine_stats_filename = os.path.join(engine_config.engine_dir_on_server, d_param)

    if os.path.exists(engine_stats_filename):
        res = load_statistics_from_csv(engine_stats_filename)
        return res
    else:
        return None


def get_engine_filt_coefs(engine_config: EngineConfig, do_from_snapshot=False):
    """
    Get filtration coefs from engine_config

    :param engine_config:  src engine config
    :param do_from_snapshot: if True, get data from snapshot path , that is in results folder
    :return: filtration coefs df
    """
    if do_from_snapshot:
        d_param = get_params(engine_config.engine_snapshot_dir
                             + "\\"
                             + os.path.basename(engine_config.main_params_dir),
                             "ObjectQualityEstimatorParams_filtration_coefficients_file")
        if d_param is None:
            return None
        filt_coefs_filename = engine_config.engine_snapshot_dir + "\\" + d_param
    else:
        d_param = get_params(engine_config.main_params_dir,
                             "ObjectQualityEstimatorParams_filtration_coefficients_file")
        if d_param is None:
            return None

        filt_coefs_filename = engine_config.engine_dir + "\\" + d_param

    if os.path.exists(filt_coefs_filename):
        res = load_statistics_from_csv(filt_coefs_filename)
        return res
    else:
        return None


def set_imagery_dir(engine_config: EngineConfig):
    act_param = get_params(engine_config.main_params_dir, "RPrepFactoryParams_imagery_folder")
    new_param = "\"../" + os.path.basename(engine_config.imagery_dir) + "/\""
    if act_param != new_param:
        params = {"RPrepFactoryParams_imagery_folder": new_param}
        return set_new_params(engine_config.main_params_dir, params)
    return True


def set_imagery_dir_new(engine_config: EngineConfig, new_imagery_folder: str):
    act_param = get_params(engine_config.main_params_dir, "RPrepFactoryParams_imagery_folder")
    new_param = "\"../" + new_imagery_folder + "/\""
    if act_param != new_param:
        params = {"RPrepFactoryParams_imagery_folder": new_param}
        set_new_params(engine_config.main_params_dir, params)


# deprecated wit v4.0
def check_and_update_engine_features(engine_config: EngineConfig):
    if not os.path.exists(engine_config.engine_dir + "\\" + get_stat_header_bat):
        # warnings.warn("\n\nNO {} for updating engine features. Can lead to engine errors!".format(
        #     get_stat_header_bat))
        return None

    log_print_header = "log_print_header_{}.txt".format(SESS_ID[:5])
    if os.system(engine_config.engine_dir + "\\" + get_stat_header_bat + " " + log_print_header) == 0:
        print("{} WAS UPDATED".format(get_stat_header_bat))
    else:
        print("Error during {} running".format(get_stat_header_bat))
    os.remove(engine_config.engine_dir + "\\" + log_print_header)

    if os.path.exists(engine_config.engine_dir + "\\" + stat_header_filename):
        df = pd.read_csv(engine_config.engine_dir + "\\" + stat_header_filename, sep=";")
        return df.columns.values
    else:
        print("No {} after launching {}".format(engine_config.engine_dir + "\\" + stat_header_filename,
                                                get_stat_header_bat))
        return None


def check_and_update_filtration_coefficients_file(engine_config: EngineConfig):
    filt_filename = get_params(engine_config.main_params_dir,
                               "ObjectQualityEstimatorParams_filtration_coefficients_file")

    if filt_filename == "":
        print("filtration_coefficients_file is not used")
        return True
    if not os.path.exists(engine_config.engine_dir + "\\" + filt_filename):
        print("filtration_coefficients_file {} is not exist".format(filt_filename))
        return True
    print("active filtrations:")
    df = pd.read_csv(engine_config.engine_dir + "\\" + filt_filename, sep=";", index_col=0)
    if len(df.columns) == 1:
        df = pd.read_csv(engine_config.engine_dir + "\\" + filt_filename, sep=" ", index_col=0)
    for c in df.columns:
        print(c)


def check_and_update_statistics(engine_config: EngineConfig, new_features, do_update=True) -> bool:
    stat_filename = get_params(engine_config.main_params_dir,
                               "ObjectQualityEstimatorParams_experiment_feature_statistics_file").replace(
        "\"", "")
    if stat_filename == "":
        print("statistics_file is not used")
        return True
    if not os.path.exists(engine_config.engine_dir + "\\" + stat_filename):
        print("statistics_file {} is not exist".format(stat_filename))
        return True
    df = pd.read_csv(engine_config.engine_dir + "\\" + stat_filename, sep=" ", index_col=0)

    new_features_stat = []
    for f in new_features:
        if "Target" in f:
            continue
        new_features_stat.append(f + "_mean")
        new_features_stat.append(f + "_stdev")

    do_update = not all(new_features_stat == df.columns)

    if do_update:
        for f in new_features:
            if "Target" in f:
                continue
            if f + "_mean" not in df.columns:
                df[f + "_mean"] = 0
            if f + "_stdev" not in df.columns:
                df[f + "_stdev"] = 10000

        df = df[new_features_stat]
        df.to_csv(engine_config.engine_dir + "\\" + stat_filename, sep=" ")
        print("{} WAS UPDATED".format(stat_filename))

    return all(new_features_stat == df.columns)


def check_and_update_feature_mask(engine_config: EngineConfig, new_features, do_update=True) -> bool:
    if_all_ok = True
    main_params_fname = engine_config.engine_snapshot_dir + "\\main_params.yml"

    def process(engine_config: EngineConfig, model_table_filename, new_features) -> bool:
        if not os.path.exists(model_table_filename):
            print("model_table {} is not exist".format(model_table_filename))
            return True

        df = pd.read_csv(model_table_filename, sep=" ", index_col=0)
        if_all_ok = True
        for i, r in df.iterrows():
            fmask_df = pd.read_csv(engine_config.engine_dir + "\\" + r["Selected_features_filename"], sep=";")
            if do_update:
                if any(new_features != fmask_df.columns):
                    for new_col in new_features:
                        if new_col not in fmask_df.columns:
                            fmask_df[new_col] = "skip"
                    fmask_df = fmask_df[new_features]
                    fmask_df.to_csv(engine_config.engine_dir + "\\" + r["Selected_features_filename"], index=False,
                                    sep=";")
                    print("{} WAS UPDATED".format(model_table_filename))
            if_all_ok = if_all_ok and all(new_features == fmask_df.columns)
        return if_all_ok

    print("========================")
    print("Checking shape_model:")
    p = get_params(main_params_fname, "ObjectQualityEstimatorParams_shape_model_table")
    shape_model_table_fname = p.replace(
        "\"",
        "")
    if shape_model_table_fname == "":
        print("shape_model_table is not used")
    else:
        if not process(engine_config, engine_config.engine_dir + "\\" + shape_model_table_fname, new_features):
            if_all_ok = False
            print("PROBLEMS WITH SHAPE MODEL")
        else:
            print("OK")
    print("========================")
    print("Checking global_model:")
    global_model_table_fname = get_params(main_params_fname, "ObjectQualityEstimatorParams_global_model_table").replace(
        "\"",
        "")
    if global_model_table_fname == "":
        print("global_model_table is not used")
    else:
        global_model_table_fname = global_model_table_fname.replace("\"", "")
        if not process(engine_config, engine_config.engine_dir + "\\" + global_model_table_fname, new_features):
            if_all_ok = False
            print("PROBLEMS WITH GLOBAL MODEL")
        else:
            print("OK")

    print("========================")
    print("Checking dist_model:")
    dist_model_table_fname = get_params(main_params_fname, "ObjectQualityEstimatorParams_distance_model_table")
    if dist_model_table_fname == "":
        print("dist_model_table is not used")
    else:
        dist_model_table_fname = dist_model_table_fname.replace("\"", "")
        if not process(engine_config, engine_config.engine_dir + "\\" + dist_model_table_fname, new_features):
            if_all_ok = False
            print("PROBLEMS WITH DIST MODEL")
        else:
            print("OK")
    return if_all_ok


def copy_engine(src, dst) -> bool:
    """
    Advanced function for engine copy. It copies only necessary files (only the ones, that are mentioned in main_params)
    Also need to update bat files using update_bats() afterwards (as they are unique for each machine)

    :param src: full path to folder with src engine
    :param dst: full path to dst folder
    :return: true if success
    """

    if not os.path.exists(src):
        print("source engine dir {} is not exists".format(src))
        return False
    if not os.path.exists(dst):
        print("Creating {} ".format(dst))
        os.makedirs(dst)

    main_params_filename = src + "\\" + EngineConfig.main_params_filename
    if not os.path.exists(src + "\\bin"):
        print(f"No bin folder in {src} folder exists.")
        return False
    if os.path.exists(dst + "\\bin"):
        shutil.rmtree(dst + "\\bin")

    while True:
        try:
            shutil.copytree(src + "\\bin", dst + "\\bin")  # , dirs_exist_ok=True)
            break
        except:
            print(f"Waiting for bin copy possibility from {src} to {dst}")
            time.sleep(1)

    if not os.path.exists(src + "\\OtherData"):
        print(f"No OtherData folder in {src} folder exists.")
        return False
    if os.path.exists(dst + "\\OtherData"):
        shutil.rmtree(dst + "\\OtherData")
    while True:
        try:
            shutil.copytree(src + "\\OtherData", dst + "\\OtherData")  # , dirs_exist_ok=True)
            break
        except:
            print(f"Waiting for OtherData copy possibility from {src} to {dst}")
            time.sleep(1)

    if os.path.exists(main_params_filename):
        shutil.copy2(main_params_filename, dst)
        with open(main_params_filename, 'r') as stream:
            for line in stream.read().splitlines():
                param_value = (line.split(": ")[-1]).replace("\"", "").replace("/", "\\")
                f_dir = src + "\\" + param_value
                if os.path.exists(f_dir) and os.path.isfile(f_dir):
                    shutil.copy2(f_dir, dst + "\\" + param_value)
                    # print(f_dir)
    else:
        print("No {}".format(main_params_filename))
        return False

    return True


def are_dir_trees_equal(dir1, dir2, mode="equal", message=[]) -> bool:
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    :param dir1: First directory path
    :param dir2: Second directory path
    :param mode: equal - dir2 is equal to dir1, in - all dir1 files should be in dir2
    :return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
   """

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    is_equal = True
    if len(dirs_cmp.left_only) > 0:
        print("MISSED FILES:")
        message.append("MISSED FILES:")
        for r in dirs_cmp.left_only:
            print(r)
            message.append(r)

        is_equal = False
    if len(dirs_cmp.right_only) > 0:
        print("NEW FILES:")
        message.append("NEW FILES:")
        for r in dirs_cmp.right_only:
            print(r)
            message.append(r)
        if mode == 'equal':
            is_equal = False
    if len(dirs_cmp.funny_files) > 0:
        print("FUNNY FILES:")
        message.append("FUNNY FILES:")
        for r in dirs_cmp.funny_files:
            print(r)
            message.append(r)
        is_equal = False

    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)

    if len(mismatch) > 0:
        print("MISMATCH FILES:")
        message.append("MISMATCH FILES:")
        for r in mismatch:
            print(r)
            message.append(r)

        is_all_not_critical = False
        if len(mismatch) == 1:
            if mismatch[0] == "main_params.yml":
                mismatch_params = compare_main_params(dir1 + "\\" + mismatch[0], dir2 + "\\" + mismatch[0])
                is_all_not_critical = True
                for param in mismatch_params:
                    if param not in not_critical_params:
                        is_all_not_critical = False
                        break
        is_equal = is_all_not_critical and is_equal

    if len(errors) > 0:
        print("ERRORS FILES:")
        message.append("ERRORS FILES:")
        for r in errors:
            print(r)
            message.append(r)
        is_equal = False

    if not is_equal:
        return False

    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2, message=message, mode='in'):
            return False
    return True


def compare_engine_with_snapshot(engine_config: EngineConfig, message: list, tmp_postfix: str = "test") -> bool:
    dir1 = engine_config.engine_snapshot_dir
    dir2 = engine_config.engine_dir + "\\" + "engine_snapshot_" + tmp_postfix

    if os.path.exists(dir2):
        shutil.rmtree(dir2)
    print("Making local engine snapshot in {}".format(dir2))
    copy_engine(engine_config.engine_dir, dir2)
    engines_are_equal = are_dir_trees_equal(dir1, dir2, message=message, mode='in')
    while True:
        try:
            shutil.rmtree(dir2)
            break
        except:
            pass

    return engines_are_equal


def get_engine_dir_on_server(engine_config):
    client = engine_config.define_client(engine_config.get_engine_postfix())
    if client == "":
        print(
            f"WARNING! No client defined for {engine_config.get_engine_postfix()}.\n"
            f"ENGINE_DIR folder will be {server_workdir}")

        return server_workdir + "\\" + os.path.basename(engine_config.engine_dir)
    return server_workdir + "\\" + client + "\\" + os.path.basename(engine_config.engine_dir)


def update_engine(engine_config, error_messages):
    if not os.path.exists(engine_config.engine_dir):
        print("Engine does not exist in local workdir {}".format(engine_config.workdir))
        engine_dir_on_server = get_engine_dir_on_server(engine_config)
        if os.path.exists(engine_dir_on_server):
            copy_engine(engine_dir_on_server, engine_config.engine_dir)
            print("Engine was taken from server")
        else:
            error_messages.append("Engine does not exist on server.\nCheck {}".format(engine_config.engine_dir))
            return False

    print("Updating bat files")
    if not update_bats(engine_config.engine_dir):
        error_messages.append("Problems with update_bats")
        return False
    return True


def engine_pre_check(engine_config: EngineConfig, error_messages):
    print("============= ENGINE PRE-CHECK==================")
    if not os.path.exists(engine_config.engine_dir):
        if not update_engine(engine_config, error_messages):
            return False

    """Checking if engine was launched before"""
    if not os.path.exists(engine_config.local_results_dir):
        print("No RESULTS dir for engine{}\nCreating...".format(engine_config.engine_version))
        os.makedirs(engine_config.local_results_dir)

        if engine_config.engine_version < "_v3.3":
            # TODO: deprecate if work ok with wrong header in explicit
            print("\n\n================================================")
            print("Checking Engine before first run")
            print("================================================")
            engine_features = check_and_update_engine_features(engine_config)
            if engine_features is None:
                print("Problems with extracting engine features")
                error_messages.append("Problems with extracting engine features")
                return False

            # TODO: deprecate after check
            print("\n================================================")
            print("Checking Statistics file")
            if not check_and_update_statistics(engine_config, engine_features):
                error_messages.append("Problems with check_and_update_statistics")
                return False

            # TODO: deprecate after check
            print("\n================================================")
            print("Checking feature_component mask file")
            if not check_and_update_feature_mask(engine_config, engine_features):
                error_messages.append("Problems with check_and_update_feature_mask")
                return False

    """Checking if engine snapshot exists"""
    if not os.path.exists(engine_config.engine_snapshot_dir):
        print("\n================================================")
        print("Engine snapshot does NOT exist in {}".format(engine_config.local_results_dir))
        copy_engine(engine_config.engine_dir, engine_config.engine_snapshot_dir)
        print('Snapshot was created in {}'.format(engine_config.local_results_dir))
    else:
        print("\n================================================")
        print("Engine snapshot EXISTS in {}".format(engine_config.local_results_dir))
        print("Comparing local engine with snapshot...")
        if not compare_engine_with_snapshot(engine_config, error_messages, str(SESS_ID)):
            print("\n================================================")
            """Trying to copy engine from snapshot """
            print("Trying to copy engine from snapshot")
            copy_engine(engine_config.engine_snapshot_dir, engine_config.engine_dir)
            print("Comparing local engine with snapshot...")
            if not compare_engine_with_snapshot(engine_config, error_messages, str(SESS_ID)):
                print("\n================================================")
                print(r"Even after engine update from snapshot Engine params are NOT equal.")
                print(r"Do you want to archive previous snapshot and replace it with new (y\n)?")
                answer = input()

                if answer == "y":
                    os.rename(engine_config.engine_snapshot_dir, engine_config.engine_snapshot_dir +
                              "_archive_{}".format(datetime.datetime.now().strftime(
                                  "%d-%m-%Y_%H-%M-%S")))
                    copy_engine(engine_config.engine_dir, engine_config.engine_snapshot_dir)
                    pass
                else:
                    return False

            else:
                print("\n================================================")
                print("Engine folder was updated with snapshot.")
        else:
            print("\n================================================")
            print("Engine is equal to snapshot.")

    # create link to right dll for engine starts from v4.10.7.25
    dst_engine_as_int = get_engine_v_ass_int(engine_config.engine_version)
    if dst_engine_as_int >= get_engine_v_ass_int("_v4.10.7.25"):
        logger.info(f'Create dynamic link for engine{engine_config.engine_version}')
        mklink_path = os.path.join(engine_config.engine_dir, mklink_bat)
        link_filder_path = os.path.join(engine_config.engine_dir, 'bin', extra_libs_link_name)
        if os.path.exists(link_filder_path):
            shutil.rmtree(link_filder_path)
        mklink_output = subprocess.run(mklink_path).returncode

        if mklink_output != 0:
            msg = f'Could not create link to dlls for engine{engine_config.engine_version}'
            error_messages.append(msg)
            return False

    print("\n================================================")
    print("Checking Imagery dir")
    if not set_imagery_dir(engine_config):
        error_messages.append("Problems with set_imagery_dir")
        return False

    return True


def compare_main_params(f1, f2):
    params1 = {}
    params2 = {}
    with open(f1, 'r') as stream:
        for line in stream.read().splitlines():
            try:
                cur_param_name, cur_param_value = line.split(": ")
                params1[cur_param_name] = cur_param_value
            except:
                pass

    with open(f2, 'r') as stream:
        for line in stream.read().splitlines():
            try:
                cur_param_name, cur_param_value = line.split(": ")
                params2[cur_param_name] = cur_param_value
            except:
                pass
    mismatched_params = [k for k in params1 if k in params2 and params1[k] != params2[k]]
    return mismatched_params


class DensityParams:
    def __init__(self):
        self.age = 0


def get_density_table(engine_config: EngineConfig):
    # check if density models are used
    density_models_table_fname = engine_config.engine_dir + "\\" + get_params(engine_config.main_params_dir,
                                                                              "ObjectQualityEstimatorParams_density_model_table")
    density = get_engine_density(engine_config, do_from_snapshot=True)

    if (density_models_table_fname is None) or (not os.path.exists(density_models_table_fname)):
        if density is None:
            print(f"Engine {engine_config.get_engine_postfix()} has wrong density settings. ")
            print(f"Engine density_models_table_fname is INVALID. ")
            print(f"Engine density from file is INVALID.")
            exit(1)

    #
    pass


def create_local_copy(config: EngineConfig, postfix="") -> [bool, EngineConfig]:
    engine_dir_on_server = config.engine_dir_on_server

    new_engine_postfix = "_".join([config.engine_version, postfix])
    config.set_another_engine_dir(new_engine_postfix)
    config.engine_dir_on_server = engine_dir_on_server

    if os.path.exists(config.engine_dir):
        print(f"Local copy of engine{config.engine_version} with postfix {postfix} alteady exists")
        return False, config

    if os.path.exists(config.engine_dir_on_server):
        if not copy_engine(config.engine_dir_on_server, config.engine_dir):
            print("Problems with copying engine from server to local workdir".format(config.engine_version,
                                                                                     server_workdir))
            return False, config
    else:
        print("engine{} does not exist on server.\nCheck {}".format(config.engine_version, server_workdir))
        return False, config

    print("Engine was taken from server")
    new_imagery_dir = "".join(["Imagery", config.get_engine_postfix()])
    config.imagery_dir = workdir + "\\" + new_imagery_dir

    return True, config


def delete_local_copy(config: EngineConfig):
    rmtree_time: int = 3  # seconds to wait for shutil func
    s0 = time.time()
    minutes_limit: float = 2.5  # minutes to wait for failures
    # now begin count
    if os.path.exists(config.engine_dir):
        while (time.time() - s0) / 60 < minutes_limit:
            try:
                shutil.rmtree(config.engine_dir)
                break
            except Exception as E:
                print(f"Trying to remove tmp engine dir {config.engine_dir}; " + \
                      f"min left: {((time.time() - s0) / 60 - minutes_limit):.2f}\n" + \
                      f"Caught exception: {E}")
                time.sleep(rmtree_time)

    s0 = time.time()
    if os.path.exists(config.imagery_dir):
        while (time.time() - s0) / 60 < minutes_limit:  # True:
            try:
                shutil.rmtree(config.imagery_dir)
                break
            except Exception as E:
                print(f"Trying to remove tmp engine dir {config.imagery_dir}" + \
                      f"min left: {((time.time() - s0) / 60 - minutes_limit):.2f}\n" + \
                      f"Caught exception: {E}")
                time.sleep(rmtree_time)
