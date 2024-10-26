import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

plt = checker.get_module('matplotlib.pyplot')


def visualize_metrics(metrics_fp: str, additional_info: str):
    """
    Visualize various metrics by creating horizontal bar charts for each metric category.

    This function reads a CSV file containing metric data, processes it to create pivot tables for
    different metric categories, and generates a series of horizontal bar charts to visualize the metrics.
    It also includes additional information as a text annotation on the first subplot.

    Parameters:
    -----------
    metrics_fp : str
        The file path to the CSV file containing the metric data.
    additional_info : str
        Additional information to be displayed on the plot.

    Returns:
    --------
    None
        The function saves the generated plot as an HTML file and does not return any value.

    Example usage:
    --------------
    additional_info = "Additional Info:\n" \
                      "1. metrics on all AA male data \n2. new model - centered on all, lifting based tg \n3. actual model - centered on all, stop feed based tg"

    visualize_metrics(metrics_fp='path_to_metrics.csv', additional_info=additional_info)
    """
    metrics_df = pd.read_csv(metrics_fp, sep=';')
    metrics_df.value = round(metrics_df.value, 3)

    piv = metrics_df.pivot_table(index='metric', columns='exp_name', values='value', aggfunc='mean')

    loc_err_std = piv.loc[piv.index.str.contains('err std')]
    loc_mean_relative_abs_err = piv.loc[piv.index.str.contains('mean relative abs err')]
    loc_mean_relative_err = piv.loc[piv.index.str.contains('mean relative err')]
    loc_count_rate_less_3_5 = piv.loc[piv.index.str.contains('point count rate less then 3.5%')]
    loc_count_rate_less_5 = piv.loc[piv.index.str.contains('point count rate less then 5%')]

    all_metrics = [loc_err_std,
                   loc_mean_relative_abs_err,
                   loc_mean_relative_err,
                   loc_count_rate_less_3_5,
                   loc_count_rate_less_5]

    n_tables = len(all_metrics)
    fig, axes = plt.subplots(n_tables, 1, figsize=(15, 5 * n_tables), sharex=True)

    if n_tables == 1:
        axes = [axes]

    for ax, pivo in zip(axes, all_metrics):
        pivo.plot.barh(ax=ax)
        for container in ax.containers:
            ax.bar_label(container, padding=3)
        ax.set_yticks(range(len(pivo)))
        ax.set_yticklabels(pivo.index, ha='right')
        for label in ax.get_yticklabels():
            label.set_y(label.get_position()[1] + 0.03)
        ax.legend(loc='upper left', bbox_to_anchor=(1.08, 1), borderaxespad=0.)

    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)

    x_pos, y_pos = 1.5, 0.65
    axes[0].text(x_pos, y_pos, additional_info, transform=axes[0].transAxes, ha='right', va='top', fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.5))
    plt.show()


# Example usage
additional_info = "Additional Info:\n" \
                  "1. metrics on all AA male data \n2. new model - centered on all, lifting based tg \n3. actual model - centered on all, stop feed based tg"

visualize_metrics(metrics_fp='path_to_metrics.csv', additional_info=additional_info)
