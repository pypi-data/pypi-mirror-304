import datetime
import os

import numpy as np
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from scipy.stats import chi2

from bdm2.constants.global_setup.data import house_match_columns, device_match_columns
from bdm2.constants.global_setup.group_by import active_group_by_method, group_by_house_reliability
from bdm2.data_handling.dataset.mahalanobis.components.distance_check import match_device_info, \
    calculateMahalanobis
from bdm2.data_handling.dataset.mahalanobis.components.methods import draw_pipes
from bdm2.data_handling.dataset.mahalanobis.components.params import MahalanobisParameter
from bdm2.data_handling.generated_data.checks.interpolation_outliers_search.components.common import colorstr
from bdm2.utils.process_data_tools.components.collecting.explicit import means_by


class MahalanobisCheck:
    allowed_indexing = {
        'by_house': house_match_columns,
        'by_device': device_match_columns
    }

    def __init__(self,
                 params: MahalanobisParameter,
                 save_images: bool,
                 save_excel: bool,
                 save_all: bool = False,
                 ):
        self.params: MahalanobisParameter = params
        self.logger = self.params.logger
        self.save_all = save_all
        self.save_images = save_images
        self.save_excel = save_excel

    @property
    def global_index_cols(self):
        assert self.params.indexing_type in \
               self.allowed_indexing.keys(), \
            'indexing_type is not in INDEXING_TYPE space. ' \
            f'Possible values: {list(self.allowed_indexing.keys())}'
        return self.allowed_indexing[self.params.indexing_type]

    @property
    def group_by_v(self):
        return active_group_by_method

    def prepare_data(self, df, filter):
        df.rename(columns={'age': self.params.age_column}).reset_index()
        df = filter.filter_res_df_csv(df,
                                      age_col=self.params.age_column)

        if self.params.indexing_type == 'by_house':
            df = means_by(df,
                          self.global_index_cols + [self.params.age_column],
                          group_by_house_reliability)

            df = df.drop(columns=['device'])
        df = match_device_info(df,
                               match_columns=self.global_index_cols)

        return df

    @property
    def dst_dir(self):
        return str(Path("mahalanobis_output") / f"{datetime.datetime.now().strftime('%d%m_%H-%M')}")

    @property
    def fig_folder(self):

        return str(Path(self.dst_dir) / "figs")

    def run(self):
        results_dict = {}
        self.logger.info("prepare df of interests")
        self.params.df_of_interest = self.prepare_data(df=self.params.df_of_interest,
                                                       filter=self.params.filters_of_interest)

        self.logger.info("prepare df to compare with")
        self.params.df_to_compare_with = self.prepare_data(df=self.params.df_to_compare_with,
                                                           filter=self.params.filters_to_compare_with)

        # filter res_df_historical according to filter_df_base_fname
        # if filter_df_base_fname is not None:
        #     if os.path.exists(filter_df_base_fname):
        #         print(colorstr('blue', f'Filter res_df by external df ({filter_df_base_fname})'))
        #         filter_df_base = pd.read_csv(filter_df_base_fname, sep=';')
        #         filter_df_base = filter_df_base.groupby(global_index_cols).first().reset_index()
        #         initial_len = len(df_to_compare_with)
        #         df = pd.merge(filter_df_base[global_index_cols], df_to_compare_with,
        #                       on=global_index_cols, how='left')
        #         df = df.dropna(subset=[age_colum])
        #         filtered_df_len = len(df)
        #         print(f"after dataset filtration only {filtered_df_len}/{initial_len} remains")

        res_df_historical_by_age = self.params.df_to_compare_with.groupby(
            self.params.age_column)  # df_to_compare_with['daynum'].unique()
        res_df_target_by_age = self.params.df_of_interest.groupby(
            self.params.age_column)  # df_of_interest['daynum'].unique()

        print(colorstr('blue', f"{'':-^70}"))
        self.logger.info(f'Calculating Mahalanobis by Age')
        output_df = self.params.df_of_interest.iloc[:0]
        for age in np.sort(self.params.df_of_interest[self.params.age_column].unique()):
            # define target points to estimate
            res_df_age = res_df_target_by_age.get_group(age).copy()
            # define historical data with age range +-2
            res_df_historical_age = pd.concat([res_df_historical_by_age.get_group(age1)
                                               for age1 in
                                               range(age - self.params.age_window_size // 2, age +
                                                     self.params.age_window_size // 2 + 1)
                                               if age1 in res_df_historical_by_age.indices], ignore_index=True)
            if len(res_df_historical_age) == 0:
                print()
                continue

            for set_label in self.params.features_set:
                # calc Mahalanobis
                res_df_age[f'{set_label}_mahal'] = calculateMahalanobis(
                    data=res_df_historical_age[self.params.features_set[set_label]].dropna(
                        subset=self.params.features_set[set_label],
                        how='any'),
                    y=res_df_age[self.params.features_set[set_label]])

                # if vis:
                # visualize_distancies(y=res_df_historical_age[self.params.features_set[set_label]],
                #                      data_to_check=res_df_age[self.params.features_set[set_label]],
                #                      title=f'age {age}',
                #                      n_steps_per_feature=10,
                #                      x_feature=self.params.features_set[set_label][0],
                #                      y_feature=self.params.features_set[set_label][1]
                #                      )

            output_df = pd.concat([output_df, res_df_age], ignore_index=True)

        if self.save_excel:
            if not os.path.exists(self.dst_dir):
                os.makedirs(self.dst_dir)
        if self.save_images:
            if not os.path.exists(self.fig_folder):
                os.makedirs(self.fig_folder)
        output_df = output_df.sort_values(by=self.global_index_cols)
        # calculate p-value for whole target data
        print(colorstr('blue', f' NOT Saving results'))
        save_fname = os.path.join(self.dst_dir, f'results.xlsx')
        if self.save_excel:
            writer = pd.ExcelWriter(save_fname, engine='openpyxl')
        index_columns = self.global_index_cols + [self.params.age_column]
        state_cols = []

        for set_label in self.params.features_set:

            m_col = f'{set_label}_mahal'
            p_col = f'{set_label}_p'
            state_col = f'{set_label}_state'
            state_cols.append(state_col)

            p_val_degree = len(self.params.features_set[set_label]) - 1

            output_df[p_col] = 1 - chi2.cdf(output_df[m_col], p_val_degree)

            output_df[state_col] = True
            if self.params.p_th is not None:
                output_df[state_col] = (output_df[state_col] * (output_df[p_col] > self.params.p_th)) | (
                    output_df[p_col].isna())
            if self.params.m_th is not None:
                output_df[state_col] = (output_df[state_col] * (output_df[m_col] < self.params.m_th)) | (
                    output_df[p_col].isna())

            df_to_save = output_df[index_columns + self.params.features_set[set_label] + [m_col, p_col, state_col]]
            df_to_save = df_to_save.rename(columns={m_col: 'mahal', p_col: 'p', state_col: 'state'})

            if self.save_excel:
                df_to_save.to_excel(writer, f"{set_label}_full", index=False)
                df_to_save[~df_to_save['state']].to_excel(writer, f"{set_label} bad cases", index=False)

            results_dict.setdefault(f"{set_label}_full", df_to_save)
            results_dict.setdefault(f"{set_label} bad cases", df_to_save[~df_to_save['state']])

        output_df['union_state'] = (output_df[state_cols]).all(axis=1)
        if self.save_excel:
            output_df.to_excel(writer, f"full", index=False)
            output_df[~output_df['union_state']].to_excel(writer, f"bad cases", index=False)
            writer.close()
            print(f'REPORT WAS SAVED')
            print(f'{save_fname}')

        results_dict.setdefault(f"full", output_df)
        results_dict.setdefault(f"bad cases", output_df[~output_df['union_state']])

        # finding all suspicious cases
        print(colorstr('blue', f'Finding suspicious cases'))
        iter_cases = output_df.set_index(self.global_index_cols).index.unique()

        bad_cases = output_df[~output_df['union_state']].set_index(self.global_index_cols).index.unique()
        print(f'Suspicious cases count = {len(bad_cases)}')

        # Visualizing and saving plots for bad cases
        print(colorstr('blue', f'Saving plots for suspicious cases'))
        output_df_by_device = output_df.groupby(self.global_index_cols)
        for case in iter_cases:

            device_group = output_df_by_device.get_group(case).copy()
            # check if there are cases where on interval of 5 days number of bad cases is more than 3
            if any(~device_group['union_state']):
                print(colorstr('red', f"{case} has {len(device_group[~device_group['union_state']])} bad datapoints"))
                is_real_bad = any((~device_group['union_state']).rolling(7).sum() > 3)
                if not is_real_bad:
                    print(colorstr('blue', f"{case} has bad datapoints, but they are not stable"))
                    if not self.save_all:
                        continue
            # if not need to save all, continue
            elif not self.save_all:
                continue
            # if bad and approved that it is bad, or save all, save
            y_count = max([len(self.params.features_set[label]) for label in self.params.features_set])
            x_count = len(self.params.features_set)
            fig, ax = plt.subplots(y_count, x_count, squeeze=False,
                                   figsize=(x_count * 4, y_count * 4))

            for x, set_label in enumerate(self.params.features_set):
                features_set_state_col = f'{set_label}_state'
                device_group['class'] = device_group[features_set_state_col].apply(
                    lambda x: "ok" if x else 'bad')
                device_group = device_group.sort_values('class', ascending=False)

                for y, feature in enumerate(self.params.features_set[set_label]):
                    target_colname = feature

                    draw_pipes(df=None,
                               df_zones=self.params.df_to_compare_with,  # [density_train_df_filtered[age_colum]<30],
                               df_dots=device_group,
                               target_colname=target_colname,
                               filters_of_zones={},
                               filters_of_interest={},
                               gby=['class'],
                               age_colname=self.params.age_column,
                               zone_mode=self.params.zone_mode,
                               n_stdevs=self.params.m_th,
                               pipes_alpha=0.3,
                               fig=fig,
                               ax=ax[y, x])
            if self.save_images:
                fig_fname = os.path.join(self.fig_folder, "_".join(case) + '.png')
                plt.suptitle("_".join(case))
                plt.tight_layout()
                plt.savefig(fig_fname)
                plt.close()

        return results_dict
