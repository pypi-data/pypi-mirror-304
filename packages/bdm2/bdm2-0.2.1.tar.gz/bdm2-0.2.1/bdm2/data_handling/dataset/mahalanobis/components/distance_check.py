import itertools
import os.path

from bdm2.constants.global_setup.data import standards_match_columns, device_match_columns, house_match_columns
from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.constants.global_setup.group_by import active_group_by_method
from bdm2.data_handling.dataset.collect_and_prepare_data import CollectAndPrepareData
from bdm2.data_handling.dataset.components.dataset_params import CollectingParams
from bdm2.data_handling.dataset.mahalanobis.components.methods import draw_pipes
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.ClientSettingsManager import ClientSettings
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage


import matplotlib.pyplot as plt
import pandas as pd

from typing import List, Optional

import numpy as np
from scipy.stats import chi2


def calculateMahalanobis(y: pd.DataFrame, data: pd.DataFrame, cov=None):
    y_mu = y - data.mean(axis=0)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    # According to https://en.wikipedia.org/wiki/Multivariate_normal_distribution
    # need to divide by 2 and get sqrt
    return np.sqrt(mahal.diagonal()/2)


def visualize_distancies(y: pd.DataFrame,
                         data_to_check: pd.DataFrame,
                         x_feature: str, y_feature: str, title: str,
                         n_steps_per_feature: int = 30):
    y_stat = y.describe()
    n_stdevs = 1
    y_stat.loc['range'] = (y_stat.loc['max'] - y_stat.loc['min']) + n_stdevs * 2 * y_stat.loc['std']

    data = pd.DataFrame(index=np.arange(n_steps_per_feature))

    feature_arrays = []
    for feature in y_stat.columns:
        feature_stat = y_stat[feature]
        data[feature] = np.arange(feature_stat['min'] - n_stdevs * feature_stat['std'],
                                  feature_stat['max'] + n_stdevs * feature_stat['std'],
                                  feature_stat['range'] / n_steps_per_feature)[:n_steps_per_feature]
        feature_arrays.append(data[feature].values)

    data_mesh = pd.DataFrame(list(map(list, itertools.product(*feature_arrays))), columns=y_stat.columns)
    # y_count = min(len(y), 300)
    data_mesh['m'] = calculateMahalanobis(y=data_mesh, data=y)

    data_mesh_mean = data_mesh.groupby([x_feature, y_feature], as_index=False).mean().round(3)
    data_mesh_pivot = pd.pivot(data_mesh_mean, index=x_feature, columns=y_feature, values='m')
    tgrid, pgrid = np.meshgrid(data_mesh_mean[x_feature], data_mesh_mean[y_feature])

    heat = np.zeros_like(tgrid)
    for i in range(len(tgrid)):
        for j in range(len(pgrid)):
            heat[i, j] = data_mesh_pivot.loc[tgrid[i, j], pgrid[i, j]]
    fig, ax = plt.subplots()
    im = ax.pcolormesh(tgrid, pgrid, heat, cmap='gist_heat_r')  # , vmin=0, vmax=10)
    fig.colorbar(im, ax=ax)
    # im = ax.imshow(data_mesh_pivot)

    ax.scatter(y[x_feature], y[y_feature], label='raw')
    ax.scatter(data_to_check[x_feature], data_to_check[y_feature], label='to_estimate')
    ax.set_xlabel(x_feature)
    ax.set_ylabel(y_feature)
    ax.set_title(title)
    ax.legend()
    plt.suptitle('Mahalanobis distance mesh')
    plt.tight_layout()

    plt.show()


def match_device_info(df: pd.DataFrame, match_columns: List[str]):
    # match_extra_columns
    if not all([c in df.columns for c in match_columns]):
        raise ValueError('match_device_info: not all match_columns are in df')
    devices = PostgresDevicesStorage().get_devices(filters=Filter())
    # devices = BirdooUtils.load_devices_from_csv(GlobalConfig.device_csv)
    devices = devices.groupby(match_columns).first()
    columns = standards_match_columns + match_columns
    cols_to_match = [c for c in columns if c not in df and c in devices]
    df = pd.merge(df, devices[cols_to_match], left_on=match_columns,
                  right_index=True)
    return df


if __name__ == '__main__':

    gby = ['farm', 'house']
    zone_mode = 'std'  # minmax, std
    n_stdevs = 2  # for pipes drawing
    vis = False

    """
    ==============================================
    Define engine of results
    """

    main_config = EngineConfig()
    postfix = "_v4.10.7.23_CGTHBG_Arbor-Acres_female_2812_final"
    results_postfix = "_restore"
    main_config.set_another_engine_version(postfix, results_postfix)

    client = main_config.define_client(postfix)
    breed_type = postfix.split('_')[3].replace('-', ' ')
    gender = postfix.split('_')[4].replace('-', ' ')

    group_by_v = active_group_by_method
    """
    ==============================================
    Define feature_component
    """

    age_colum = 'daynum'

    # to collect
    src_features = [
        'volume_norm_corr',
        'min_axis_norm_corr',
        'max_axis_norm_corr',
        # 'reliability',
        # 'tilt_reliability',
        # 'missing_reliability'
    ]

    features_to_estimate = [c + "_mean" for c in src_features]

    p_val_degree = len(src_features) - 1
    p_th = 0.05

    historical_client_settings = {
        client: ClientSettings(client_name=client,
                               engine_postfix=postfix,
                               results_postfix=results_postfix,
                               gender=gender,
                               breed_type=breed_type,
                               filters=Filter(
                                   farms=['BTG'],
                                   cycles=['Cycle 1']
                               ),
                               manual_weights_postfix=None)
    }

    target_client_settings = {
        client: ClientSettings(client_name=client,
                               engine_postfix=postfix,
                               results_postfix=results_postfix,
                               gender=gender,
                               breed_type=breed_type,
                               filters=Filter(
                                   farms=['BF1', 'BF2']
                               ),
                               manual_weights_postfix=None)
    }

    # init df fname (collect_df or train_df) to specify which data to use as historical. If None, then all found res_df
    #  will be used. USED ONLY FOR HISTORICAL
    filter_df_base_fname: Optional[str] = None

    cparams = CollectingParams(breed_gender_as_int=False,
                               check_not_aggregated=True)
    # coding_params_path = os.path.join(os.path.dirname(os.path.dirname(density_train_fname)),
    #                                   r'module\coding_params.yaml')
    # coding_params = None
    # if os.path.exists(coding_params_path):
    #     with open(coding_params_path, "r") as stream:
    #         coding_params = yaml.safe_load(stream)
    # if coding_params is not None:
    #     for key in coding_params:
    #         decode_params = {v: k for k, v in coding_params[key].items()}
    #         density_train_df[key] = density_train_df[key].apply(lambda x: decode_params[x])
    """
    ==============================================
    Define filter
    """
    # Collect Points of interest
    cp_target = CollectAndPrepareData(client_settings=target_client_settings,
                                      collect_config=cparams,
                                      working_features=src_features,
                                      age_column_name=age_colum,
                                      vis=False
                                      )

    print(src_features)
    res_df_target = cp_target.run().rename(columns={'age': age_colum}).reset_index()
    res_df_target = match_device_info(res_df_target, match_columns=device_match_columns)

    print(src_features)
    cp_historical = CollectAndPrepareData(client_settings=historical_client_settings,
                                          collect_config=cparams,
                                          working_features=src_features,
                                          age_column_name=age_colum,
                                          vis=False
                                          )
    res_df_historical = cp_historical.run().rename(columns={'age': age_colum}).reset_index()
    res_df_historical = match_device_info(res_df_historical, match_columns=device_match_columns)

    # filter_df_base_fname = r""
    if filter_df_base_fname is not None:
        if os.path.exists(filter_df_base_fname):
            filter_df_base = pd.read_csv(filter_df_base_fname, sep=';')
            filter_df_base = filter_df_base.groupby(house_match_columns).first().reset_index()
            initial_len = len(res_df_historical)
            df = pd.merge(filter_df_base[house_match_columns], res_df_historical,
                          on=house_match_columns, how='left')
            df = df.dropna(subset=['age'])
            filtered_df_len = len(df)
            print(f"after dataset filtration only {filtered_df_len}/{initial_len} remains")

    #  ===================== BY AGE ====================================
    res_df_historical_by_age = res_df_historical.groupby(age_colum)
    res_df_target_by_age = res_df_target.groupby(age_colum)

    output_df = res_df_target.iloc[:0]
    for age in np.sort(res_df_target[age_colum].unique()):
        print(age)
        # define target points to estimate
        res_df_age = res_df_target_by_age.get_group(age)
        # define historical data with age range +-2
        res_df_historical_age = pd.concat([res_df_historical_by_age.get_group(age1) for age1 in range(age - 1, age + 2)
                                           if age1 in res_df_historical_by_age.indices], ignore_index=True)
        if len(res_df_historical_age)==0:
            continue

        # calc Mahalanobis
        res_df_age['m'] = calculateMahalanobis(
            data=res_df_historical_age[features_to_estimate],
            y=res_df_age[features_to_estimate])
        output_df = pd.concat([output_df, res_df_age], ignore_index=True)

        if vis:
            visualize_distancies(y=res_df_historical_age[features_to_estimate],
                                 data_to_check=res_df_age[features_to_estimate],
                                 title=f'age {age}',
                                 n_steps_per_feature=10,
                                 x_feature=features_to_estimate[0],
                                 y_feature=features_to_estimate[1]
                                 )

    # calculate p-value for whole target data
    output_df['p'] = 1 - chi2.cdf(output_df['m'], p_val_degree)
    plt.figure()
    plt.scatter(output_df['m'], output_df['p'])
    # output_df['m'].hist()
    plt.show()
    fig2, (ax_m_2, ax_p_2) = plt.subplots(2)
    for label, group in output_df.groupby(gby):
        ax_p_2.scatter(group[age_colum], group['p'], label=str(label), s=3)
        ax_m_2.scatter(group[age_colum], group['m'], label=str(label), s=3)
    ax_p_2.set_title('p-value')
    ax_p_2.set_ylim(0, 1)
    ax_m_2.set_title('Mahalanobis')
    plt.legend()
    # plt.show()

    for target_colname in features_to_estimate:
        # df_to_draw = pd.concat([res_df_filtered, density_train_df_filtered], ignore_index=True)
        fig, ax = draw_pipes(df=None,
                             df_zones=res_df_historical,  # [density_train_df_filtered[age_colum]<30],
                             df_dots=res_df_target,
                             target_colname=target_colname,
                             filters_of_zones={},
                             filters_of_interest={},
                             gby=gby,
                             age_colname=age_colum,
                             zone_mode=zone_mode,
                             n_stdevs=n_stdevs,
                             pipes_alpha=0.3)

        if 'err' in target_colname:
            ax.axhline(0)
        output_df['class'] = output_df['p'] > p_th
        output_df['class'] = output_df['class'].apply(lambda x: "close" if x else 'far')
        fig, ax = draw_pipes(df=None,
                             df_zones=res_df_historical,  # [density_train_df_filtered[age_colum]<30],
                             df_dots=output_df,
                             target_colname=target_colname,
                             filters_of_zones={},
                             filters_of_interest={},
                             gby=['class'],
                             age_colname=age_colum,
                             zone_mode=zone_mode,
                             n_stdevs=n_stdevs,
                             pipes_alpha=0.3)

    plt.show()
