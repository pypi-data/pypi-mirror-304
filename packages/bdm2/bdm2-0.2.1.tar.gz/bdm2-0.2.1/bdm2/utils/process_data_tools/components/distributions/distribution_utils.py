import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from bdm2.logger import build_logger
from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')
from typing import List, Union

# from bdm2.utils.telegram_bot import birdoo_telebot


class Distribution:
    """
    Data for distribution visualization

    :param label: id if data
    :param data: data values

    """

    def __init__(self, label: str, data: pd.Series):
        self.label: str = label
        self.data: pd.Series = data


class AxesParams:
    """
    Axes params for distribution visualization

    :param label: id of axes
    :param xlabel: xlabel of axes
    :param ylabel: ylabel of axes
    :param grid: if True add grid to axes

    """

    def __init__(
            self,
            label: str = "Axes",
            xlabel: str = "x",
            ylabel: str = "y",
            grid: bool = True,
    ):
        self.label: str = label
        self.xlabel: str = xlabel
        self.ylabel: str = ylabel
        self.grid: bool = grid

        #: list of distribution objects to be vis
        self.distributions: List[Distribution] = []

        #: Axes
        self.axes: Union[plt.Axes, None] = None


def send_fig_to_telegram_chat(fig: plt.Figure, fig_text: str, chat_id: int, ask=True):
    """
    Send image with caption to telegram chat

    :param fig: plt.Figure object be send
    :param fig_text: caption
    :param chat_id: dst telegram chat id
    :param ask: ask to send. If true, before sanding ask for permission
    :return: None
    """
    pass
    # logger = build_logger(Path(__file__), save_log=False)
    # if ask:
    #     # plt.show()
    #     logger.info("Do you want to send plot to telegram? y/n")
    #     answer = input()
    # else:
    #     answer = "y"
    #
    # if answer == "y":
    #     fig.savefig("tmp.jpg")
    #     jpg = open("tmp.jpg", "rb")
    #     # birdoo_telebot.bot.send_photo(chat_id, jpg, caption=fig_text)
    #     jpg.close()
    #     os.remove("tmp.jpg")


def init_fig_and_axes(axes_list: List[AxesParams]) -> plt.Figure:
    """
    Init fig and axes for axes list

    :param axes_list:
    :return: update input axes_list and return Figure
    """
    # plot distributions
    n_axes = len(axes_list)
    fig, ax = plt.subplots(n_axes, figsize=(12, n_axes + n_axes * 3), dpi=100)
    try:
        _ = iter(ax)
    except TypeError as te:
        ax = [ax]

    for i in range(n_axes):
        axes_list[i].axes = ax[i]
    return fig


def plot_hist(axes_list: List[AxesParams], init_axes: bool = False):
    """
    Update all axes attributes in axes_list by drawing distribution. if init_axes=True, will init them from code
    If all axes attributes in axes_list are None, will init them by force

    :param axes_list: list of all axes. Axes will be arranged in vertical line
    :param init_axes: if True, will init them from code
    """
    logger = build_logger(Path(__file__), save_log=False)
    if init_axes:
        logger.info(f"axes are inited in plot_hist")
        _ = init_fig_and_axes(axes_list)

    not_all_none_axes = False
    for _, axes in enumerate(axes_list):
        if axes.axes is not None:
            not_all_none_axes = True
            break
    if not not_all_none_axes:
        logger.info(f"As all axes are None,inited in plot_hist")
        _ = init_fig_and_axes(axes_list)
    n_bins = 50
    try:
        for ax_ind, axes in enumerate(axes_list):
            if len(axes.distributions) == 0:
                continue
            mean_w = np.mean([distrib.data.mean() for distrib in axes.distributions])
            stdev_w = np.max([distrib.data.std() for distrib in axes.distributions])
            if stdev_w <= 0.01:
                stdev_w = 0.01
            if axes.axes is None:
                warnings.warn(
                    f"axes for {axes.label} is None. but init_axes={init_axes}"
                )
            axes.axes.hist(
                [distrib.data for distrib in axes.distributions],
                bins=np.arange(
                    mean_w - 6 * stdev_w, mean_w + 6 * stdev_w, 12 * stdev_w / n_bins
                ),
                label=[distrib.label for distrib in axes.distributions],
            )

            axes.axes.set_title(axes.label)
            axes.axes.set_ylabel(axes.ylabel)
            axes.axes.set_xlabel(axes.xlabel)
            axes.axes.grid(axes.grid)
            axes.axes.legend()

        # return fig, ax
    except Exception as e:
        logger.info(e)
