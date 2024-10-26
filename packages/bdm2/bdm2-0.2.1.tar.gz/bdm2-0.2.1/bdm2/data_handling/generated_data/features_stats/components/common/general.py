import glob
import logging
import os
import pathlib
import re
from pathlib import Path
from typing import Optional, Any, List, Dict, Tuple

import pandas as pd

from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.data_handling.generated_data.features_stats.components.common.feature import Feature
from bdm2.data_handling.generated_data.features_stats.components.common.regular import get_apply_lambda
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.explicits.explicit_manager import get_explicit_files

# constants:
SMALL_COMB_IQR_KEY: str = 'small_comb_iqr'


class ExtraFeatures(Feature):
    def __init__(self, name, isRolled, isFilterable, n_left_stdev: Any, n_right_stdev: Any,
                 mean_stdev_from_src: bool, discard_percent: float = 5, agg: Optional[str] = 'mean',
                 adapt: Optional[bool] = True, individual_weight: Optional[float] = None,
                 useFirstStandardValue: Optional[bool] = None,
                 useLastStandardValue: Optional[bool] = None, ):
        # AssertionError section
        if n_left_stdev is not None:
            assert n_left_stdev > 0, f'n_left_stdev must be positive !'
        if n_right_stdev is not None:
            assert n_right_stdev > 0, f'n_right_stdev must be positive !'

        super().__init__(name=name, isRolled=isRolled, isFilterable=isFilterable)

        self.n_left_stdev = n_left_stdev
        self.n_right_stdev = n_right_stdev
        self.mean_stdev_from_src = mean_stdev_from_src
        self.discard_percent = discard_percent
        self.agg = agg
        self.adapt = adapt
        self.individual_weight = individual_weight
        self.useFirstStandardValue = useFirstStandardValue
        self.useLastStandardValue = useLastStandardValue

        # --- named attrs ---
        self.mean_name = f"{self.name}_mean"
        self.stdev_name = f"{self.name}_stdev"
        self.lstdev_coef_name = f"{self.name}_lstdev_coef"
        self.rstdev_coef_name = f"{self.name}_rstdev_coef"
        # self.q1_name = f"{self.name}_q1"
        # self.q3_name = f"{self.name}_q3"
        # for the iqr determination:
        self.lower_range_name = f"{self.name}_lower_range"
        self.upper_range_name = f"{self.name}_upper_range"
        self.filterable_name: str = f"{self.name}_filterable"
        # for more safe columns-usage:
        self.cols_to_replace: List[str] = [self.mean_name, self.stdev_name, self.lstdev_coef_name,
                                           self.rstdev_coef_name]

    @property
    def discard_percent(self):
        return self._discard_percent

    @discard_percent.setter
    def discard_percent(self, my_discard_percent):
        assert my_discard_percent > 0 and my_discard_percent < 100, f"discard_percent must be in the range of 0 and 100"
        self._discard_percent = my_discard_percent

    @property
    def n_right_stdev(self):
        return self._n_right_stdev

    @n_right_stdev.setter
    def n_right_stdev(self, n_right_stdev):
        if n_right_stdev != None:
            assert n_right_stdev > 0, f'n_right_stdev must be positive !'
        self._n_right_stdev = n_right_stdev

    @property
    def n_left_stdev(self):
        return self._n_left_stdev

    @n_left_stdev.setter
    def n_left_stdev(self, n_left_stdev):
        if n_left_stdev != None:
            assert n_left_stdev > 0, f'n_left_stdev must be positive !'
        self._n_left_stdev = n_left_stdev

    @property
    def mean_stdev_from_src(self):
        return self._mean_stdev_from_src

    @mean_stdev_from_src.setter
    def mean_stdev_from_src(self, mean_stdev_from_src):
        assert type(mean_stdev_from_src) == bool, f'type of "mean_stdev_from_src" must be bool !'
        self._mean_stdev_from_src = mean_stdev_from_src


def prepare_paths_info(df: pd.DataFrame, column_to_pattern: Dict[str, str],
                       cloud_way=False) -> pd.DataFrame:
    """

    @param df:
    @param column_to_pattern: contain columns-to-regex_patterns mapping;
        Example: you may use {'cycle': or_pattern_cycle} so you will add column 'cycle' and resulted values to it
    @return:
    """
    c_df = df.copy()
    # apply lambdas:
    for col, pattern in column_to_pattern.items():
        c_lambda = get_apply_lambda(pattern=pattern)
        c_df[col] = df['path'].apply(lambda x: c_lambda(x))
        del c_lambda

    return c_df


def increment_path(path, exist_ok=True, sep=''):
    # Increment path, i.e. runs/exp --> runs/exp{sep}0, runs/exp{sep}1 etc.
    path = Path(path)  # os-agnostic
    if (path.exists() and exist_ok) or (not path.exists()):
        return str(path)
    else:
        dirs = glob.glob(f"{path}{sep}*")  # similar paths
        matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]  # indices
        n = max(i) + 1 if i else 2  # increment number
        return f"{path}{sep}{n}"  # update path


def get_dirs_to_files(devices_loc: pd.DataFrame,
                      filters: Filter,
                      main_config: EngineConfig,
                      logger: logging.Logger,
                      useRolled: Optional[bool] = False) -> List[Tuple[str, List[str]]]:
    dirs_to_files = []
    for _, device in devices_loc.iterrows():
        try:
            if not filters.check_device(device):
                continue
            explicit_dir, explicit_files = get_explicit_files(device, main_config, filters, useRolled=useRolled)
            if len(explicit_files):
                dirs_to_files.append((explicit_dir, explicit_files))
        except Exception as E:
            logger.exception(E)

    return dirs_to_files


def check_path(filepath: Optional[pathlib.WindowsPath], prefix: Any = '') -> str:
    """

    @param filepath:
    @param prefix: datetime.datetime.now().strftime(_datetime_format)
    @return:
    """
    if filepath is not None:
        if filepath.exists():
            # rename it:
            basename = filepath.name
            new_basename = '_'.join(['renamed', str(prefix), basename])
            new_filepath = str(filepath).replace(basename, new_basename)
            return new_filepath

        else:
            return str(filepath)


def retrieve_from_logger(logger_fp: str,
                         level_name: str = '[ERROR]') -> List[str]:
    if not os.path.exists(logger_fp):
        return []
    with open(logger_fp, 'r') as file:
        lines = file.readlines()
    # now select lines where you have level_name:
    selected = [i for i in lines if level_name in i]
    return selected

# # iterate again to collect data for plot(ly):
#        for feature in features.keys():
#            if not features[feature].agg == 'skip':
#                # initialize graphs
#                plotly_graphs = SharedSubplots()
#
#                subset = percentage_stats_info.loc[percentage_stats_info.feature == features[feature].name, :]
#                metrics_to_plot = ['mean', 'std', 'lstdev', 'rstdev']
#                for metric in metrics_to_plot:
#                    metric_cols = subset.filter(regex=(f'.*{metric}.*')).columns
#                    cols_to_use = ['age'] + list(metric_cols)
#                    tmp_subset = subset.loc[:, cols_to_use]
#                    tmp_subset['metric'] = metric
#                    tmp_to_append = pd.DataFrame()
#                    for m_col in metric_cols:
#                        tmp_subset_copy = tmp_subset.copy()
#                        tmp_subset_copy['exact_metric'] = m_col
#                        tmp_subset_copy = tmp_subset_copy.rename(columns={f"{m_col}": 'metric_value'})
#                        tmp_to_append = pd.concat([tmp_to_append, tmp_subset_copy])
#                    dict_to_append = {'df': tmp_to_append, 'title_text': f"{metric}", 'gby': ['age'],
#                                  'feature_name': 'metric_value', 'x_colname': 'age'}
#
#                    plotly_graphs.append_n_prepare(dict_to_append)
#
#                plotly_graphs.plot(suptitle=f"feature: {subset['feature'].unique()[0]}; agg: {subset['agg'].unique()[0]}",
#                                   show=False, extra_legend_cols=['exact_metric'])
#                save_fp = Path(os.getcwd()) / 'tmp_plots'
#                if not save_fp.exists():
#                    save_fp.mkdir()
#                plotly_graphs.save_plots(save_dir=str(save_fp))
