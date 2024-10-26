import os
from typing import Dict, Tuple

import pandas as pd
from loguru import logger


def load_weights_from_csv(filename: str, index_col: str = "age") -> pd.DataFrame:
    """
    Return weighs pd.DataFrame. (sep= ,;)
    :param filename: full path to weights file
    :param index_col: name of index ('age' by default)
    :return: pd.DataFrame
    """
    num_of_cols: Tuple[int, ...] = (2, 3)
    output_columns = [index_col, "Weights", "std"]
    if os.path.exists(filename):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            df = pd.read_csv(
                filename, sep="[ ,;]", index_col=None, header=None, engine="python"
            )
            df = df.dropna(axis="columns", how="all")
            df = df.dropna(axis="index", how="any")
            if len(df.columns) not in num_of_cols:  # != 2:
                logger.info(
                    "Wrong number of columns in  {}; ".format(filename)
                    + f"{len(df.columns)} not in {num_of_cols}"
                )
                df = pd.DataFrame(columns=output_columns)
            else:
                df.columns = output_columns[: len(df.columns)]
        else:
            df = pd.read_excel(filename, index_col=0)
        df = df.set_index(index_col)
        return df

    logger.info("!!! Weights file {} does not exist".format(filename))
    return pd.DataFrame()


def save_weights_to_csv(standard: pd.Series, fname: str):
    df_to_save = standard.to_frame()
    df_to_save.to_csv(fname, sep=";", header=False)


def load_statistics_from_csv(filename: str) -> pd.DataFrame:
    """
    Return weighs pd.DataFrame. (sep= ,;)
    :param filename: full path to statistics
    :return: pd.DataFrame
    """
    if os.path.exists(filename):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            df = pd.read_csv(filename, sep="[ ,;]", index_col=0, engine="python")
        else:
            # according to docs for 1.2.0 version:
            #   https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
            #
            try:
                df = pd.read_excel(filename, engine=None, index_col=0)
            except Exception as E:
                error_msg: str = (
                        f"Caught exception {E} during opening file {filename}. It may be related "
                        + f"to either selected engine, corrupted file or excel-opening related problem "
                        + f"(see, for example, https://stackoverflow.com/a/68478217 ). Raising error"
                )
                logger.error(error_msg)
                raise E

        return df
    logger.error("!!! Statistics file {} does not exist".format(filename))
    return pd.DataFrame()


def load_density_from_csv(filename) -> pd.DataFrame:
    """
    Return density pd.DataFrame. (sep= ,;)
    :param filename: full path to density file
    :return: pd.DataFrame
    """
    if os.path.exists(filename):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            df = pd.read_csv(filename, sep="[ ,;]", index_col=0, engine="python")
        else:
            df = pd.read_excel(filename, index_col=0)
        # if len()
        return df
    logger.error("!!! Density file {} does not exist".format(filename))
    return pd.DataFrame()


def load_ideal_cv_curve_from_csv(filename) -> pd.DataFrame:
    """
    Return density pd.DataFrame. (sep= ,;)
    :param filename: full path to density file
    :return: pd.DataFrame
    """
    if os.path.exists(filename):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            df = pd.read_csv(filename, sep="[ ,;]", index_col=0, engine="python")

        else:
            df = pd.read_excel(filename, index_col=0)
        cols = [col for col in df.columns if "Unnamed" not in col]
        return df[cols]

    logger.error("!!! Ideal CV curve file {} does not exist".format(filename))
    return pd.DataFrame()


def load_density_corr_coefs_from_csv(filename) -> pd.DataFrame:
    """
    Return density pd.DataFrame. (sep= ,;)
    :param filename: full path to density file
    :return: pd.DataFrame
    """
    if os.path.exists(filename):
        if filename.endswith(".csv") or filename.endswith(".txt"):
            df = pd.read_csv(filename, sep=";", index_col=0)
        else:
            df = pd.read_excel(filename, index_col=0)
        cols = [col for col in df.columns if "Unnamed" not in col]
        return df[cols]

    logger.error("!!! Ideal CV curve file {} does not exist".format(filename))
    return pd.DataFrame()


def build_config_dict(df: pd.DataFrame) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Build the configuration dictionary from the DataFrame.

    :param df: DataFrame containing client information
    :return: Configuration dictionary
    """
    config_dict = {}
    for _, row in df.iterrows():
        client_id = row["client"]
        config_dict[
            f"{client_id}_{row['gender']}_{row['breed_type'].replace(' ', '_')}"
        ] = {
            "client_settings": {
                "client_name": client_id,
                "gender": row["gender"],
                "breed_type": row["breed_type"],
                "engine_postfix": row["engine_config_name"],
                "results_postfix": row["results_postfix"],
            },
            "filter_settings": {
                "clients": [client_id],
                "breed_types": [row["breed_type"]],
                "genders": [row["gender"]],
            },
        }
    return config_dict
