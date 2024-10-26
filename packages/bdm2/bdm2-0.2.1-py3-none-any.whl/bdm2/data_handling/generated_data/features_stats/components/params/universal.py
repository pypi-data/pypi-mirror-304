from typing import List, Dict

from bdm2.constants.global_setup.data import max_age


class InterpolationParams:
    method: str = "polynomial"
    order: int = 3
    limit_direction: str = "both"
    downcast: str = "infer"


class UniversalParams:
    def __init__(self,
                 how,
                 features_params,
                 average,
                 client,
                 engine_postfix,
                 small_houses_num,
                 use_np,
                 ages,
                 smooth_window,
                 useFirstStandardValue,
                 useLastStandardValue,
                 iqr_percentiles, iqr_boundary_shift,
                 small_combinations_threshold, small_combinations_ages,
                 small_combinations_boundary_shifts, mean_coef):
        self.how: bool = how
        self.interpolation_params = InterpolationParams()
        self.features_params = features_params
        self.average: int = average
        self.client: str = client
        self.engine_postfix: str = engine_postfix
        self.small_houses_num: int = small_houses_num
        self.use_np: bool = use_np
        self.ages: List[int] = ages
        self.smooth_window: int = smooth_window
        self.useFirstStandardValue: bool = useFirstStandardValue
        self.useLastStandardValue: bool = useLastStandardValue
        self.iqr_percentiles: List[int] = iqr_percentiles
        self.iqr_boundary_shift: float = iqr_boundary_shift
        self.small_combinations_threshold: int = small_combinations_threshold
        self.small_combinations_ages: List[int] = small_combinations_ages
        self.small_combinations_boundary_shifts: List[int] = small_combinations_boundary_shifts
        self.mean_coef: List[float] = mean_coef

    class StaticParams:
        max_age: int = max_age + 1
        min_stdev_percent: float = 0.1
        spline_order: int = 3
        adapt_mean: bool = True
        gby: List[str] = ['cycle', 'house']
        weight_with_expected: bool = False
        boundaries: str = 'extreme'
        adjusted_weights: Dict[str, float] = {"interpolated": 0.75,
                                              "previous": 0.10}
        rel_error_threshold: float = 0.15
        num_curves: int = 0
        min_datapoints_for_curve: int = 4
        mean_check_how: str = 'any'
        mean_diff_thresh: float = 2.0
        interpolate_individually_adapted: bool = True
        update_negative_values: bool = False
        n_individual_house_std: int = 2
        n_all_houses_perf_std: int = 3
