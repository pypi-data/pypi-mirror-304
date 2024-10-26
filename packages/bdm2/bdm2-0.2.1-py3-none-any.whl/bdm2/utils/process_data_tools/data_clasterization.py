import logging
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from bdm2.constants.global_setup.server_paths import device_csv
from bdm2.logger import build_logger
from bdm2.utils.dependency_checker import DependencyChecker
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.devices.devices_utils import (
    load_devices_from_csv,
)
from bdm2.utils.process_data_tools.components.explicits import explicit_manager

# from engine_config import *
# # from BIRDOO_IP import BirdooUtils, ExplicitManager
# from sklearn.cluster import MiniBatchKMeans, KMeans
# from sklearn.decomposition import PCA, LatentDirichletAllocation
# from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')

from bdm2.constants.global_setup.engine import EngineConfig


def reduce_data(
        df: pd.DataFrame,
        by: List[str],
        target: str,
        round_val: int = 1,
        decrease_rate: float = 0.3,
        n_attempts=5,
        verbose: bool = False,
        logger: Optional[logging.Logger] = None,
):
    """
    take df, cluster data by 'by' columns (using round values to define bins)
    then decrease number of samples inside this bin according to decrease_rate. then compare reduced mean target value
    with full bin mean target value. if difference too big, try one more time (max n_attempts times)
    """
    if not all([c in df.columns for c in by]):
        absent_columns = [c for c in by if c not in df.columns]
        logger.error(f"{absent_columns} columns are not in input df")
        raise ValueError(f"{absent_columns} columns are not in input df")
    if target not in df.columns:
        logger.error(f"{target} is not in input df")
        raise ValueError(f"{target} is not in input df")

    # check if by features are all not none
    if any(pd.isna(df[by + [target]]).any(axis=1)):
        logger.warning(f"input_df has nan values in 'by' or 'target' columns")
        raise ValueError(f"input_df has nan values in 'by' or 'target' columns")

    if logger is None:
        logger = logging.getLogger()
    # if decrease_count is None and decrease_rate is None:
    #     raise ValueError('decrease_rate or decrease_count should be defined')
    df_output = df.iloc[:0].copy()
    index_cols = []
    for ind in by:
        df[ind + "_round"] = df[ind].round(round_val)
        index_cols.append(ind + "_round")

    group_decrease_rate = decrease_rate
    # if group_decrease_rate is None:
    #     group_decrease_rate = decrease_count / len(df)
    # if group_decrease_rate > 1:
    #     group_decrease_rate = 1

    for _, group in df.groupby(index_cols):
        group_mean = group[target].mean()
        err_map = {}
        for _ in range(n_attempts):
            tmp_df = group.sample(int(np.ceil(len(group) * group_decrease_rate)))

            if len(tmp_df) == 0:
                break
            tmp_df_mean = tmp_df[target].mean()
            reduce_err = abs(tmp_df_mean - group_mean) / group_mean
            err_map[reduce_err] = tmp_df
            if reduce_err < 0.005:
                break
            else:
                pass
        if len(err_map) == 0:
            continue
        df_output = pd.concat(
            [df_output, err_map[min(list(err_map.keys()))]], ignore_index=True
        )
        # df_output = df_output.append(err_map[min(list(err_map.keys()))], ignore_index=True)

    df_output_mean = round(df_output[target].mean(), 4)
    df_mean = round(df[target].mean(), 4)
    err = (df_output_mean - df_mean) / df_mean
    if verbose:
        logger.info(f"before reduce:\n\tdata size: {len(df)}\n\tmean_mass: {df_mean}")
        logger.info(
            f"after reduce:\n\tdata size: {len(df_output)}\n\tmean_mass: {df_output_mean}"
        )
        logger.info(f"reduce err: {int(err * 1000) / 10}%")

    if abs(err) > 0.01:
        logger.info("Will NOT be added")
        return pd.DataFrame(columns=df.columns)

    return df_output[[c for c in df_output.columns if c not in index_cols]]


if __name__ == "__main__":
    logger = build_logger(Path(__file__), save_log=False)
    client = "Thailand"
    # client = "Cargill-NG"
    # client = "Japan"
    logger.info(f"Client: {client}")
    """
    =============================================
    Define engine
    """
    postfix = "_v4.0.5_Thailand_final_3009"
    results_postfix = ""
    # results_postfix = "_restore"

    engine_config = EngineConfig()
    engine_config.set_another_engine_version(postfix, results_postfix)

    logger.info("Results dir: {}".format(engine_config.local_results_dir))
    logger.info("Engine dir: {}".format(engine_config.engine_dir))

    """
    ==============================================
    Define filter
    """
    filters = Filter()
    filters.farms = [client]
    filters.cycles = ["Cycle 7"]
    filters.houses = ["House 1"]

    logger.info("\nFilter:")
    label = filters.generate_label(house=False)

    devices = load_devices_from_csv(device_csv)
    devices = filters.filter_devices(devices)
    for _, device in devices.iterrows():
        explicits_dir, explicits = explicit_manager.get_explicit_files(
            device, engine_config, filters, False
        )
        for explicit in explicits:
            df = explicit_manager.load_explicit(explicits_dir + "\\" + explicit)
            if df.empty:
                continue
            reduce_data(df, by=["volume_norm_corr", "daynum"], target="")
            pass
