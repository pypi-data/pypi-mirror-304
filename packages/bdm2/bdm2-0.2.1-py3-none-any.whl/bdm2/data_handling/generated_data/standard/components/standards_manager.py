import warnings
from typing import List, Optional

from bdm2.utils.process_data_tools.utils import (
    load_ideal_cv_curve_from_csv,
    load_weights_from_csv,
    load_statistics_from_csv,
    load_density_from_csv,
)


import pandas as pd

from bdm2.constants.global_setup import server_paths
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import PostgresActualClientsInfoStorage

standard_weight_predictor_file_path = (
        server_paths.standards_dir + "standard_weight_model.pkl"
)

_ACTUAL_INFO_STORAGE = PostgresActualClientsInfoStorage()


def get_actual_weights_postfix(src_type, client: str) -> str:
    return _ACTUAL_INFO_STORAGE.get_actual_weights_postfix(
        src_type, client=client, breed_type=None, gender=None
    )


def get_actual_target_weights_postfix(client: str) -> Optional[str]:
    return _ACTUAL_INFO_STORAGE.get_actual_target_weights_postfix(
        client=client, breed_type=None, gender=None
    )


def get_actual_PIWFHA_weights_postfix(client) -> str:
    return _ACTUAL_INFO_STORAGE.get_actual_piwfha_weights_postfix(
        client=client, breed_type=None, gender=None
    )


def get_actual_engine(client: str, breed_type: str, gender: str) -> (str, str):
    """
    Get actual engine name and results postfix from actual_engines info.

    :param client: client name used for getting actual info
    :param breed_type: breed_type name used for getting actual info
    :param gender: gender name used for getting actual info
    :return:
    """

    return _ACTUAL_INFO_STORAGE.get_actual_engine(
        client=client, breed_type=breed_type, gender=gender
    )


def get_actual_statistics(
        client: str, breed_type: str, gender: str
) -> (str, pd.DataFrame):
    """
    Get actual features statistics info from actual_engines info.

    TODO: replace with storage
    :param client: client name used for getting actual standard
    :param breed_type: breed_type name used for getting actual standard
    :param gender: gender name used for getting actual standard
    :return: src fname and standards values

    :raises KeyError: if standard for specified client, breed, gender not found in actual_engines_info file
    :raises FileExistsError: if standard was specified in actual_engines_info file but not found in file system
    """
    fname = _ACTUAL_INFO_STORAGE.get_actual_statistics_fname(
        client=client, breed_type=breed_type, gender=gender
    )
    standard = _ACTUAL_INFO_STORAGE.get_32actual_statistics(
        client=client, breed_type=breed_type, gender=gender
    )
    return fname, standard


def get_actual_standard_weights(
        client: str, breed_type: str, gender: str
) -> (str, pd.DataFrame):
    """
    Get actual standards weights info from actual_engines info.

    TODO: replace with storage
    :param client: client name used for getting actual standard
    :param breed_type: breed_type name used for getting actual standard
    :param gender: gender name used for getting actual standard
    :return: src fname and standards values

    :raises KeyError: if standard for specified client, breed, gender not found in actual_engines_info file
    :raises FileExistsError: if standard was specified in actual_engines_info file but not found in file system
    """
    fname = _ACTUAL_INFO_STORAGE.get_actual_weights_standard_fname(
        client=client, breed_type=breed_type, gender=gender
    )
    standard = _ACTUAL_INFO_STORAGE.get_actual_weights_standard(
        client=client, breed_type=breed_type, gender=gender
    )
    return fname, standard


def get_standard_weights(
        client: str, breed_type: Optional[str] = None, gender: Optional[str] = None
) -> (str, pd.DataFrame):
    """
    TODO: replace with storage
    Get standard weights fname and load standard for specified client, breed, gender from actual engine info file.
    If breed and gender are None, use DEPRECATED approach -> return standard for specified in function farm values.
    If farm is not specified in function, return standard for Thailand

    Output data is pd.Dataframe with column 'Weights' and ages as index

    :param client: client name used for getting actual standard
    :param breed_type: breed_type name used for getting actual standard
    :param gender: gender name used for getting actual standard
    :return: src fname and standards values
    """

    no_actual_standard_weights = False
    if breed_type is not None and gender is not None:
        try:
            fname, weights = get_actual_standard_weights(client, breed_type, gender)
            if fname is not None:
                return fname, weights
            no_actual_standard_weights = True
            # raise Exception("NOT WORK NOW")
            # standard_weights_fname = ""
            # df =  get_actual_standard_weights(client, breed_type, gender)
            # return get_actual_standard_weights(client, breed_type, gender)
        except KeyError as ke:
            no_actual_standard_weights = True
            warnings.warn(str(ke))
        except FileExistsError as fee:
            no_actual_standard_weights = True
            warnings.warn(str(fee))
        except Exception:
            # TODO:remove
            pass
    if not no_actual_standard_weights:
        warnings.warn(
            f"Used DEPRECATED APPROACH for getting standard_weights, use client, breed_type, gender as inputs."
        )

    # TODO: deprecate
    if client == "Japan":
        standard_weights_fname = (
                server_paths.standards_dir + r"\Japan\ROSS_Standard_Japan_Mix.csv"
        )
    elif client == "Thailand" or client == "KXTHCP":
        standard_weights_fname = (
                server_paths.standards_dir + r"\Thailand\CP_ROSS_std_Weight.csv"
        )
    elif client == "Cargill-NG":
        standard_weights_fname = (
                server_paths.standards_dir + r"\Cargill-NG\Cargill-NG_ROSS_Standard.csv"
        )
    elif client == "BTG" or client == "CGTHBG":
        standard_weights_fname = server_paths.standards_dir + r"\BTG\BTG_AA_std.csv"
    elif client == "BRF" or client == "CGBRBF":
        standard_weights_fname = (
                server_paths.standards_dir + r"\BRF\BRF_ROSS_std_fem_adjusted.csv"
        )
    elif client == "KXPHPSM" or client == "TDPHSM":
        standard_weights_fname = (
                server_paths.standards_dir + r"\KXPHPSM\KXPHPSM_ROSS_std_mix_adjusted.csv"
        )
    elif client == "KXPHP1" or client == "CGBRSA":
        standard_weights_fname = (
                server_paths.standards_dir + r"\KXPHPSM\KXPHPSM_ROSS_std_mix_adjusted.csv"
        )
    elif client == "CGTHCM":
        standard_weights_fname = (
                server_paths.standards_dir + r"\Thailand\CP_ROSS_std_Weight.csv"
        )
    elif client == "SSA-274" or client == "CGBRSA":
        standard_weights_fname = r"\\datasets\chikens\MHDR_Chicken\sources\ManualWeights\SSA-274\Adjusted_full_new_2\standards\CGBRSA_standard.csv"
    elif client == "TDIDWD":
        standard_weights_fname = (
                server_paths.standards_dir + r"\TDIDWD\TDIDWD_Lohmann_std_mix.csv"
        )
    else:
        standard_weights_fname = (
                server_paths.standards_dir + r"\Thailand\CP_ROSS_std_Weight.csv"
        )
        print(
            f"No standard for {client}. Will be used default:\n{standard_weights_fname}"
        )

    return standard_weights_fname, load_weights_from_csv(standard_weights_fname)


def get_statistics(
        client, breed_type: Optional[str] = None, gender: Optional[str] = None
) -> (str, pd.DataFrame):
    no_actual_statistics = False
    if breed_type is not None and gender is not None:
        try:
            fname, weights = get_actual_statistics(client, breed_type, gender)
            if fname is not None:
                return fname, weights
            no_actual_statistics = True
        except KeyError as ke:
            no_actual_statistics = True
            warnings.warn(str(ke))
        except FileExistsError as fee:
            no_actual_statistics = True
            warnings.warn(str(fee))
        except Exception:
            # TODO:remove
            pass
    if not no_actual_statistics:
        warnings.warn(
            f"Used DEPRECATED APPROACH for getting statistics, use client, breed_type, gender as inputs."
        )

    if client == "Japan":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Japan\Statistics_Japan_Volume_norm_only.csv"
    elif client == "Thailand" or client == "KXTHCP":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Thailand\Thailand_Generated_Statistics_for_2stdev.csv"
    elif client == "Cargill-NG":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Cargill-NG\Cargill-NG_Generated_Statistics.csv"
    elif client == "BRF" or client == "CGBRBF":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\BRF\BRF_Generated_Statistics_female.csv"
    elif client == "BTG" or client == "CGTHBG":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\BTG\BTG_manual_Statistics_male.csv"
    elif client == "KXPHPSM" or client == "TDPHSM":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\KXPHPSM\KXPHPSM_Generated_Statistics_1102.csv"
    # TODO: UPDATE
    elif client == "KXPHP1" or client == "CGTHBG":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Cargill-NG\Cargill-NG_Generated_Statistics.csv"
    # TODO: UPDATE
    elif client == "CGTHCM" or client == "CGTHCM":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Cargill-NG\Cargill-NG_Generated_Statistics.csv"
    # TODO: UPDATE
    elif client == "SSA-274" or client == "CGBRSA":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Standards\Cargill-NG\Cargill-NG_Generated_Statistics.csv"
    elif client == "C-Vale" or client == "CGBRCV":
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Statistics\C-Vale\mix_ROSS_C1\C-Vale_Generated_Statistics.csv"
    else:  # default
        statistics_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Statistics\C-Vale\mix_ROSS_C1\C-Vale_Generated_Statistics.csv"

    return statistics_fname, load_statistics_from_csv(statistics_fname)


def get_last_actual_density(client):
    density_fname = ""

    if client == "Japan":
        density_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Densities_Japan\adjusted_density_Japan_0507_manual.csv"
    elif client == "Thailand":
        density_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Densities_Thailand\adjusted_density_Thailand_2907_manual.csv"
    elif client == "Cargill-NG":
        density_fname = r"\\datasets\chikens\MHDR_Chicken\sources\Densities_Cargill-NG\density_model_opt_Cargill-NG_3007.csv"
    else:
        print(f"No density for {client}")

    return density_fname, load_density_from_csv(density_fname)


def get_ideal_cv_curve(client):
    ideal_cv_fname = ""

    if client == "Japan":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_mix.csv"
    elif client == "Thailand":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif client == "Cargill-NG":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_mix.csv"
    elif client == "BTG":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif client == "BRF":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif client == "KXPHP1":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_mix.csv"
    elif client == "KXPHPSM":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif client == "CGTHCM":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif client == "SSA-274":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_mix.csv"
    else:
        print(f"No ideal_cv for {client}")

    return ideal_cv_fname, load_ideal_cv_curve_from_csv(ideal_cv_fname)


def get_ideal_cv_curve_for_gender(gender):
    ideal_cv_fname = ""
    if gender == "male":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif gender == "female":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_male.csv"
    elif gender == "mix":
        ideal_cv_fname = server_paths.ideal_cv_dir + r"\ideal_cv_curve_mix.csv"
    else:
        print(f"No ideal_cv for {gender}")

    return ideal_cv_fname, load_ideal_cv_curve_from_csv(ideal_cv_fname)


def load_standard_weight_model():
    import pickle

    # Load from file
    with open(standard_weight_predictor_file_path, "rb") as file:
        pickle_model = pickle.load(file)

    return pickle_model


"""
Matching Utils
"""


def match_standard_df(
        df: pd.DataFrame, match_df: pd.DataFrame, by: List[str], match_cols: List[str]
):
    if any([(x not in match_df.columns) for x in match_cols]):
        print("Not all match columns are in match_df")
        print("Required columns: {}".format(match_cols))
        return df
    if any([(x not in df.columns) for x in by]):
        print("Not all required columns are in df")
        print("Required columns: {}".format(by))
        return df
    if any([(x not in match_df.columns) for x in by]):
        print("Not all required columns are in match_df")
        print("Required columns: {}".format(by))
        return df

    for col in match_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    match_df = match_df[by + match_cols]

    df = pd.merge(df, match_df, how="left", on=list(by))
    return df


def match_standard_weights(
        client: str,
        df: pd.DataFrame,
        new_col_name: str = "standard_weight",
        age_col_name: str = "age",
) -> [pd.DataFrame, str]:
    standard_fname, standard = get_standard_weights(client)
    if standard is None or standard.empty:
        print(f"{standard_fname} is not exist")
        return df, ""

    standard = standard.reset_index()
    standard.columns = [age_col_name, new_col_name]

    df = match_standard_df(df, standard, by=[age_col_name], match_cols=[new_col_name])
    return df, new_col_name


def match_ideal_cv(
        client: str,
        df: pd.DataFrame,
        new_col_name: str = "ideal_cv",
        age_col_name: str = "age",
) -> [pd.DataFrame, str]:
    cv_fname, cv = get_ideal_cv_curve(client)
    if cv is None:
        print(f"{cv_fname} is not exist")
        return df, ""

    cv = cv.reset_index()
    cv.columns = [age_col_name, new_col_name]

    df = match_standard_df(df, cv, by=[age_col_name], match_cols=[new_col_name])
    return df, new_col_name


def match_statistics(
        client: str, df: pd.DataFrame, features: List[str], age_col_name: str = "age"
) -> [pd.DataFrame, str]:
    stat_fname, stat = get_statistics(client)
    if stat is None:
        print(f"{stat_fname} is not exist")
        return df, ""
    cols = list(stat.columns)
    stat = stat.reset_index()
    stat.columns = [age_col_name] + cols
    possible_features = [f + "_mean" for f in features if f + "_mean" in stat.columns]

    df = match_standard_df(df, stat, by=[age_col_name], match_cols=possible_features)
    return df, stat
