import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import numpy as np
import pandas as pd
from brddb.utils.common import colorstr
from tqdm import tqdm

from bdm2.constants.global_setup.data import standards_match_columns, house_match_columns
from bdm2.data_handling.generated_data.checks.interpolation_outliers_search.components.calculations import (
    get_current_error,
)
from bdm2.data_handling.generated_data.checks.interpolation_outliers_search.components.target_weights import \
    get_target_key_days
from bdm2.utils.dependency_checker import DependencyChecker
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.sqlhelpers.get_info import PostgreClients
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.sqlalchemy_target_weights_storage import \
    PostgresAlchemyTargetWeightsStorage

required_modules = [
    'plotly.graph_objects'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

go = checker.get_module('plotly.graph_objects')
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)  # UserWarning


@dataclass
class ColumnNames:
    error_colname: str = 'error'
    error_column_postfix: str = 'error'
    is_outlier_colname: str = 'is_outlier'
    closest_day_colname: str = 'closest_day'
    resulted_key: str = 'resulted'
    mean_err_key: str = 'mean_err'
    range_key: str = 'range'
    abs_mean_err_key: str = 'abs_mean_err'
    avg_density_colname: str = 'avg_density'
    tgt_colname: str = 'target'
    input_colname: str = 'input'


class RunConfig:
    threshold: float = 0.05
    age_colname: str = "daynum"
    tgt_colname: str = "adjusted_weight"
    raw_tgt_colname: str = "raw_adjusted_weight"
    input_colname: str = "volume_norm_corr_mean"
    avg_density_colname: str = "avg_density"
    outlier_day_colname: str = "outlier_day"
    client_colname: str = "client"
    closest_day_colname: str = "closest_day"
    rel_diff_colname: str = "rel_diff"
    outputs_foldername: str = "tmp_outputs"
    resulted_key: str = "resulted"
    range_key: str = "intersection_indices"
    abs_mean_err_key: str = "abs_mean_rel_err"
    mean_err_key: str = "mean_err"
    average: int = 2
    smooth_window: int = 1
    key_days: List[int] = [7, 14, 21, 28, 35, 42]
    which_reliability: Optional[str] = "reliability"
    reading_kwargs: Dict[str, Any] = dict(sep=None, engine='python'),
    is_plot: bool = True
    plotly: bool = True
    gby_dataset: List[str] = ['farm', 'cycle', 'house']
    gby_density: List[str] = ['client', 'breed_type', 'gender']
    extended_gby: List[str] = ['farm', 'cycle', 'house', 'daynum']
    is_standard_rolling: bool = True
    standard_rolling_window: int = 5
    is_extended_averaging: bool = True
    results_dir: Path = Path(__file__).parent
    useFirstStandardValue: bool = True
    useLastStandardValue: bool = False
    min_day: int = 7
    max_day: int = 42
    delta_range: int = 1
    verbose: int = 2
    storage: str = "postgre"
    filters: Filter = Filter()
    use_filters: bool = True
    weights_units: str = "kg"
    save_individual_days: bool = False


class InterpolationOutliersSearcher:
    def __init__(self, need_to_save_res: bool):
        self.need_to_save_res = need_to_save_res
        self.config = RunConfig()
        self.columns = ColumnNames()
        self.gby_to_attr: Dict[str, str] = dict(farm='farms', cycle='cycles', house='houses')
        device_storage = PostgresDevicesStorage()
        self.storage = PostgresAlchemyTargetWeightsStorage(
            device_storage=device_storage,
            units=WEIGHTS_UNITS[self.config.weights_units]
        )
        self.outliers = []
        self.ok = []
        self.output_df = pd.DataFrame()
        self.front_out_dict = {}

    def prepare_plot_directory(self):
        if self.config.results_dir is None:
            self.config.results_dir = Path(__file__).parents[0]

        if self.config.is_plot:
            plots_foldername = Path(f"outlier_plots_threshold={self.config.threshold}")
            plots_folderpath = self.config.results_dir / plots_foldername
            if not plots_folderpath.exists():
                plots_folderpath.mkdir()
            return plots_folderpath
        return None

    def filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.config.use_filters:
            postgre_clients = PostgreClients()
            farm_info = postgre_clients.get_farms(filters=self.config.filters)
            unique_clients = list(set(farm_info['clients_name']))
            if len(self.config.filters.farms) == 1:
                assert len(unique_clients) == 1, f"Multiple clients for one farm: {unique_clients}"
            return self.config.filters.filter_res_df_csv(res_df=df, age_col=self.config.age_colname)
        else:
            return df.copy()

    def process_group(self, group_df: pd.DataFrame, group_name, plots_folderpath: Optional[Path]):
        meaned = self.calculate_means(group_df)
        for subgroup_name, subgroup_df in group_df.groupby(self.config.gby_dataset):
            curr_seq, interpolated = self.get_interpolated_sequence(subgroup_df, meaned)
            self.check_outliers(subgroup_name, subgroup_df, group_df, group_name,
                                curr_seq,
                                interpolated,
                                plots_folderpath)

    def calculate_means(self, group_df: pd.DataFrame) -> pd.DataFrame:
        meaned = group_df.groupby(self.config.age_colname).mean()
        meaned[self.config.avg_density_colname] = meaned[self.config.tgt_colname] / meaned[self.config.input_colname]
        return meaned

    def get_interpolated_sequence(self,
                                  subgroup_df: pd.DataFrame,
                                  meaned: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        subgroup_df = subgroup_df.groupby(
            self.config.extended_gby).mean().reset_index() if self.config.is_extended_averaging else subgroup_df
        curr_seq = subgroup_df.set_index(self.config.age_colname)
        interpolated = curr_seq[self.config.input_colname] * meaned[self.config.avg_density_colname]

        return curr_seq, interpolated.dropna()

    def check_outliers(self, subgroup_name: Tuple[str],
                       subgroup_df, group_df, group_name,
                       curr_seq: pd.DataFrame,
                       interpolated: pd.Series,
                       plots_folderpath: Optional[Path]):

        ind = standards_match_columns + house_match_columns
        tmp_front_df = pd.DataFrame(columns=ind)
        tmp_front_df.set_index(ind, inplace=True)
        if self.config.is_standard_rolling:
            interpolated = self.apply_standard_rolling(interpolated)
            # Call the plotting function here]
            is_outlier: bool = False
            # declaring
            current_key_days: List[int]
            if self.config.use_filters:
                # get it using filters:
                filters_for_key_days = copy.deepcopy(self.config.filters)
                # add for them additional info like
                for value, possible_attr in zip(subgroup_name, self.config.gby_dataset):
                    if possible_attr in self.gby_to_attr.keys():
                        attr_name = self.gby_to_attr[possible_attr]
                        attr = getattr(filters_for_key_days, attr_name, None)
                        if attr is None:
                            continue
                        attr_value = [value]
                        setattr(filters_for_key_days, attr_name, attr_value)

                current_key_days, current_src_names = get_target_key_days(filters=filters_for_key_days,
                                                                          storage=self.storage)
                print(colorstr(f"green", f"initialized key days for given {subgroup_name}: {current_key_days}"))
            else:
                current_key_days = self.config.key_days
                current_src_names: List[str] = ['not_used' for _ in range(len(current_key_days))]

            if len(current_key_days) == 0:
                warn_msg = f"there's no key days for {subgroup_name} " + \
                           f"using storage = {self.config.storage} and {self.config.filters}. Skipping it"
                warnings.warn(colorstr('bright_magenta', warn_msg))
            sliders_fig: List[Any] = []
            sliders_steps: List[Any] = []
            clusters: List[Any] = []
            # for day in intersection:
            sorted_tuples = sorted(zip(current_key_days, current_src_names))
            sorted_key_days, sorted_src_names = zip(*sorted_tuples)

            for day, src_name in zip(sorted_key_days, sorted_src_names):
                # now start to collect some dataframe info:
                curr_info: Dict[str, Any] = {}  #
                # first iterate over the current sequences:
                for gn, gb in zip(subgroup_name, self.config.gby_dataset):
                    curr_info[gb] = gn
                # now iterate over the client's info to fill breed and gender:
                for gn, gb in zip(group_name, self.config.gby_density):
                    curr_info[gb] = gn
                # if client in the keys...
                if self.config.client_colname in subgroup_df.columns:
                    u_clients = list(set(subgroup_df[self.config.client_colname]))
                    if len(u_clients) == 1:
                        curr_info[self.config.client_colname] = u_clients[0]
                    else:
                        warn_msg = f"you either have no defined clients for curr row with {group_name}" \
                                   f" or duplicates; " + \
                                   f"\ngot {u_clients} as the unique clients"
                        warnings.warn(colorstr('yellow', warn_msg))
                # append some additional info:
                curr_info['age'] = day
                curr_info[self.columns.is_outlier_colname] = 0
                curr_tgt = curr_seq[self.config.tgt_colname]
                output_dict = get_current_error(day=day,
                                                curr_seq=curr_seq,
                                                curr_tgt=curr_tgt,
                                                interpolated=interpolated,
                                                smooth_window=self.config.smooth_window,
                                                average=self.config.average,
                                                useFirstStandardValue=self.config.useFirstStandardValue,
                                                useLastStandardValue=self.config.useLastStandardValue,
                                                name=subgroup_name,
                                                key_days=sorted_key_days,
                                                delta_range=self.config.delta_range)

                if output_dict is None:
                    continue
                mean_err = output_dict[self.config.mean_err_key]
                closest_day = output_dict[self.config.closest_day_colname]
                curr_info[self.config.closest_day_colname] = closest_day
                resulted = output_dict[self.config.resulted_key]

                if day != closest_day:
                    warnings.warn(f"closest_day = {closest_day} != key day = {day}")

                # day_error_key: str = f"{day}_{OutliersSearchConstants.error_column_postfix}"
                # day_error_key: str = 'error' # 'age'
                if pd.isnull(mean_err):
                    # print(f"you shouldn't be there at day {day}")
                    curr_info[
                        self.columns.error_colname] = -1

                else:
                    curr_info[self.columns.error_colname] = mean_err

                if abs(mean_err) > self.config.threshold:
                    curr_info[self.columns.is_outlier_colname] = 1

                    # Generating front output dict
                    # curr_day = output_dict['closest_day']
                    if not subgroup_name in self.front_out_dict.keys():
                        self.front_out_dict.setdefault(subgroup_name, {})

                    self.front_out_dict[subgroup_name].setdefault(day, {})
                    self.front_out_dict[subgroup_name][day].setdefault(
                        f"Standard Curve * Current {self.config.input_colname}", output_dict['resulted'].to_dict())
                    self.front_out_dict[subgroup_name][day].setdefault('mean_err', output_dict['mean_err'])
                    self.front_out_dict[subgroup_name][day].setdefault('current_target_adj_weight', curr_tgt)
                    self.front_out_dict[subgroup_name][day].setdefault(f"raw {self.config.input_colname}",
                                                                       curr_seq[self.config.input_colname])

                    print(f"errors = {mean_err:.3f} for day = {closest_day} and range = {self.config.delta_range}")
                    is_outlier = True

                    if self.need_to_save_res:
                        if self.config.is_plot:
                            self.update_sliders_steps(sliders_steps=sliders_steps,
                                                      sliders_fig=sliders_fig,
                                                      curr_tgt=curr_tgt,
                                                      resulted=resulted,
                                                      interpolated=interpolated,
                                                      day=day,
                                                      closest_day=closest_day,
                                                      output_dict=output_dict,
                                                      mean_err=mean_err,
                                                      src_name=src_name,
                                                      curr_seq=curr_seq,
                                                      clusters=clusters,
                                                      )

                self.output_df = pd.concat([self.output_df, pd.DataFrame([curr_info])], axis=0, ignore_index=True)

                # again:
            if self.need_to_save_res:
                if self.config.is_plot:
                    # now save figure:
                    figure_path = str(plots_folderpath / ('_'.join(subgroup_name) + '.html'))
                    self.plot_outlier(figure_path=figure_path,
                                      sliders_fig=sliders_fig,
                                      sliders_steps=sliders_steps,
                                      clusters=clusters,
                                      subgroup_name=subgroup_name,
                                      group_name=group_name)

                    del sliders_fig
                    del sliders_steps

            if is_outlier:
                self.outliers.append(subgroup_name)
            else:
                self.ok.append(subgroup_name)
            # self.plot_outliers(subgroup_name, curr_seq, interpolated, plots_folderpath)

    def apply_standard_rolling(self, interpolated: pd.Series) -> pd.Series:
        min_age_to_interpolate = min(interpolated.index)
        max_age_to_interpolate = max(interpolated.index)
        new_interpolated_indices = np.arange(min_age_to_interpolate, max_age_to_interpolate + 1, 1)
        interpolated = interpolated.reindex(new_interpolated_indices)
        interpolated = interpolated.rolling(window=self.config.standard_rolling_window, min_periods=1).mean()
        nan_indices = interpolated[interpolated.isna()].index
        old_nan_indices = list(set(interpolated.index).intersection(nan_indices))
        interpolated[old_nan_indices] = interpolated[old_nan_indices]
        return interpolated.dropna()

    def update_sliders_steps(self,
                             sliders_steps: List[Any],
                             sliders_fig: List[Any],
                             curr_tgt: pd.Series,
                             resulted: pd.Series,
                             interpolated: pd.Series,
                             day: int,
                             closest_day: int,
                             output_dict: Dict[str, Any],
                             mean_err: float,
                             src_name: str,
                             curr_seq: pd.DataFrame,
                             clusters: List[Any],
                             ):
        sliders_fig.append(go.Scatter(x=curr_tgt.index, y=curr_tgt.values,
                                      line=dict(color='DarkOrange', width=3, dash='dash'),
                                      name=f'Current Target {self.config.tgt_colname}',
                                      marker=dict(size=8, color='DarkOrange')))

        sliders_fig.append(go.Scatter(x=resulted.index, y=resulted.values,
                                      mode='markers',
                                      marker_symbol='circle',
                                      marker=dict(color='RoyalBlue', size=10,
                                                  line=dict(width=2, color='Black')),
                                      name=f'Interpolated Curve Excluding {day} with Range ='
                                           f' {self.config.delta_range}'))

        indices = list(output_dict[self.config.range_key])
        sliders_fig.append(go.Scatter(x=indices, y=resulted.loc[indices].values,
                                      mode='markers',
                                      marker_symbol='x',
                                      marker=dict(color='Crimson', size=12,
                                                  line=dict(width=2, color='Black')),
                                      name=f'Mean Error: {mean_err:.2f}, Day: {day}, Src: {src_name},'
                                           f' Avg Reliability:'
                                           f' {curr_seq.loc[indices, self.config.which_reliability].mean():.3f}'))

        x0 = min(indices) - 1
        x0 = x0 if x0 in resulted.index else x0 + 1
        x1 = max(indices) + 1
        x1 = x1 if x1 in resulted.index else x1 - 1
        y0, y1 = resulted[x0], resulted[x1]
        clusters.append(dict(type='circle', xref='x', yref='y',
                             x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color='Crimson', width=2, dash='dash')))

        if self.config.which_reliability is not None and self.config.which_reliability in curr_seq.columns:
            customdata = curr_seq[self.config.which_reliability]
            customdata = customdata.reindex(interpolated.index)
            customdata = customdata.fillna('N/A')
            # Преобразуем customdata в массив значений для использования в hovertemplate
            customdata_values = customdata.values if customdata is not None else None
            if customdata_values is not None:
                hovertemplate = f"{self.config.which_reliability}: %{{customdata:.3f}}"
            else:
                hovertemplate = None
        else:
            hovertemplate = None

        sliders_fig.append(go.Scatter(x=interpolated.index, y=interpolated.values,
                                      line=dict(color='ForestGreen', width=3),
                                      mode='lines+markers',
                                      marker_symbol='triangle-up',
                                      marker=dict(color='ForestGreen', size=10),
                                      customdata=customdata,
                                      hovertemplate=hovertemplate,
                                      name=f"{self.config.avg_density_colname}"
                                           f" Standard Curve * Current {self.config.input_colname}"))

        sliders_fig.append(go.Scatter(x=curr_seq.index, y=curr_seq[self.config.input_colname].values,
                                      line=dict(color='DimGray', width=2),
                                      mode='lines+markers',
                                      marker_symbol='cross',
                                      marker=dict(color='DimGray', size=8),
                                      visible='legendonly',
                                      name=f"Raw {self.config.input_colname} Values"))

        sliders_steps.append((day, src_name, closest_day))

    def plot_outlier(self, figure_path: str, sliders_fig: List[Any],
                     sliders_steps: List[Tuple[Any]],
                     clusters: List[Any],
                     subgroup_name: Tuple[str],
                     group_name: Tuple[Any],
                     ):
        fig_num: int = 5
        layout_steps: List[Any] = []
        fig = go.Figure(sliders_fig)

        # Настройка кнопок для переключения между шагами
        updatemenus_buttons = [dict(label="None",
                                    method="relayout",
                                    args=["shapes", []])]

        for i, (outlier_day, day_name, closest_day) in enumerate(sliders_steps):
            step = dict(
                method='restyle',
                args=[{'visible': [False] * len(fig.data)},
                      {'title': f"Day: {outlier_day}"}],
                label=f"Day: {outlier_day} [{day_name}]; Closest Day = {closest_day}",
            )
            step['args'][0]['visible'][i * fig_num: (i * fig_num + fig_num)] = [True] * fig_num
            layout_steps.append(step)
            updatemenus_buttons.append(
                dict(label=f"Day: {outlier_day} [{day_name}]; Closest Day = {closest_day}",
                     method="relayout",
                     args=["shapes", [clusters[i]]]))

        sliders = [dict(
            currentvalue={"prefix": "Outlier Day: "},
            steps=layout_steps,
        )]
        updatemenus = [dict(type='buttons',
                            buttons=updatemenus_buttons)]

        # Настройка заголовка
        title = [": ".join([i, j]) for i, j in zip(self.config.gby_dataset, subgroup_name)]
        title = ', '.join(title)
        title += "<br>"
        title += ', '.join([": ".join([i, j]) for i, j in zip(self.config.gby_density, group_name)])

        # Обновляем разметку графика
        fig.update_layout(
            sliders=sliders,
            title=title,
            updatemenus=updatemenus,
            legend=dict(x=0.01, y=0.99, traceorder='reversed', orientation='h'),
            margin=dict(l=0, r=0, t=50, b=0),
        )

        if len(sliders_fig):
            fig.write_html(figure_path)

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df_to_use = self.filter_data(df)
        plots_folderpath = self.prepare_plot_directory()
        pbar = tqdm(df_to_use.groupby(self.config.gby_density), total=len(df_to_use.groupby(self.config.gby_density)))
        for group_name, group_df in pbar:
            self.process_group(group_df, group_name, plots_folderpath)
        # The output dataframe with results could be returned here
        self.output_df['is_standard_rolling'] = self.config.is_standard_rolling
        self.output_df['standard_rolling_window'] = self.config.standard_rolling_window
        self.output_df['delta_range'] = self.config.delta_range
        self.output_df['threshold'] = self.config.threshold

        print(f"output shape: {self.output_df.shape}")

        return self.output_df  # Placeholder for actual implementation


if __name__ == '__main__':
    test_df_fp = r"\\Datasets\chikens\MHDR_Chicken\sources\datasets\zbage_datasets\test_20240820_union_tmp_full\collected_df.csv"
    test_df = pd.read_csv(test_df_fp, sep=';')
    # if need_to_save_res = True - result folder with graphs will be saved
    # in current module folder
    ios = InterpolationOutliersSearcher(need_to_save_res=False)
    out = ios.run(df=test_df)
    print()
