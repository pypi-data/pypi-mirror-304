from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RolledCollectingParams:
    """


    :param work_dir: str
    :param log_folder: str

    :param match_index: define unique column in input df, to be used for matching data
    :param age_column: age column of input file
    :param engine_name_column: define engine that was used for required rolled files
    :param results_postfix_column: define results folder postfix

    :param rolled_track_id_column: column for grouping by track (always 'Track_ID' by default)
    :param rolled_age_column: age column of rolled files (always 'daynum' by default)
    :param gby_track_reliability: reliability column to be use as weight for grouping by track
           (in most cases should be taken from GlobalConfig.group_by_methods[active_group_by_method])

    :param features: features to be added from rolled. (i.e. volume_norm_corr, reliability, etc. not mean!!)
    :param keep_mean_values: if true, try to find {feature)_mean column in input data
           and shift rolled values to target mean values

    :param do_reducing: if true - reduce data
    :param reduce_target_count: target count of rolled samples for each row in group (500 by default)
    :param reduce_by: columns for bin definition
    :param reduce_target_column: columns for saving mean value of
    :param reduce_round_val: define bin accuracy
    :param reduce_n_attempts: as reducing has random behaviour it could be performed several times to keep mean values

    :param do_extrapolation: do extrapolation of rolled features
    :param extrapolated_flag_column: str = 'flag_extrapolated'

    .. note::
        keep_mean_values parameter is used for extending smoothed or filtered data and keeping desired mean values

    """

    work_dir: str
    log_folder: str
    age_column: str
    match_index: List[str]

    features: List[str]
    keep_mean_values: bool

    do_reducing: bool
    do_extrapolation: bool

    reduce_by: List[str]
    reduce_target_column: str

    engine_name_column: str
    results_postfix_column: str

    min_count: int = 500
    rolled_track_id_column: str = "Track_ID"
    rolled_sess_id_column: str = "Sess_ID"
    rolled_age_column: str = "daynum"

    gby_track_reliability: str = "private_reliability"

    # reducing params
    reduce_round_val: int = 1
    reduce_target_count: int = 500
    reduce_n_attempts: int = 5

    # extrapolation params
    extrapolated_flag_column: str = "flag_extrapolated"
    apply_extrapolation_to_raw_datapoints: bool = False
    extr_max_age: Optional[int] = None
    distrib_count_to_extrapolate: int = 5
    mean_values_smooth_window: int = 1

    def __str__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in self.__dict__.items()])
