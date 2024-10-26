import numpy as np
import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'scipy.signal',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

scipy_signal = checker.get_module('scipy.signal')

from bdm2.constants.global_setup.data import max_age


def interpolate_and_smooth_coefs(density_corr_coefs: pd.Series, smooth_window: int) -> pd.Series:
    """
    Take valid density_corr_coefs (can be defined not for all required ages) fill intermediate values with linear method
    Propagate last valid observation forward to max age
    Propagate first valid observation backward to 0 age

    :param density_corr_coefs: valid corr coefs with ages as index
    :param smooth_window: for smoothing corr coefs after extrapolation
    :return: corr coefs on full required age range
    """

    density_corr_coefs_full = pd.Series(index=np.arange(max_age))
    density_corr_coefs_full.loc[:] = density_corr_coefs
    # fill intermediate values with linear method
    min_valid_age = density_corr_coefs.index.min()
    max_valid_age = density_corr_coefs.index.max()
    density_corr_coefs.loc[min_valid_age: max_valid_age] = density_corr_coefs.loc[
                                                           min_valid_age:max_valid_age].interpolate(method='linear')
    # use next valid observation to fill gap
    density_corr_coefs_full = density_corr_coefs_full.fillna(method='bfill')
    # propagate last valid observation forward to next
    # To prevent bad impact of last point, will generate 5 extrapolation curves, that start from different last points
    # And choose median one
    extrapolation_variants = pd.DataFrame(index=density_corr_coefs_full.index, dtype=float)
    density_corr_coefs_full_cut = density_corr_coefs_full.copy()
    for i in range(5):
        if i > 0:
            last_not_nan_age = density_corr_coefs_full.dropna().index[-i]
            density_corr_coefs_full_cut[last_not_nan_age] = np.nan
        extrapolation_variants[i] = density_corr_coefs_full_cut.fillna(method='ffill')

    density_corr_coefs_full = extrapolation_variants.median(axis=1)

    if smooth_window > 1:
        density_corr_coefs_smoothed = scipy_signal.savgol_filter(density_corr_coefs_full, smooth_window, 1)
        density_corr_coefs_smoothed = scipy_signal.savgol_filter(density_corr_coefs_smoothed, smooth_window, 1)
    else:
        density_corr_coefs_smoothed = density_corr_coefs_full
    density_corr_coefs_smoothed = pd.Series(density_corr_coefs_smoothed, index=density_corr_coefs_full.index)
    return density_corr_coefs_smoothed


def calc_err(df: pd.DataFrame, target_col: str, pred_col: str) -> pd.Series:
    return df[pred_col] / df[target_col] - 1
