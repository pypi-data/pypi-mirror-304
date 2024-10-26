import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'plotly.graph_objects',
    'matplotlib.pyplot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

go = checker.get_module('plotly.graph_objects')
plt = checker.get_module('matplotlib.pyplot')


def create_plot4feature(feature: str,
                        target_df: pd.DataFrame,
                        group_by_level: list,
                        plot_title: str):
    """
    Create an interactive scatter plot for a specific feature grouped by given levels.

    This function generates an interactive scatter plot using Plotly for the specified feature,
    grouping the data by the provided levels. Additionally, it creates a static scatter plot using Matplotlib.
    The interactive plot is displayed and saved as an HTML file.

    Parameters:
    -----------
    feature : str
        The name of the feature/column to plot from the DataFrame.
    target_df : pd.DataFrame
        The DataFrame containing the data to be plotted.
    group_by_level : list
        A list of column names by which to group the data before plotting.
    plot_title : str
        The title of the plot.

    Returns:
    --------
    None
        The function displays the interactive plot, saves it as an HTML file,
        and creates a static scatter plot.

    Example usage:
    --------------
    create_plot4feature(
        feature='error',
        target_df=your_dataframe,
        group_by_level=['client'],
        plot_title='Error Scatter Plot by Client'
    )
    """
    slider_fig = []

    for label, subgroup in target_df.groupby(group_by_level):
        if isinstance(label, str):
            label_str = label
        else:
            label_str = "_".join(list(map(str, label)))
        slider_fig.append(go.Scatter(x=subgroup['daynum'], y=subgroup[feature], mode='markers', name=label_str))
        fig = go.Figure(slider_fig)

        fig.update_layout(
            title=plot_title,
            width=1000,
            height=800,
            hoverlabel_namelength=-1,
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )

        plt.scatter(x=subgroup['daynum'], y=subgroup[feature], label=label_str)
    fig.show()
    fig.write_html(r'D:\LOCAL_GARBAGE\2105 AA male\.html')

df = pd.read_csv(r'\\Datasets\chikens\MHDR_Chicken\sources\datasets\zbage_datasets\union_training_combinations_actual_20240904_union_full\collected_df.csv',
                 sep=';')
# Example usage
create_plot4feature(feature='error', target_df=pd.DataFrame(), group_by_level=['client'], plot_title='some plot')
