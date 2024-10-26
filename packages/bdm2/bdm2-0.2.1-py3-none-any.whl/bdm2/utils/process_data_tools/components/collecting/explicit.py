"""
Tools for managing explicit and rolled files

"""
import datetime
import os
import secrets
import string
import time
import warnings
from pathlib import Path
from typing import List, Any, Union, Dict, Tuple, Optional

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')
import numpy as np
import pandas as pd
from brddb.utils.common import colorstr, warningColorstr, exceptionColorstr

from bdm2.constants.global_setup.data import valuable_reliability_columns
from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.explicits.explicit_files import (
    ExplicitFileConstants,
    FileExtensions,
)


from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'pyarrow.parquet',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

pq = checker.get_module('pyarrow.parquet')


import bz2
import io



class ExplicitFormat:
    """Define appropriate explicit file format.

    Properties:
        format -- all acceptable formats explicit file
        raw_format -- only raw acceptable formats explicit file
        compress_format -- only compress acceptable format explicit file
    """

    @property
    def raw_format(self):
        return ".txt", ".csv"

    @property
    def compress_format(self):
        return ".bz2"

    @property
    def format(self):
        return tuple(list(self.raw_format) + [self.compress_format])


class ExplicitFormatError(Exception):
    """Exception raised for errors in the explicit file format.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Explicit file has an incorrect format."):
        self.message = message
        super().__init__(self.message)


def stats_by_args(
        df, group_by_args: List[str], features: List[str], weight_coefs_column: str = "",
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
) -> pd.DataFrame:
    """
    Group by arguments: day_colname. Works only with numeric_features
    All string columns are grouped as first one in group.
    All reliability columns are grouped as simple mean
    All other digits columns are grouped as weighted mean

    :param df: df, that contains
    :param day_colname:
    :param features:
    :param weight_coefs_column:
    :return: mean, std, count for features, grouped by group_by_args
    :rtype: pd.DataFrame
    @param logger:
    @param weight_coefs_column:
    @param features:
    @param group_by_args:
    """
    active_features = list(set(features).intersection(set(df.columns)))
    active_group_by_args = list(set(group_by_args).intersection(set(df.columns)))

    for active_feature in active_features:
        if not np.issubdtype(df[active_feature].dtype, np.number):
            raise ValueError(f"Values for  {active_feature} are not numeric")

    if len(active_features) == 0:
        raise ValueError(f"No features {features} in df")
    if len(active_group_by_args) == 0:
        raise ValueError(f"No group_by_args {features} in df")
    if (weight_coefs_column not in df.columns) and (weight_coefs_column != ""):
        raise ValueError(f"No {weight_coefs_column} in df")

    df_by_day_stats = (
        df[active_features + active_group_by_args]
        .groupby(active_group_by_args)
        .agg(["mean", "std", "skew", pd.DataFrame.kurt, "count"])[features]
    )
    if set(df_by_day_stats.columns.get_level_values(0)).difference(set(df.columns)):
        logger.info(
            "WARNING in ExplicitManager.stats_by_args! Columns after group by are not equal"
        )

    for id, group in df.groupby(active_group_by_args):
        if weight_coefs_column == "":
            weights_coefs = pd.Series(1, index=group.index)
        else:
            weights_coefs = group[weight_coefs_column]
        group_wmean = ((group[features].T * weights_coefs).T).sum(
            min_count=1
        ) / weights_coefs.sum(min_count=1)
        group_wmean.name = id
        df_by_day_stats.loc[id, (features, "mean")] = group_wmean.values

    df_by_day_stats = (
        df_by_day_stats.stack(level=0)
        .reset_index(level=1)
        .rename(columns={"level_1": "feature"})
    )
    df_by_day_stats["CV"] = df_by_day_stats["std"] / df_by_day_stats["mean"]
    df_by_day_stats = df_by_day_stats.sort_index()
    return df_by_day_stats


def means_by_track(
        df,
        sess_id_colname: str,
        track_id_colname: str,
        age_colname: str,
        weight_coefs_column: str = "",
) -> pd.DataFrame:
    """
    Group by track. Group by arguments: age, sess_id, track_id.
    All string columns are grouped as first one in group.
    All reliability columns are grouped as simple mean
    All other digits columns are grouped as weighted mean

    :param df: Explicit or Rolled data for only one device in one cycle-house.
    :param sess_id_colname: no sess_id in raw explicit/rolled files. Could be defined with define_sess_ids().
        Or will be computed in this function if sess_id_colname not in df.columns
    :param track_id_colname: id of track in terms of 1 session
    :param age_colname: age/daynum column
    :param weight_coefs_column: coefs, that are used as weights in weighted mean function
    :return: df grouped by track
    """
    # define group by columns
    gb_columns = [age_colname, sess_id_colname, track_id_colname]
    initial_cols = df.columns
    loc_df = df.copy()

    exist_flag = True
    if sess_id_colname not in loc_df.columns:
        exist_flag = False
        # define sess from image_name column
        loc_df[sess_id_colname] = define_sess_ids(loc_df, 5)

    # loc_df = loc_df.groupby(gb_columns).get_group((44, 2, 16597))
    output_df = means_by(
        loc_df, gb_columns, weight_coefs_column
    )  # .drop([sess_id_colname], axis=1)
    if not exist_flag:
        output_df = output_df.drop([sess_id_colname], axis=1)
    return output_df


def means_by_sess(
        df, sess_id_colname: str, age_colname: str, weight_coefs_column: str = ""
) -> pd.DataFrame:
    """
    Group by track. Group by arguments: age, sess_id, track_id.
    All string columns are grouped as first one in group.
    All reliability columns are grouped as simple mean
    All other digits columns are grouped as weighted mean

    :param df: Explicit or Rolled data for only one device in one cycle-house.
    :param sess_id_colname: no sess_id in raw explicit/rolled files. Could be defined with define_sess_ids().
        Or will be computed in this function if sess_id_colname not in df.columns
    :param track_id_colname: id of track in terms of 1 session
    :param age_colname: age/daynum column
    :param weight_coefs_column: coefs, that are used as weights in weighted mean function
    :return: df grouped by track
    """
    # define group by columns
    gb_columns = [age_colname, sess_id_colname]
    initial_cols = df.columns
    loc_df = df.copy()

    exist_flag = True
    if sess_id_colname not in loc_df.columns:
        exist_flag = False
        # define sess from image_name column
        loc_df[sess_id_colname] = define_sess_ids(loc_df, 5)

    # loc_df = loc_df.groupby(gb_columns).get_group((44, 2, 16597))
    output_df = means_by(
        loc_df, gb_columns, weight_coefs_column
    )  # .drop([sess_id_colname], axis=1)
    if not exist_flag:
        output_df = output_df.drop([sess_id_colname], axis=1)
    return output_df


def means_by_age(df, age_colname: str, weight_coefs_column: str = "") -> pd.DataFrame:
    """
    Group by age. Group by arguments: age.
    All string columns are grouped as first one in group.
    All reliability columns are grouped as simple mean
    All other digits columns are grouped as weighted mean

    :param df: Explicit or Rolled data for only one device in one cycle-house.
        Or will be computed in this function if sess_id_colname not in df.columns
    :param age_colname: age/daynum column
    :param weight_coefs_column: coefs, that are used as weights in weighted mean function
    :return:
    :rtype: pd.DataFrame
    """

    # define group by columns
    gb_columns = [age_colname]
    loc_df = df.copy()
    output_df = means_by(loc_df, gb_columns, weight_coefs_column)

    return output_df


def means_by(
        df: pd.DataFrame,

        group_by_columns: List[str],
        weight_coefs_column: str = "",
        add_count=False,
        count_column: str = "count",
        save_dtypes: bool = False,
        use_median: bool = False,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
        debug=True,
) -> pd.DataFrame:
    """
    Group by track. Group by arguments: age, sess_id, track_id.
    All string columns are grouped as first one in group.
    All reliability columns are grouped as simple mean
    All other digits columns are grouped as weighted mean

    :param df: Explicit or Rolled data for only one device in one cycle-house.
    :param sess_id_colname: no sess_id in raw explicit/rolled files. Could be defined with define_sess_ids().
        Or will be computed in this function if sess_id_colname not in df.columns
    :param track_id_colname: id of track in terms of 1 session
    :param age_colname: age/daynum column
    :param weight_coefs_column: coefs, that are used as weights in weighted mean function
    :param save_dtypes: if true, convert output columns to initial dtypes. Can be usefull if want to save int columns
    :return:
    :rtype: pd.DataFrame
    """

    # define group by columns
    gb_columns = group_by_columns
    initial_cols = df.columns
    initial_dtypes = df.dtypes

    loc_df = df.copy()
    # check necessary columns
    if any([col not in df.columns for col in group_by_columns]):
        raise ValueError(
            f"ValueError: Not all group_by_columns {group_by_columns} in df"
        )

    loc_df = loc_df.set_index(gb_columns)
    if weight_coefs_column == "":
        weight_coefs = pd.Series(1, index=loc_df.index)
    elif weight_coefs_column in df.columns:
        weight_coefs = loc_df[weight_coefs_column]
    else:
        raise ValueError(f"means_by_track: ValueError: No {weight_coefs_column} in df")

    # define columns with string values. Will be taken the FIRST one in group
    str_columns = [
        col
        for col in loc_df.columns
        if loc_df[col].dtype == "object"
           or loc_df[col].dtype == datetime.datetime
           or pd.api.types.is_datetime64_any_dtype(loc_df[col])
    ]
    # define reliability by columns. Will be taken the MEAN in group
    reliability_columns = valuable_reliability_columns
    reliability_columns = list(set(reliability_columns).intersection(set(initial_cols)))

    # define all other features columns. Will be taken the WEIGHTED MEAN in group
    digit_cols = list(
        set(initial_cols)
        .difference(str_columns)
        .difference(reliability_columns)
        .difference(gb_columns)
    )

    str_df = loc_df.groupby(gb_columns)[str_columns].first()
    rel_df = loc_df.groupby(gb_columns)[reliability_columns].mean()

    # calculating weighted mean

    if use_median:
        digits_df = loc_df.groupby(gb_columns)[digit_cols].median()
    else:
        digits_df = loc_df[digit_cols].copy()
        digits_df_weights = loc_df[digit_cols].copy()
        for col in digit_cols:
            digits_df[col] = digits_df[col] * weight_coefs
            digits_df_weights[col] = weight_coefs * (1 - digits_df[col].isna())

        digits_df_sum = digits_df.groupby(gb_columns).sum(min_count=1)
        reliability_sum = digits_df_weights.groupby(gb_columns).sum(min_count=1)

        digits_df = digits_df_sum / reliability_sum

    # concatenating all dfs
    output_df = pd.concat(
        [
            str_df.reset_index(),
            digits_df.reset_index(drop=True),
            rel_df.reset_index(drop=True),
        ],
        axis=1,
    )[initial_cols]
    if add_count:
        output_df[count_column] = (
            loc_df.groupby(gb_columns, as_index=False).count()[loc_df.columns[0]].values
        )
    if debug:
        logger.info(
            f"means_by stat:\n"
            f"\tstr columns count: {len(str_columns)}\n"
            f"\trelability columns count: {len(reliability_columns)}\n"
            f"\tdigits columns count: {len(digit_cols)}"
        )

    if save_dtypes:
        problem_cols = []
        for c in output_df.columns:
            if c in initial_dtypes:
                try:
                    output_df[c] = output_df[c].astype(initial_dtypes[c])
                except Exception as e:
                    problem_cols.append(c)
        if len(problem_cols):
            logger.info(
                colorstr(
                    "yellow", f"means_by: could not save dtypes for {problem_cols}"
                )
            )
    return output_df


def define_sess_ids(df: pd.DataFrame, sess_gap_in_minutes: float = 5,
                    logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
                    ) -> pd.Series:
    """
    Return unique sess ids for df. Sess defines as group of measurements divided by time interval sess_gap_in_minutes

    :param df: explicit/rolled file format
    :param sess_gap_in_minutes: time interval sess_gap_in_minutes
    :return: pd.Series with correspondent sess ids
    :rtype: pd.Series
    """

    ts = get_s_datetime_from_Image_name(df)
    ts = ts.sort_values()
    ts_diff = ts - ts.shift(1)

    #  reset index to use .iloc[ind:]
    new_sess_start = (
            ts_diff > datetime.timedelta(minutes=sess_gap_in_minutes)
    ).reset_index(drop=True)
    sessions_count = new_sess_start.sum()
    inds = new_sess_start[new_sess_start == True].index.values
    inds.sort()
    sess_ids = pd.Series(0, index=ts.index)
    for ind in inds:
        sess_ids.iloc[ind:] += 1
    logger.info(f"sessions_count: {sessions_count}")

    sess_ids = sess_ids.sort_index()
    return sess_ids


def combine_explicits(df1: pd.DataFrame, df2: pd.DataFrame, replace=False,
                      logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
                      ):
    main_df = df1
    add_df = df2

    main_sess_column = get_datetime_from_Image_name(main_df)
    add_sess_column = get_datetime_from_Image_name(add_df)

    union_sess = np.unique(
        list(set(main_sess_column).intersection(set(add_sess_column)))
    )
    logger.info("{} images are replaced".format(len(union_sess)))

    if replace:
        main_sess_column_to_add = np.unique(
            list(set(main_sess_column).difference(set(add_sess_column)))
        )
        add_sess_column_to_add = np.unique(add_sess_column)
    else:
        main_sess_column_to_add = np.unique(main_sess_column)
        add_sess_column_to_add = np.unique(
            list(set(add_sess_column).difference(set(main_sess_column)))
        )

    out_df = main_df[np.isin(main_sess_column, main_sess_column_to_add)]
    out_df = pd.concat(
        [out_df, add_df[np.isin(add_sess_column, add_sess_column_to_add)]],
        ignore_index=True,
    )

    return out_df


def get_union_columns(cols1: List[Any], cols2: List[Any]):
    return list(set(cols1).intersection(set(cols2)))


def drop_header_rows_from_df(df: pd.DataFrame) -> pd.DataFrame:
    df_output = df.copy()
    for col in df.columns:
        df_output = df_output[df_output[col] != col]

    for col in df_output.columns:
        try:
            df_output[col] = df_output[col].astype(float)
        except:
            pass
    return df_output


def pyarrow_parquet_to_pd(path: str) -> pd.DataFrame:
    # https://medium.com/productive-data-science/why-you-should-use-parquet-files-with-pandas-b0ca8cb14d71
    pqfile = pq.read_table(path)
    df = pqfile.to_pandas()
    return df


def _clean_explicit(df: pd.DataFrame) -> pd.DataFrame:
    column_mask: List[str] = [x for x in df.columns if "Unnamed" not in x]
    df = df.loc[:, column_mask]  # [[x for x in df.columns if "Unnamed" not in x]]
    # TODO: check if how='any' is desired behaviour
    df = df.dropna(subset=df.columns, axis=0, how="any")
    return df


def load_explicit(
        explicit_filename: str, sep: str = ";", drop_header_rows: bool = False,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
) -> pd.DataFrame:
    """
    Must return directory and RELATIVE paths (!)
    @param explicit_filename:
    @param sep:
    @param drop_header_rows:
    @return:
    """
    if not os.path.exists(explicit_filename):
        return pd.DataFrame()
    # cls_format_instance = ExplicitFormat()
    # compress_format: str = cls_format_instance.compress_format
    available_formats: Tuple[str] = (
        ExplicitFileConstants.available_extensions
    )  # cls_format_instance.format

    condition = any([explicit_filename.endswith(x) for x in available_formats])
    if not condition:
        raise ExplicitFormatError(
            message=f"{explicit_filename} must ends with {' ,'.join(available_formats)}"
        )

    df: Optional[pd.DataFrame] = None
    path_or_buffer: Union[str, io.StringIO] = explicit_filename
    # now start with the fastest ones:
    if explicit_filename.endswith(FileExtensions.parquet):
        df = pyarrow_parquet_to_pd(explicit_filename)
        # return df
    elif explicit_filename.endswith(FileExtensions.feather):
        # for .feather format there's no big difference between pandas and pyarrow so let it be so
        df = pd.read_feather(explicit_filename)
        # return df
    elif explicit_filename.endswith(FileExtensions.bz2):
        with bz2.open(explicit_filename, "rb") as fin:
            tmp_str_buffer = fin.read().decode()
        path_or_buffer = io.StringIO(tmp_str_buffer)

    if any(
            [
                explicit_filename.endswith(FileExtensions.txt),
                explicit_filename.endswith(FileExtensions.csv),
                explicit_filename.endswith(FileExtensions.bz2),
            ]
    ):

        try:
            df = pd.read_csv(path_or_buffer, sep=sep, low_memory=False)
        except pd.errors.ParserError:
            # still explicit_filename due to the fact than filepath_to_read can be buffer rather than path
            logger.info(
                f"{explicit_filename} has bad lines. Work on explicit could be incorrect"
            )
            df = pd.read_csv(path_or_buffer, sep=sep, on_bad_lines="skip")
        except Exception as e:
            raise Exception(f"ERROR: {e}")

        if len(df.columns) == 1:
            raise ExplicitFormatError(
                message=f"{explicit_filename} has only one column. "
                        f"Maybe cause of wrong sep, check file. expected sep={sep}"
            )

    assert df is not None, f"Check if/else statements"
    if (len(df.columns) > 0) and drop_header_rows:
        df = drop_header_rows_from_df(df)
    # fixed slicing:
    # TODO: maybe ? column_mask: List[bool] = ["Unnamed" not in x for x in df.columns]
    column_mask: List[str] = [x for x in df.columns if "Unnamed" not in x]
    df = df.loc[:, column_mask]  # [[x for x in df.columns if "Unnamed" not in x]]
    # TODO: check if how='any' is desired behaviour
    df = df.dropna(subset=df.columns, axis=0, how="any")
    return df


def get_only_not_filtered(df: pd.DataFrame, logger=build_logger(file_name=f"{Path(__file__)}", save_log=False), ) -> pd.DataFrame:
    """
    Retuturn only data , where df["Filters"] == "none" . If Filters is not in df columns, return full df

    :param df: DataFrame with Filters columns.
    :return: filtered DataFrame
    :rtype: pd.DataFrame
    """
    if "Filters" not in df.columns:
        logger.info("'Filters' not in df.columns")
        return df
    return df.loc[df["Filters"] == "none"]


def get_unique_filename_body(name_char_num: int) -> str:
    output = "".join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(name_char_num)
    )
    return output


def _implicit_save_explicit(
        df: pd.DataFrame, extension: str, explicit_filename: str
) -> None:
    if (extension == FileExtensions.txt) or (extension == FileExtensions.csv):
        df.to_csv(explicit_filename, **ExplicitFileConstants.save_kwargs)
    elif extension == FileExtensions.bz2:
        # 'sep' and 'index' are replaced with kwargs unpacking
        name_char_num: int = 9
        timeout_limit: int = 10
        unique_hash_name: str = get_unique_filename_body(name_char_num)
        s0: float = time.time()
        while os.path.exists(unique_hash_name) is True:
            unique_hash_name = get_unique_filename_body(name_char_num)
            curr_time_diff: float = time.time() - s0
            if curr_time_diff > timeout_limit:
                error_msg: str = (
                    f"Cannot generate unique filename for temporary binary file "
                    f"for {explicit_filename} for {curr_time_diff:.3f} seconds exceeding "
                    f"timeout limit = {timeout_limit} seconds"
                )
                raise TimeoutError(error_msg)

        df.to_csv(unique_hash_name, **ExplicitFileConstants.save_kwargs)
        with open(unique_hash_name, mode="rb") as fin, bz2.open(
                explicit_filename, "wb"
        ) as fout:
            fout.write(fin.read())

        os.remove(unique_hash_name)
        # ExplicitCompressor.compress_pandas(df=df,
        #                                    **ExplicitFileConstants.save_kwargs,
        #                                    file_path_out=explicit_filename)
    elif extension == FileExtensions.parquet:
        df.to_parquet(explicit_filename)

    elif extension == FileExtensions.feather:
        df.to_feather(explicit_filename)

    else:
        raise NotImplementedError(
            f"unknown condition: extension = {extension}; "
            f"check either you constants classes or this part of the code"
        )


# TODO: add decorator which will catch exceptions like
#       @throwsException
#   and apply it to this func
def save_explicit(
        df: pd.DataFrame, explicit_filename: str, need_clean: bool = False
) -> bool:
    # TODO: allow it to work with Union[Path, str]
    # TODO: maybe rename explicit_filename to explicit_filepath
    #   or simply path/filepath?
    #   you even take parent dir to check it's existence so it's better to use variable names as what they really are
    #   (check how much (i hope not so) usages this func have and replace keywords)
    """
    Save explicit to explicit_filename

    :param df: pandas DataFrame
    :param explicit_filename: full path to dst file
    :param need_clean: whether your input should be prepared (unnamed cols, nans, headers etc) or not
    :return: True if success
    :rtype: bool
    """
    parent_dir = os.path.dirname(explicit_filename)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    extension: str = ExplicitFileConstants.get_extension(explicit_filename)
    if extension not in ExplicitFileConstants.available_extensions:
        error_msg: str = (
            f"for path {explicit_filename} got extension = {extension}; "
            f"available ones are: {ExplicitFileConstants.available_extensions}"
        )
        # raise AssertionError(error_msg)
        warnings.warn(warningColorstr(error_msg))
        return False

    if need_clean:
        df = _clean_explicit(df)

    # now it comes to if/else statements:
    _implicit_save_explicit(
        df, extension=extension, explicit_filename=explicit_filename
    )
    return True


def convert_explicit(
        path: str,
        logger,
        mode: Optional[str] = None,
        drop_header_rows: bool = True,
        delete_source: bool = True,
        verbose: bool = True,
        replace: bool = False,
        handle_exception: bool = True,
) -> Tuple[bool, Optional[str]]:
    """
    Returns True if converting succeeded else False

    @param mode: like 'parquet', 'feather', 'bz2' etc
        now can be added also an extension:
    @param drop_header_rows: see load_explicit
        drops header rows in the body of dataframe
    """

    if mode.startswith(ExplicitFileConstants.splitter):
        # mode must be an extension without '.' (dot) (!)
        mode = mode.lstrip(ExplicitFileConstants.splitter)

    assert (
            mode in ExplicitFileConstants.available_format_keys
    ), f"got mode={mode}; available format keys are {ExplicitFileConstants.available_format_keys}"

    src_ext: str = ExplicitFileConstants.get_extension(path)
    tgt_ext: str = ExplicitFileConstants.format_to_extension_mapping[mode]
    tgt_path = path.replace(src_ext, tgt_ext)

    # should_remove: bool = False
    if tgt_path == path:
        # todo: add unittests
        if replace is False:
            warn_msg: str = (
                f"source path and replaced path are equal: {path} == {tgt_path}; "
                f"file won't be rewritten since replace={replace}"
            )
            if logger is not None:
                logger.warning(warn_msg)
            else:
                logger.info(warningColorstr(warn_msg))
            return False, tgt_path
        else:
            if verbose:
                warn_msg: str = (
                    f"file at path {path} will be overwritten since "
                    f"replace={replace} (extensions are equal)"
                )
                if logger is not None:
                    logger.warning(warn_msg)
                else:
                    logger.info(warningColorstr(warn_msg))

            # should_remove = True

    # then change it:
    assert tgt_ext in ExplicitFileConstants.available_extensions, f"check the code"

    # 1. save it:
    df = load_explicit(path, drop_header_rows=drop_header_rows)
    # save it:
    save_explicit(df, tgt_path)
    # try to load again:
    try:
        load_explicit(tgt_path)
        # in that case you can delete
        if delete_source:
            # but now you actually have the opportunity
            #   for equal initial (path) and target (tgt_path)
            # so remove in the case they are NOT the same (!)
            # TODO: add unittests
            if tgt_path != path:
                os.remove(path)
            elif verbose:
                is_path_exists: bool = os.path.exists(tgt_path)
                warn_msg: str = (
                    f"delete_source={delete_source} but tgt_path == initial; "
                    f"path {tgt_path} exists: {is_path_exists}"
                )
                assert (
                        is_path_exists is True
                ), f"stmh went wrong: {tgt_path} should not be deleted; check if/else statements"
                if logger is not None:
                    logger.warning(warn_msg)
                else:
                    logger.info(warningColorstr(warn_msg))

            if verbose:
                info_msg: str = (
                    f"df can be loaded from new path {tgt_path}; source was deleted at path {path}"
                )
                if logger is not None:
                    logger.info(info_msg)
                else:
                    logger.info(info_msg)
                # logger.info(f"df can be loaded from new path {tgt_path}; deleted source at path {path}")

        return True, tgt_path

    except Exception as E:
        if handle_exception is False:
            raise E
        error_msg: str = (
            f"Caught exception {E} during loading dataframe at new path {tgt_path}; "
            f"source path cannot be replaced with given mode={mode} "
            f"and ext={tgt_ext}; removing it..."
        )
        if verbose:
            logger.info(exceptionColorstr(error_msg))

        # delete target if and only if it's NOT equal to source:
        if tgt_path != path:
            os.remove(tgt_path)

        return (
            False,
            None,
        )  # TODO: maybe it's better to return initial filepath in that case?


def get_age_from_explicit_file(explicit_filename: str) -> Union[int, None]:
    """
    Define age from explicit_filename

    :param explicit_filename: full or base explicit filename
    :return: age as int
    :rtype: int, None
    """
    basename = os.path.basename(explicit_filename)
    try:
        age_ind = basename.find("_age_")
        if age_ind < 0:
            return None
        return int(basename[age_ind + 1:].split(".")[-2].split("_")[1])
    except:
        return None


def get_sess_id_from_explicit_file(explicit_filename: str) -> Union[int, None]:
    """
    Define sess_id  from explicit_filename

    :param explicit_filename:  full or base explicit filename
    :return: sess_id as int
    """
    basename = os.path.basename(explicit_filename)
    try:
        sess_ind = basename.find("_sess_")
        if sess_ind < 0:
            return 0
        return int(basename[sess_ind + 1:].split(".")[-2].split("_")[1])
    except:
        return None


def get_datetime_from_Image_name(df: pd.DataFrame) -> List[datetime.datetime]:
    return list(get_s_datetime_from_Image_name(df))


def get_s_datetime_from_Image_name(df: pd.DataFrame,
                                   logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
                                   ) -> pd.Series:
    if "Image_name" not in df.columns:
        logger.info("No Image_name in df columns")
        return pd.Series(dtype=float)
    try:  # From rolled
        datetima_values = pd.to_datetime(
            df["Image_name"].values.astype(datetime.datetime)
        ).values
    except:  # From explicit
        datetima_values = pd.to_datetime(
            list(
                map(
                    lambda x: "_".join(
                        os.path.basename(x)[len("depthMap"):].split(".")[:-2]
                    ),
                    df["Image_name"],
                )
            ),
            format="%Y_%m_%d_%H_%M_%S",
        )
    return pd.Series(datetima_values, index=df.index)


def filter_by_time(df: pd.DataFrame, filters: Filter,
                   logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
                   ) -> pd.DataFrame:
    """
    FIlter by time, based on Image_name column

    :param df: explicit or rolled df
    :param filters:
    :return: filtered df
    :rtype: pd.DataFrame
    """
    if df["Image_name"].dtype == np.int64:
        logger.info("Image_name has wrong format. NO data will be filtered")
        return df
    if filters.start_time is None and filters.end_time is None:
        return df

    time = pd.Series(
        [t.time() for t in get_datetime_from_Image_name(df)], index=df.index
    )
    df_output = df.copy()

    if filters.start_time is not None:
        time = time.iloc[time.values > filters.start_time.time()]
    if filters.end_time is not None:
        time = time.iloc[time.values < filters.end_time.time()]
    df_output = df_output.loc[time.index]
    return df_output


def get_explicit_distribution_statistics(
        explicit_df: pd.DataFrame, columns: List[str],
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
) -> pd.DataFrame:
    union_columns = get_union_columns(list(explicit_df.columns), columns)
    logger.info("Columns for distribution_statistics: {}".format(union_columns))
    explicit_df_valusble = explicit_df[union_columns]
    df = pd.DataFrame(index=[union_columns])

    df["mean"] = explicit_df_valusble.mean().values
    df["stdev"] = explicit_df_valusble.std().values
    df["count"] = explicit_df_valusble.count().values
    df["skew"] = explicit_df_valusble.skew().values
    df["kurtosis"] = explicit_df_valusble.kurtosis().values

    return df


def compare_explicits_by_day(
        explicits_map: pd.DataFrame, columns: List[str], plot_type=plt.plot,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
):
    for column in columns:
        plt.figure()
        for explicit_label in explicits_map:
            mean_by_day_df = (
                explicits_map[explicit_label].groupby("daynum", as_index=False).mean()
            )
            plot_type(
                mean_by_day_df["daynum"], mean_by_day_df[column], label=explicit_label
            )
            logger.info(
                "{} contains {} samples".format(
                    explicit_label, len(explicits_map[explicit_label])
                )
            )
        plt.title(column)
        plt.legend()

    plt.show()


def list_explicits(dirpath: str) -> List[str]:
    """
    Returns list of unique filenames (basenames) (!) in input dir (dirpath variable)
    """
    # select only files:
    all_files = os.listdir(dirpath)  # list(explicit_dir.glob('**/*'))
    # now make a map:
    #   file_body -> Map<extension, path>
    #   so you can select faster than iterating over list of tuples
    common_to_formats: Dict[str, Dict[str, str]] = (
        ExplicitFileConstants.get_common_part_to_extension_map(all_files)
    )  # {}
    # for debug:
    # doubled_keys = [key for key in common_to_formats.keys() if len(common_to_formats[key]) > 1]
    # common_to_formats[doubled_keys[0]]
    # now iterate again:
    explicit_files: List[str] = []
    for common_part in common_to_formats.keys():
        c_files: Dict[str, str] = common_to_formats[common_part]
        # since you have 'continue' keyword during dict collecting
        #   you don't have to handle zero length case (even though it's handled via <fp is not None>)
        if len(c_files) == 1:
            # append it using generator rather than iterator
            # https://stackoverflow.com/a/3097896
            explicit_files.append(next(iter(c_files.values())))
        else:
            # now in the following order:
            # first goes parquet, than txt and the last one is bz2
            fp: Optional[str] = None
            for prioritized_ext in ExplicitFileConstants.listing_order:
                # if prioritized_ext in c_files.keys():
                fp = c_files.get(prioritized_ext, None)
                if fp is not None:
                    explicit_files.append(fp)
                    break

            assert fp is not None, f"not initialized fp; check for loops"

    return explicit_files


# def get_explicit_files(device: pd.Series,
#                        main_config: MainConfig,
#                        filters: BirdooUtils.Filter = None,
#                        useRolled: bool = False,
#                        use_binary: Optional[bool] = None
#                        ) -> Tuple[str, List[str]]:
#     """
#     Returns tuple of
#         dirname retrieved from device pd.Series
#         list of unique files (in terms of available different file extensions)
#             as the __basename__ rather than full path
#             so make sure you concatenate strings when accessing paths
#
#     ForwardRunViz_folder
#
#     @param device: device row from device`s table
#     @param main_config: configuration class
#     @param filters: filtration class
#     @param useRolled: flag. If True will be used rolled folder, otherwise explicit folder
#     @param use_binary:  flag. If True will be used binary(explicit/rolled) folder, otherwise raw(explicit/rolled) folder
#     @return: explicit_dir: path, explicit_files_output: filenames
#     """
#
#     if use_binary is not None:
#         warnings.warn(
#             f"get_explicit_files: 'use_binary' is deprecated  parameter: from now you have the following prioritization "
#             f"reading order: {ExplicitFileConstants.listing_order}; remove this parameter from function call; "
#             f"the next commits your function call won't survive")
#
#     explicit_files_output = []
#     if useRolled:
#         activeExplicitFolder = main_config.ForwardRunViz_rolled_folder
#     else:
#         activeExplicitFolder = main_config.ForwardRunViz_folder
#
#     explicit_dir: str = os.path.join(main_config.local_results_dir, device.path, activeExplicitFolder)
#     # explicit_dir = main_config.local_results_dir + "\\" + device.path + "\\" + activeExplicitFolder
#     if not os.path.exists(explicit_dir):
#         logger.info(f"CHECK 'explicit_dir'. PATH {explicit_dir} doesn`t exists")
#         return explicit_dir, explicit_files_output
#
#     explicit_files = list_explicits(dirpath=explicit_dir)
#     for file in explicit_files:
#         if filters is not None:
#             age = get_age_from_explicit_file(file)
#             if not filters.check_age(age):
#                 continue
#         explicit_files_output.append(file)
#
#     return explicit_dir, explicit_files_output
#
#
# def get_explicit_files_completeness(
#         main_config: MainConfig,
#         filters: Optional[BirdooUtils.Filter],
#         useRolled: bool,
#         age_column_name: str = 'age',
#         sess_column_name: str = 'sess',
#         use_binary: Optional[bool] = None
# ) -> pd.DataFrame():
#     """
#     Return results' folder summary of data that is computed with next columns:
#     GlobalConfig.device_match_columns + [ age_column_name, sess_column_name]
#
#     @param main_config: configuration class
#     @param filters: filtration class
#     @param useRolled: flag. If True will be used rolled folder, otherwise explicit folder
#     @param use_binary:  flag. If True will be used binary(explicit/rolled) folder, otherwise raw(explicit/rolled) folder
#     @return: explicit_dir: path, explicit_files_output: filenames
#     """
#
#     if use_binary is not None:
#         warnings.warn(
#             f"get_explicit_files_completeness: 'use_binary' is deprecated  parameter: from now you have the following prioritization "
#             f"reading order: {ExplicitFileConstants.listing_order}; remove this parameter from function call; "
#             f"the next commits your function call won't survive")
#
#     devices = BirdooUtils.load_devices_from_csv(GlobalConfig.device_csv)
#     unique_farms = devices['farm'].unique()
#     farm_folders = [f for f in os.listdir(main_config.local_results_dir) if f in unique_farms]
#     if filters is None:
#         filters = BirdooUtils.Filter()
#
#     filters.farms = list(set(farm_folders).intersection(filters.farms))
#     devices = filters.filter_devices(devices)
#
#     df_output = pd.DataFrame(columns=GlobalConfig.device_match_columns + [age_column_name, sess_column_name])
#     for _, device in devices.iterrows():
#         _, files = get_explicit_files(device, main_config, filters, useRolled=useRolled)
#         if len(files) == 0:
#             continue
#         for f in files:
#             age = get_age_from_explicit_file(f)
#             sess = get_sess_id_from_explicit_file(f)
#             s2add = device[GlobalConfig.device_match_columns]
#             s2add[age_column_name] = age
#             s2add[sess_column_name] = sess
#             df_output.loc[len(df_output)] = s2add
#     return df_output
#
#
# def get_features_df_from_explicits(device: pd.Series,
#                                    main_config: MainConfig,
#                                    filters: BirdooUtils.Filter,
#                                    features: List[str],
#                                    useRolled: bool = True,
#                                    dropFiltered: bool = True):
#     df_output = pd.DataFrame()
#     explicit_dir, explicit_files = get_explicit_files(device, main_config=main_config, filters=filters,
#                                                       useRolled=useRolled)
#     if (len(explicit_files) == 0):
#         # logger.info(f"No explicits  found")
#         return df_output
#     time_diffs: List[float] = []
#     file_sizes: List[int] = []
#     for file in explicit_files:
#         try:
#             logger.info(f"{file}")
#             filepath: str = os.path.join(explicit_dir, file)
#             st = datetime.datetime.now()
#             tmp_df = load_explicit(filepath)
#             time_diffs.append((datetime.datetime.now() - st).total_seconds())
#             file_sizes.append(os.path.getsize(filepath))
#             if dropFiltered and main_config.engine_version > '_v4.0':
#                 tmp_df = tmp_df[tmp_df["Filters"] == 'none']
#
#             if len(features) != 0:
#                 union_columns = list(set(tmp_df.columns).intersection(features))
#             else:
#                 union_columns = tmp_df.columns
#
#             if len(union_columns) == 0:
#                 logger.info("No columns {} in {}".format(features, file))
#                 continue
#
#             tmp_df = filter_by_time(tmp_df, filters)
#             tmp_df = tmp_df[union_columns]
#             df_output = pd.concat([df_output, tmp_df], ignore_index=True)
#         except Exception as e:
#             logger.info(f"Exception {e}")
#             continue
#     logger.info(f"count = {len(explicit_files)}")
#     logger.info(f"mean load_explicit time_diff = {np.round(np.mean(time_diffs), 3)} s")
#     logger.info(f"mean load_explicit file_sizes = {np.round(np.mean(file_sizes) / 1000 / 1000, 3)} Mb")
#     # sys.exit(1)
#     return df_output
#
#
# def get_all_features_df_from_explicits(devices,
#                                        main_config: MainConfig,
#                                        filters: BirdooUtils.Filter,
#                                        useRolled=True, add_device_params=False, dropFiltered=True):
#     df_output = pd.DataFrame()
#     devices_loc = filters.filter_devices(devices)
#     for _, device in devices_loc.iterrows():
#         label = BirdooUtils.generate_id_from_device(device, GlobalConfig.device_match_columns)
#         try:
#             if not filters.check_device(device):
#                 continue
#
#             tmp_df = get_features_df_from_explicits(device,
#                                                     main_config,
#                                                     filters,
#                                                     features=[],
#                                                     useRolled=useRolled,
#                                                     dropFiltered=dropFiltered
#                                                     )
#             if tmp_df.empty:
#                 logger.info("No data for {} ages {}".format(device.id, " ".join(map(str, filters.ages))))
#                 continue
#             if add_device_params:
#                 tmp_df.loc[:, GlobalConfig.device_match_columns] = device[GlobalConfig.device_match_columns].values
#                 for c in GlobalConfig.standards_match_columns:
#                     if c in device.index:
#                         tmp_df[c] = device[c]
#
#             df_output = pd.concat([df_output, tmp_df], ignore_index=True)
#         except Exception as e:
#             logger.info(f"Problems with {label}\n{e}")
#
#     if not df_output.empty:
#         first_col_name = df_output.columns[0]
#         df_output = df_output.loc[df_output[first_col_name] != first_col_name]
#     return df_output


def set_new_columns(df, new_columns, value=-1):
    for new_col in new_columns:
        if new_col not in df.columns:
            df[new_col] = value

    df = df[new_columns]
    return df


def rolled_image_name_to_datetime(image_name: str):
    try:
        return datetime.datetime.strptime(image_name, "%Y-%b-%d %H:%M:%S.%f")
    except:
        return datetime.datetime.strptime(image_name, "%Y-%b-%d %H:%M:%S")

# def remove_doubles(device: pd.Series, main_config: MainConfig, filters: BirdooUtils.Filter):
#     explicit_folder, files = get_explicit_files(device=device,
#                                                 main_config=main_config,
#                                                 filters=filters,
#                                                 useRolled=False)
#     if len(files) == 0:
#         return
#     logger.info("\nDevice {} processing".format(device.id))
#
#     files_by_age = {}
#     for f in files:
#         age = get_age_from_explicit_file(f)
#         if age not in files_by_age:
#             files_by_age[age] = []
#         files_by_age[age].append(f)
#
#     for age in files_by_age:
#         logger.info(f"Checking age {age}")
#         logger.info(f"n files = {len(files_by_age[age])}")
#         if len(files_by_age[age]) == 1:
#             continue
#
#         df_union_explicit = pd.DataFrame()
#         sum_len = 0
#         for f_age in files_by_age[age]:
#             logger.info(f"{f_age} is processing")
#             tmp_explicit = load_explicit(explicit_folder + "\\" + f_age)
#             sum_len += len(tmp_explicit)
#
#             tmp_explicit["Image_basename"] = [os.path.basename(x) for x in tmp_explicit["Image_name"]]
#             tmp_explicit['ts'] = get_datetime_from_Image_name(tmp_explicit)
#
#             if df_union_explicit.empty:
#                 df_union_explicit = tmp_explicit
#                 continue
#             new_data_Image_basename = set(tmp_explicit["Image_basename"]).difference(
#                 set(df_union_explicit["Image_basename"]))
#
#             # USE ONLY NEW TIMESTAMPS
#             tmp_explicit = tmp_explicit[tmp_explicit["Image_basename"].isin(new_data_Image_basename)]
#
#             # CONCAT
#             df_union_explicit = pd.concat([
#                 df_union_explicit, tmp_explicit
#             ])
#
#         # SORT BY TIMESTAMP
#         df_union_explicit = df_union_explicit.sort_values(by='ts')
#         # DROP EXTRA COLUMNS
#         df_union_explicit = df_union_explicit.drop(columns=['ts', "Image_basename"])
#         union_len = len(df_union_explicit)
#         save_f_name = explicit_folder + "\\" + files_by_age[age][np.argmin(list(map(len, files_by_age[age])))]
#         for f_age in files_by_age[age]:
#             os.remove(explicit_folder + "\\" + f_age)
#         save_explicit(df_union_explicit, save_f_name)
#         logger.info(f"sum explicit len = {sum_len}")
#         logger.info(f"union explicit len = {union_len}")
#         logger.info(f"Save fname: {save_f_name}")
