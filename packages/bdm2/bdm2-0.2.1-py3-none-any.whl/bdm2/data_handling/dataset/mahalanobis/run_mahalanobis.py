import pandas as pd

from bdm2.data_handling.dataset.mahalanobis.components.check import MahalanobisCheck
from bdm2.data_handling.dataset.mahalanobis.components.params import MahalanobisParameter
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


class Param(MahalanobisParameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':

    df_fp = r"\\Datasets\chikens\MHDR_Chicken\sources\datasets\zbage_datasets" \
            r"\union_training_combinations_actual_20241003_union_full\collected_df.csv"

    df = pd.read_csv(df_fp, sep=';')

    f_interests = Filter(
        farms=["BF2"],
        cycles=["Cycle 3"],
        ages=[i for i in range(20, 61, 1)]
    )

    f_to_compare = Filter(
        farms=["BF2"],
        cycles=["Cycle 2"],
        ages=[i for i in range(20, 61, 1)]

    )

    params = Param(
        df_of_interest=df,
        df_to_compare_with=df,
        filters_of_interest=f_interests,
        filters_to_compare_with=f_to_compare,

    )
    params.features_set = {
        "geom": ['volume_norm_corr_mean', 'max_axis_norm_corr_mean'],
        "rel": ['volume_norm_corr_mean', 'reliability'],
        "vol_h": ['volume_norm_corr_mean', 'height_mean']
    }

    mahal_check = MahalanobisCheck(params=params,
                                   save_images=False,
                                   save_excel=False)
    res_dict = mahal_check.run()
