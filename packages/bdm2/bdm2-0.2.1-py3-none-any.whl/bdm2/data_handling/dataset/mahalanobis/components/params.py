import pandas as pd
from pathlib import Path

from bdm2.constants.global_setup.data_columns import daynum_column, farm_column, cycle_column, std
from bdm2.logger import build_logger


class MahalanobisParameter:
    logger = build_logger(Path(__file__), save_log=False)

    def __init__(self,
                 df_of_interest: pd.DataFrame,
                 df_to_compare_with: pd.DataFrame,
                 filters_of_interest,
                 filters_to_compare_with,
                 ):
        self.df_of_interest = df_of_interest
        self.df_to_compare_with = df_to_compare_with
        self.filters_of_interest = filters_of_interest
        self.filters_to_compare_with = filters_to_compare_with
        self.dst_dir = "mahalanobis"
        self.indexing_type = "by_device"
        self.age_column = daynum_column
        self.features_set = {}
        self.compare_gby = [farm_column, cycle_column]
        self.exclude_gby = []
        self.m_th: float = 2.0
        self.p_th: float = 0.1
        self.age_window_size: int = 5
        self.zone_mode: str = std