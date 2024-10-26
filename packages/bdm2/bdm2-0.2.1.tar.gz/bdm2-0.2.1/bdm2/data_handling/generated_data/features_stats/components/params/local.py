from typing import Dict

from bdm2.constants.global_setup.server_paths import statistics_fname


class LocalWayParams:
    def __init__(self, res_df_postfix, output_folder_prefix, use_res_df, results_postfix):
        self.res_df_postfix: str = res_df_postfix
        self.output_folder_prefix: str = output_folder_prefix
        self.use_res_df: bool = use_res_df
        # self.how: str = how
        self.results_postfix: str = results_postfix

    output_filename_postfix: str = f"Generated_Statistics_{0}.csv"
    datapoints_num_thresh: int = 10000
    law: str = 'additive'
    statistics_fname: str = statistics_fname
    len_flag: bool = False
    shallow_filter: Dict = {}
