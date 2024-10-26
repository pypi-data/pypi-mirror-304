import warnings
from typing import List, Tuple, Any, Optional, Dict

import pandas as pd

from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values

# --- ints ---
MAX_DAY: int = 42
RANGE_STEP: int = 7

# dynamic constants:
KEY_DAYS = [i for i in range(7, MAX_DAY + 1, RANGE_STEP)]
REL_DIFF_COL: str = 'rel_diff'
AGE_COLNAME: str = 'daynum'
MEAN_ERR_KEY: str = 'mean_err'
ABS_MEAN_REL_ERR_KEY: str = 'abs_mean_rel_err'
CLOSEST_DAY_KEY: str = 'closest_day'
RESULTED_KEY: str = 'resulted'
RANGE_KEY: str = 'intersection_indices'


def check_max_day(series: pd.Series,
                  # day: int,
                  delta_range: int) -> int:
    """

    @param series: must be a pandas Series object with indices representing days (astype(int))
    @return:
    """
    #   1. get num of days left and right to current (max) day:
    day = max(series.index)
    c_range = set(range(day - delta_range, day + delta_range + 1, 1))
    #   2. intersect
    intersect = set(series.index).intersection(c_range)
    #   3. check if the max of it
    max_existing = max(intersect)
    if (max_existing - day) >= delta_range:
        return day
    else:
        return max_existing


def get_day_range(day: int, delta_range: int = 2,
                  min_day: int = 7, max_day: int = 42):
    if day <= min_day:
        c_range = list(range(day, day + delta_range + 1, 1))
    elif day >= max_day:
        c_range = list(range(day - delta_range, day + 1, 1))
    else:
        c_range = list(range(day - delta_range, day + delta_range + 1, 1))

    return c_range


def check_group(group: pd.DataFrame,
                rel_diff_colname: Optional[str] = REL_DIFF_COL,
                threshold: float = 0.05,
                delta_range: int = 2,
                age_colname: str = 'daynum',
                key_days: List[int] = [7, 14, 21, 28, 35, 42]):
    # intersection = set(group[age_colname].values).intersection(set(key_days))
    # intersection = sorted(list(intersection))
    working_copy = group.set_index(age_colname).copy()
    max_tuple = working_copy, None, None, None, None
    max_err: float = 0
    min_day: int = min(key_days)
    max_day: int = max(key_days)
    # for day in intersection:
    for day in key_days:
        # check max available day here:
        # working_copy.index
        c_range = get_day_range(day=day, delta_range=delta_range, min_day=min_day, max_day=max_day)

        index_intersection = set(working_copy.index.values).intersection(set(c_range))
        if len(index_intersection) == 0:
            continue
        # closest_day = min(list(index_intersection), key=lambda x: abs(x - day))
        # for_error = group.set_index(AGE_COLNAME)
        error_region = working_copy[working_copy.index.isin(index_intersection)][rel_diff_colname]
        mean_err = error_region.mean()
        if abs(mean_err) > max_err:
            max_err = mean_err
            max_tuple = (working_copy, error_region, day, mean_err, c_range)
        if abs(mean_err) > threshold:
            return working_copy, error_region, day, mean_err, c_range

    return max_tuple


def get_current_error(day: int,
                      curr_seq: Optional[pd.Series],
                      curr_tgt: Optional[pd.Series],
                      interpolated: Optional[pd.Series],
                      smooth_window: int,
                      average: int,
                      delta_range: int,
                      useFirstStandardValue: bool,
                      useLastStandardValue: bool,
                      key_days: List[int],
                      name: Tuple[Any],

                      ):
    if len(key_days) < 3:
        warnings.warn(f"{name}: {key_days} - at least 3 key days must be provided")
        return None
    # possible_max_day = check_max_day(curr_tgt,
    #                                  # day=day,
    #                                  delta_range=delta_range)

    # if possible_max_day != max_day:
    #     max_day_to_input = possible_max_day
    # else:
    #     max_day_to_input = max_day
    min_day = key_days[0]
    max_day = key_days[-1]

    closest_tgt_day = min(key_days, key=lambda x: abs(x - day))

    closest_tgt_idx: int = key_days.index(closest_tgt_day)
    # check for smallest values
    if closest_tgt_idx > 0:
        left_bound = key_days[closest_tgt_idx - 1] + 1
    else:
        left_bound = 0

    if closest_tgt_idx >= len(key_days) - 1:
        # remove all values up to max from given target:
        right_bound = int(curr_tgt.index.max())
    # elif closest_tgt_idx == 1:
    #     right_bound = day + delta_range
    else:
        # then it's an ordinary case where you can actually select the next value in the ordered list
        right_bound = key_days[closest_tgt_idx + 1] - 1

    assert left_bound >= 0 and right_bound >= 0, f''

    # left this for error calculation range
    c_range = get_day_range(day=day, min_day=min_day,
                            delta_range=delta_range,
                            max_day=max_day)

    index_intersection = set(curr_seq.index.values).intersection(set(c_range))
    if len(index_intersection) == 0:
        return None

    # here using left and right bounds select removal range:
    removal_range: List[int] = [i for i in range(left_bound, right_bound + 1, 1)]
    inputs = curr_tgt[~curr_tgt.index.isin(removal_range)]

    if len(interpolated) < 3 or len(inputs) < 3:
        warnings.warn(f"Got empty list for {name} during interpolation")
        return None
    try:
        # fig, ax = plt.subplots()
        # ax.plot(curr_tgt.index.values, curr_tgt.values, label='initial target', color='red')
        # ax.legend()
        # adjust_standard_to_values(
        #     standard=interpolated,
        #     initial_values=inputs,
        #     vis=True,
        #     smooth_window=smooth_window,
        #     average=average,
        #     useFirstStandardValue=useFirstStandardValue,
        #     useLastStandardValue=useLastStandardValue, ax=ax)
        resulted = adjust_standard_to_values(
            standard=interpolated,
            initial_values=inputs,
            vis=False,
            smooth_window=smooth_window,
            average=average,
            useFirstStandardValue=useFirstStandardValue,
            useLastStandardValue=useLastStandardValue)

        # tmp_df = pd.DataFrame()
        # interpolated.name = curr_tgt.name
        # interpolated_df = interpolated.reset_index()
        # interpolated_df['label'] = 'avg_d_x_volume'
        # curr_tgt_df = curr_tgt.reset_index()
        # curr_tgt_df['label'] = 'targets'
        #
        # inputs.name = curr_tgt.name
        # inputs_df = inputs.reset_index()
        # inputs_df['label'] = 'inputs'
        #
        # resulted.name = curr_tgt.name
        # resulted_df = resulted.reset_index()
        # resulted_df['label'] = 'resulted'
        #
        # tmp_df = pd.concat([tmp_df, interpolated_df, curr_tgt_df, resulted_df, inputs_df], axis=0, ignore_index=True)
        #
        # series_diff: pd.Series = ((resulted[resulted.index.isin(c_range)] - curr_tgt[curr_tgt.index.isin(c_range)]) /
        #                           curr_tgt[curr_tgt.index.isin(c_range)])
        #
        # mean_err = series_diff.mean()
        # title: str = f"error within range={c_range}: {mean_err:.3f}"
        # fig = px.scatter(tmp_df, x=curr_tgt.index.name, y=curr_tgt.name, title=title, color='label')
        # fig.show()

    except Exception as E:
        print(f"Caught exception during interpolation: {E}")
        return None
    # now select indices from resulted and check diff with initial values:
    series_diff: pd.Series = ((resulted[resulted.index.isin(c_range)] - curr_tgt[curr_tgt.index.isin(c_range)]) /
                              curr_tgt[curr_tgt.index.isin(c_range)])

    mean_err = series_diff.mean()
    abs_mean_rel_err = series_diff.abs().mean()

    closest_day = min(list(index_intersection), key=lambda x: abs(x - day))
    output_dict: Dict[str, Any] = {}
    output_dict[MEAN_ERR_KEY] = mean_err
    output_dict[ABS_MEAN_REL_ERR_KEY] = abs_mean_rel_err
    output_dict[CLOSEST_DAY_KEY] = closest_day
    output_dict[RESULTED_KEY] = resulted
    output_dict[RANGE_KEY] = list(index_intersection)
    return output_dict

    # if day != closest_day:
    #     warnings.warn(f"closest_day = {closest_day} != key day = {day}")
    # # try:
    # exact_err = (resulted[closest_day] - curr_tgt[closest_day]) / (curr_tgt[closest_day])
    # if pd.isnull(mean_err):
    #     # print(f"you shouldn't be there at day {day}")
    #     curr_info[f"{day}_error"] = -1
    #
    # else:
    #     curr_info[f"{day}_error"] = mean_err


if __name__ == '__main__':
    pass
    # true_outliers_slice_fp: str = r'E:\pawlin\OutliersSearch\diff_slice.csv'
    # delta_range: int = 2
    # threshold: float = 0.05
    # true_outliers_slice = pd.read_csv(true_outliers_slice_fp, sep=None, engine='python')
    # print(true_outliers_slice.head(3))
    # gby_dataset: List[str] = ['farm', 'cycle', 'house']  # , 'device']
    # extended_gby = gby_dataset + ['daynum']
    # is_avg_devices: bool = True
    # for groupname, subgroup_df in true_outliers_slice.groupby(gby_dataset):
    #     if is_avg_devices:
    #         group = subgroup_df.groupby(extended_gby).mean().reset_index()
    #     else:
    #         group = subgroup_df
    #
    #     a_group, error_region, a_day, mean_err = check_group(group=group, key_days=KEY_DAYS, age_colname=AGE_COLNAME)
    # intersection = set(group[AGE_COLNAME].values).intersection(set(KEY_DAYS))
    # intersection = sorted(list(intersection))
    #
    # for day in intersection:
    #     if day == 7:
    #         c_range = list(range(day, day + delta_range + 1, 1))
    #     elif day == 42:
    #         c_range = list(range(day - delta_range, day + 1, 1))
    #     else:
    #         c_range = list(range(day - delta_range, day + delta_range + 1, 1))
    #
    #     index_intersection = set(group[AGE_COLNAME].values).intersection(set(c_range))
    #
    #     mean_err = group[group[AGE_COLNAME].isin(c_range)][REL_DIFF_COL].mean()
    #
    #     if mean_err > threshold:
    #         print('here')
    # group[REL_DIFF_COL]
    # print(f"here")
    # intersection = set(curr_seq.index.values).intersection(set(KEY_DAYS))
    # intersection = sorted(list(intersection))
