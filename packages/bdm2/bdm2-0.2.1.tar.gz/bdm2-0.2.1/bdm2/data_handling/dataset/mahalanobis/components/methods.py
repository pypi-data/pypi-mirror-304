

import matplotlib.pyplot as plt
import pandas as pd

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.process_data_tools.components.res_df.components.file_manager import FilenameManager


from typing import Dict, List, Tuple, Optional, Iterable

from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.constants.global_setup.group_by import active_group_by_method


def draw_pipes(df: Optional[pd.DataFrame],
               target_colname: str,
               filters_of_zones: Dict[str, Filter],
               filters_of_interest: Dict[str, Filter],
               gby: List[str],
               age_colname: str = "age",
               zone_mode:str = 'std', # minmax, std
               n_stdevs: float = 2,
               fig_size: Tuple[int] = (8, 6),
               dpi: int = 150,
               pipes_alpha=0.1,
               df_zones : Optional[pd.DataFrame] = None,
               df_dots : Optional[pd.DataFrame] = None,
               fig:Optional[plt.Figure] = None,
               ax:Optional[plt.Axes] = None,
               ) -> [plt.Figure, List[plt.Axes]]:
    colors = ['c', 'm', 'y', 'g', 'salmon']
    if (fig is None) or (ax is None):
        fig, ax = plt.subplots(1, figsize=fig_size, dpi=dpi)

    # Drawing pipes
    i = 0
    if df_zones is None:
        if df is None:
            raise ValueError('df or df_zones should be defines as not None')
        df_zones = df
    if (target_colname) not in df_zones.columns:
        raise KeyError(f"No {target_colname} in df_zones.columns.")

    if df_dots is None:
        if df is None:
            raise ValueError('df or df_dots should be defines as not None')
        df_dots = df
    if (target_colname) not in df_dots.columns:
        raise KeyError(f"No {target_colname} in df_dots.columns.")

    filters_of_zones_to_draw = {}
    for i in filters_of_zones:
        filters_of_zones_to_draw[i]=filters_of_zones[i]
    if len(filters_of_zones_to_draw)==0:
        filters_of_zones_to_draw['full'] = Filter()

    for zone_id in filters_of_zones_to_draw:
        # print(f"drawing {zone_id} pipe")
        # Get values of interest
        feature_df_all = filters_of_zones_to_draw[zone_id].filter_res_df_csv(df_zones,age_col=age_colname)

        # Get mean and std by age
        feature_df_stat_by_age = feature_df_all[[target_colname,age_colname ]].groupby(age_colname).agg(['mean', 'std', 'min', 'max'])[target_colname]

        # Draw pipe
        if zone_mode == 'std':
            ax.fill_between(feature_df_stat_by_age.index,
                            feature_df_stat_by_age["mean"] - n_stdevs * feature_df_stat_by_age["std"],
                            feature_df_stat_by_age["mean"] + n_stdevs * feature_df_stat_by_age["std"],
                            alpha=pipes_alpha, color=colors[i % len(colors)],
                            label=f"{zone_id}")
        elif zone_mode == 'minmax':
            ax.fill_between(feature_df_stat_by_age.index,
                            feature_df_stat_by_age["min"],
                            feature_df_stat_by_age["max"],
                            alpha=pipes_alpha, color=colors[i % len(colors)],
                            label=f"{zone_id}")
        i += 1

    # Get values of interest
    # print(f"Collecting data for scatter plots")
    if len(filters_of_interest)==0:
        feature_df_of_interest = df_dots.copy()
    else:
        feature_df_of_interest = df_dots.iloc[:0].copy()
        for filter_id in filters_of_interest:
            print(f"adding {filter_id} data")
            feature_df_of_interest = feature_df_of_interest.append(
                filters_of_interest[filter_id].filter_res_df_csv(df_dots, age_col=age_colname),
                ignore_index=True)

    # feature_df_of_interest = feature_df_of_interest.drop_duplicates(
    #     subset=gby + [age_colname])

    # Draw values of interest
    for label, group in feature_df_of_interest.groupby(gby,sort=False):

        if isinstance(label, str):
            label_str = label
        elif not isinstance(label, Iterable):
            label_str = str(label)
        else:
            label_str = "_".join(list(map(str,label)))

        ax.scatter(group[age_colname], group[target_colname], label=label_str, s=5)

    ax.set_title("{}".format(target_colname))
    ax.legend()
    ax.grid(True)
    ax.set_ylabel(target_colname)
    ax.set_xlabel(age_colname)

    fig.tight_layout()
    return fig, ax


if __name__ == '__main__':

    gby = ['farm', 'house']
    n_stdevs = 2

    """
    ==============================================
    Define engine
    """

    main_config = EngineConfig()
    postfix = "_v4.10.7.23_CGTHBG_Arbor-Acres_female_2812_final"
    results_postfix = "_restore"
    main_config.set_another_engine_version(postfix, results_postfix)

    client = main_config.define_client(postfix)
    """
    ==============================================
    Define feature_component
    """
    # src_feature = 'mass_corr'
    # src_feature = "day_average_density"
    src_feature = "filters_of_zones_to_draw"

    # target_colname = "mass_corr_mean"
    # target_colname = "adjusted_weight"
    # target_colname = "mass_corr_mean"
    target_colname= "volume_norm_corr_mean"
    #
    group_by_v = active_group_by_method

    csv_res_df_fname = main_config.local_results_dir + "\\" + FilenameManager.get_res_fname(src_feature, postfix,
                                                                                            f"_{group_by_v}")
    feature_df = pd.read_csv(csv_res_df_fname, sep=";")

    """
    ==============================================
    Define filter
    """
    # data sets for drawing pipes
    filters_of_zones = {}

    filter_of_zones = Filter()
    filter_of_zones.farms = ['BTG']
    filters_of_zones['history'] = filter_of_zones


    # data sets for drawing dots
    filters_of_interest = {}

    filter_of_interest = Filter()
    filter_of_interest.farms = ['BF1']
    filter_of_interest.cycles = ["Cycle 1"]
    filters_of_interest['BF1'] = filter_of_interest

    filter_of_interest = Filter()
    filter_of_interest.farms = ['BF2']
    filter_of_interest.cycles = ["Cycle 1"]
    filters_of_interest['BF2'] = filter_of_interest

    filter_of_interest = Filter()
    filter_of_interest.farms = ['BF7']
    filter_of_interest.cycles = ["Cycle 1"]
    filters_of_interest['BF7'] = filter_of_interest

    fig, ax = draw_pipes(df=feature_df,
                         target_colname=target_colname,
                         filters_of_zones=filters_of_zones,
                         filters_of_interest=filters_of_interest,
                         gby=gby,
                         age_colname='age',
                         n_stdevs=n_stdevs,
                         pipes_alpha=0.3)

    if 'err' in target_colname:
        ax.axhline(0)
    plt.show()
