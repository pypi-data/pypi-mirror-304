import random

import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')

import warnings
from typing import List, Tuple, Any, Union, Optional
from pathlib import Path
from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'plotly.express'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

px = checker.get_module('plotly.express')

# declaring constants:
MODEL_NAME: str = 'model.pt'
WEIGHTS_NAME: str = 'weights.pt'
CFG_DIRNAME: str = 'cfg'
COLUMN_KEYS: List[str] = ['client', 'farm', 'cycle', 'house', 'device']
AGE_COLNAME: str = 'daynum'
PRED_COLNAME: str = 'ae_pred'
TGT_COLNAME: str = 'adjusted_weight'
REL_ERR_COLNAME: str = 'ae_rel_err'
DELTA_RANGE: int = 3


def get_random_colors(num_classes):
    return ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(num_classes)]


def append_x_legend_error(x: int, y: float, error: float,
                          plot_lines: List[Any],
                          plot_texts: List[str], extra_string: str = ''):
    try:
        # color = get_random_colors(1)
        # color=color[0]
        # https://matplotlib.org/stable/api/markers_api.html
        # default was marker='o'
        # about mec: https://www.w3schools.com/python/matplotlib_markers.asp
        curr_l, = plt.plot(x, y, color='yellow', ms=13,
                              mec='r',  # label='Example line',
                              marker='*')  # , mfc='black', mec='black', ms=10)
        plot_lines.append(curr_l)
        plot_texts.append(f"day: {x:.0f}, error: {error:.3f}" + extra_string)
    except Exception as E:
        warnings.warn(f"Got exception {E} trying to add extra plot")


def plot_outliers(label: Union[str, Tuple[str]],
                  curr_tgt: pd.Series,
                  resulted: pd.Series,
                  standard: pd.Series,
                  # tgt: pd.Series,
                  # likely: pd.Series,
                  # manual: pd.Series,
                  mean_err: float,
                  exact_err: float,
                  # errors: pd.Series,
                  day: int,
                  delta_range: int,
                  save_fp: Optional[Union[str, Path]] = None,
                  figsize: Optional[Tuple[int]] = (9, 6),
                  dpi: Optional[int] = 100):
    # both standard and tgt must have indices as
    # ages so use .set_index(age_colname) before using this func
    if not isinstance(day, int):
        warnings.warn(f"Got unknown type for the day param = {day}")
        return None
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    plot_lines = []
    plot_texts = []
    # scatter = ax.scatter(prediction.ages, prediction.pred, s=50,
    #            c=prediction.rel_error, cmap='coolwarm')
    # TODO: consider changing ax.scatter to plt.scatter
    # errors = tgt - standard
    # errors = (inputs - resulted)/standard
    # # curr_l = plt.scatter(tgt.index.values, tgt.values, s=50, marker="h",  # "o"
    # #                         c=errors, cmap='coolwarm')

    curr_l, = plt.plot(curr_tgt.index.values, curr_tgt.values, alpha=0.65, color='magenta')  # cmap='coolwarm')
    # curr_l = plt.scatter(inputs.index.values, inputs.values, alpha=0.65,
    #                         c=errors,
    #                         cmap='coolwarm')
    plot_lines.append(curr_l)
    plot_texts.append(f"current target weight")
    # https://www.tutorialspoint.com/top-label-for-matplotlib-colorbars
    # https://stackoverflow.com/a/67438721
    # clb = plt.colorbar(scatter)
    # clb = plt.colorbar()
    # clb.ax.tick_params(labelsize=8)
    # # or pass fontdict: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.plt.title.html
    # clb.ax.set_title('rel error', fontsize=11, fontweight='normal')  # 'bold')
    # ax.plot(prediction.ages, prediction.true, alpha=0.75)
    # curr_l, = plt.plot(standard.index.values, standard.values, color="deeppink", alpha=0.75)
    # plot_lines.append(curr_l)
    # plot_texts.append("standard")curr_tgt
    errors = (resulted - curr_tgt) / curr_tgt
    curr_l = plt.scatter(resulted.index.values, resulted.values, s=50, marker="h",  # "o"
                            c=errors, cmap='coolwarm')
    clb = plt.colorbar()
    clb.ax.tick_params(labelsize=8)
    # or pass fontdict: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.plt.title.html
    clb.ax.set_title('rel error', fontsize=11, fontweight='normal')  # 'bold')

    # curr_l, = plt.plot(resulted.index.values, resulted.values, color="blue", alpha=0.75)
    plot_lines.append(curr_l)
    plot_texts.append(f"interpolated curve excluding {day} with range = {delta_range}")

    # curr_l = plt.scatter(standard.index.values, standard.values, color="green", s=25, marker='+')
    curr_l, = plt.plot(standard.index.values, standard.values, color="green", alpha=0.75)
    plot_lines.append(curr_l)
    plot_texts.append("adjusted density standard curve * current volume used for interpolation")

    plt.title(label)
    append_x_legend_error(x=day,
                          y=resulted[day].item(),
                          error=exact_err,
                          plot_lines=plot_lines, plot_texts=plot_texts,
                          extra_string=f"; with delta {delta_range} mean err: {mean_err:.3f}")

    l_prop = {'size': 11, 'weight': 'normal', }
    legends = plt.legend(plot_lines, plot_texts,
                            prop=l_prop, fontsize=12, loc=0)
    # for legend in additional_legends:
    plt.gca().add_artist(legends)
    plt.legend(loc="lower right")
    plt.tight_layout()
    if save_fp is None:
        plt.show()
    else:
        plt.close()
        fig_results_fp = save_fp
        fig.savefig(fig_results_fp, dpi=dpi)
        # delete variables:
        del fig, ax


def plot_outliers2(label: Union[str, Tuple[str]],
                   curr_tgt: pd.Series,
                   resulted: pd.Series,
                   standard: pd.Series,
                   mean_err: float,
                   exact_err: float,
                   # errors: pd.Series,
                   day: int,
                   day_src_name: str,
                   delta_range: int,
                   raw_targets: Optional[pd.Series] = None,
                   true_error_region: Optional[pd.Series] = None,
                   filtered_targets: Optional[pd.Series] = None,
                   save_fp: Optional[Union[str, Path]] = None,
                   raw_error: Optional[float] = None,
                   figsize: Optional[Tuple[int]] = (11, 6),
                   dpi: Optional[int] = 100):
    # both standard and tgt must have indices as
    # ages so use .set_index(age_colname) before using this func
    if not isinstance(day, int):
        warnings.warn(f"Got unknown type for the day param = {day}")
        return None
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    plot_lines = []
    plot_texts = []
    # scatter = ax.scatter(prediction.ages, prediction.pred, s=50,
    #            c=prediction.rel_error, cmap='coolwarm')
    # TODO: consider changing ax.scatter to plt.scatter
    # errors = tgt - standard
    # errors = (inputs - resulted)/standard
    # # curr_l = plt.scatter(tgt.index.values, tgt.values, s=50, marker="h",  # "o"
    # #                         c=errors, cmap='coolwarm')

    curr_l, = plt.plot(curr_tgt.index.values, curr_tgt.values, alpha=0.65, color='magenta')  # cmap='coolwarm')
    # curr_l = plt.scatter(inputs.index.values, inputs.values, alpha=0.65,
    #                         c=errors,
    #                         cmap='coolwarm')
    plot_lines.append(curr_l)
    plot_texts.append(f"current target weight")
    # https://www.tutorialspoint.com/top-label-for-matplotlib-colorbars
    # https://stackoverflow.com/a/67438721
    # clb = plt.colorbar(scatter)
    # clb = plt.colorbar()
    # clb.ax.tick_params(labelsize=8)
    # # or pass fontdict: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.plt.title.html
    # clb.ax.set_title('rel error', fontsize=11, fontweight='normal')  # 'bold')
    # ax.plot(prediction.ages, prediction.true, alpha=0.75)
    # curr_l, = plt.plot(standard.index.values, standard.values, color="deeppink", alpha=0.75)
    # plot_lines.append(curr_l)
    # plot_texts.append("standard")curr_tgt
    errors = (resulted - curr_tgt) / curr_tgt
    curr_l = plt.scatter(resulted.index.values, resulted.values, s=50, marker="h",  # "o"
                            c=errors, cmap='coolwarm')
    clb = plt.colorbar()
    clb.ax.tick_params(labelsize=8)
    # or pass fontdict: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.plt.title.html
    clb.ax.set_title('rel error', fontsize=11, fontweight='normal')  # 'bold')

    # curr_l, = plt.plot(resulted.index.values, resulted.values, color="blue", alpha=0.75)
    plot_lines.append(curr_l)
    plot_texts.append(f"interpolated curve excluding {day} with range = {delta_range}")

    # curr_l = plt.scatter(standard.index.values, standard.values, color="green", s=25, marker='+')
    curr_l, = plt.plot(standard.index.values, standard.values, color="green", alpha=0.75, linestyle='--')
    plot_lines.append(curr_l)
    plot_texts.append("adjusted density standard curve * current volume used for interpolation")

    if raw_targets is not None:
        curr_l = plt.scatter(raw_targets.index.values, raw_targets.values, s=50, marker="x",  # "o"
                                c='black')
        plot_lines.append(curr_l)
        plot_texts.append(f"raw targets")
        # indices from error region, values from raw targets (!)
        if true_error_region is not None:
            x = true_error_region.index.values
            y = raw_targets[raw_targets.index.isin(x)].values
            curr_l = plt.scatter(x, y,
                                    s=35,  # s=25,
                                    marker="D",  # "x",  # "o"
                                    # c='olive',
                                    c='red',
                                    #   c='sienna'
                                    )
            plot_lines.append(curr_l)
            if raw_error is None:
                _raw_error = -1
            else:
                _raw_error = raw_error
            plot_texts.append(f"raw targets error region; err = {_raw_error:.2f} within {min(x)} - {max(x)}")

        if filtered_targets is not None:
            curr_l = plt.scatter(filtered_targets.index.values, filtered_targets.values, s=50, marker="x",  # "o"
                                    c='cyan')
            plot_lines.append(curr_l)
            plot_texts.append(f"filtered targets")

    plt.title(label)
    append_x_legend_error(x=day,
                          y=resulted[day].item(),
                          error=exact_err,
                          plot_lines=plot_lines, plot_texts=plot_texts,
                          extra_string=f" src_name = {day_src_name}; with delta {delta_range} mean err: {mean_err:.3f}")

    l_prop = {'size': 11, 'weight': 'normal', }
    legends = plt.legend(plot_lines, plot_texts,
                            prop=l_prop, fontsize=12, loc=0)
    # for legend in additional_legends:
    plt.gca().add_artist(legends)
    # plt.legend(loc="lower right")
    plt.legend(loc="upper left")
    plt.tight_layout()
    if save_fp is None:
        plt.show()
    else:
        plt.close()
        fig_results_fp = save_fp
        fig.savefig(fig_results_fp, dpi=dpi)
        # delete variables:
        del fig, ax


def slider_outliers(save_fp: Union[str, Path],
                    curr_tgt: pd.Series,
                    resulted: pd.Series,
                    standard: pd.Series,
                    show: bool = False):
    pass
