import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'plotly.express',
    'plotly.graph_objects',
    'plotly.io',
    'plotly.subplots'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

px = checker.get_module('plotly.express')
go = checker.get_module('plotly.graph_objects')
pio = checker.get_module('plotly.io')
make_subplots = checker.get_module('plotly.subplots')


def generate_plots4features_groups_and_diff_sources(group_by: dict,
                                                    feature_groups: dict,
                                                    dataset: pd.DataFrame,
                                                    output_file: str,
                                                    source_1: str,
                                                    source_2: str):
    """
    Create interactive plots for feature groups showing the difference between two datasets.

    This function is suitable for visualizing statistics for groups of features between two labeled sources,
    such as differences in calculations between two engines or systems.

    It performs the following steps:
    1. Aggregates the input dataset by calculating the mean for each group specified.
    2. Creates a plot with subplots for each feature group.
    3. Iterates through the provided feature groups to plot the differences.

    The differences between two datasets (source_1 and source_2) are calculated as the absolute
    difference in percentage, and both the minimum and maximum differences for each day are plotted.

    Parameters:
    -----------
    group_by : dict
        A dictionary specifying the columns to group by. The keys are the column names and the values
        are the data types.
    feature_groups : dict
        A dictionary where keys are the feature group names and values are lists of feature names.
        Example:
        {
            'behavioral': ['activity_score_mean', 'sitting_score_mean'],
            'geometric': ['max_axis_norm_corr_mean', 'min_axis_norm_corr_mean'],
            ...
        }
    dataset : pd.DataFrame
        The input dataset containing the features and groups. It should include at least the columns
        specified in `group_by` and 'daynum', along with columns for the source labels ('source_1' and 'source_2').
    output_file : str
        The path to the output HTML file where the plot will be saved.
    source_1 : str
        The label for the first data source to be compared.
    source_2 : str
        The label for the second data source to be compared.

    Returns:
    --------
    None
        The function saves the generated plot as an HTML file and does not return any value.

    Example usage:
    --------------
    group_by = {'dataset_type': 'str'}
    feature_groups = {
        'behavioral': ['activity_score_mean', 'sitting_score_mean', 'surr_score_mean', 'height_mean'],
        'geometric': ['max_axis_norm_corr_mean', 'min_axis_norm_corr_mean', 'volume_norm_corr_mean'],
        'reliability': ['common_reliability_mean', 'tilt_reliability_mean', 'missing_reliability_mean'],
        'density': ['day_average_density_mean']
    }

    create_plots(group_by=group_by, feature_groups=feature_groups, dataset=union_df, output_file='abs_diff_feature_percent_groups.html', source_1='click_df', source_2='pc_df')
    """
    grouped_data = dataset.groupby(list(group_by.keys()) + ['daynum']).mean().reset_index()
    fig = make_subplots(rows=1, cols=1, subplot_titles=["Difference for Feature Groups"], shared_xaxes=True)

    # Define color palette
    color_palette = px.colors.qualitative.Plotly
    color_mapping = {group: color_palette[i % len(color_palette)] for i, group in enumerate(feature_groups)}

    print("Max diff value between datasets by feature group:")

    daily_diff = None
    for group_name, features in feature_groups.items():
        all_diffs = []
        for feature in features:
            # Separate subgroups for source_1 and source_2
            source_1_df = grouped_data[grouped_data['dataset_type'] == source_1]
            source_2_df = grouped_data[grouped_data['dataset_type'] == source_2]

            # Check if subgroups are not empty
            if source_1_df.empty or source_2_df.empty:
                print(f"Skipping feature {feature} because one of the groups is empty.")
                continue

            # Merge by date for calculating the difference
            merged = pd.merge(source_1_df, source_2_df, on='daynum', suffixes=(f'_{source_1}', f'_{source_2}'))

            # Calculate the difference
            merged['difference'] = abs((merged[f'{feature}_{source_1}'] / merged[f'{feature}_{source_2}']) - 1)

            # Group by day and calculate the max difference
            daily_diff = merged.groupby('daynum')['difference'].max().reset_index()
            daily_diff['difference'] = round(daily_diff['difference'], 2)
            all_diffs.append(daily_diff['difference'])

            print(feature, 'max =', round(abs(merged['difference'].values.max()), 2))

        # Calculate the minimum and maximum difference for each day
        all_diffs_df = pd.concat(all_diffs, axis=1)
        min_diff = all_diffs_df.min(axis=1)
        max_diff = all_diffs_df.max(axis=1)
        daynum = daily_diff['daynum']

        # Add scatter plot
        fig.add_trace(
            go.Scatter(
                x=daynum,
                y=min_diff,
                mode='lines',
                name=f"{group_name} min",
                line=dict(color=color_mapping[group_name], dash='dot'),
                showlegend=True
            )
        )
        fig.add_trace(
            go.Scatter(
                x=daynum,
                y=max_diff,
                mode='lines',
                name=f"{group_name} max",
                fill='tonexty',
                line=dict(color=color_mapping[group_name]),
                showlegend=True
            )
        )

    # Update plot layout
    fig.update_layout(
        width=1000,
        height=800,  # Fixed height
        hoverlabel_namelength=-1,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        legend=dict(x=1.05, y=1, title='Legend'),  # Legend position and title
        title_text="Difference for Feature Groups"
    )

    # Save plot to HTML file
    pio.write_html(fig, file=output_file, auto_open=True)


# Example usage
group_by = {'dataset_type': 'str'}
feature_groups = {
    'behavioral': ['activity_score_mean', 'sitting_score_mean', 'surr_score_mean', 'height_mean'],
    'geometric': ['max_axis_norm_corr_mean', 'min_axis_norm_corr_mean', 'volume_norm_corr_mean'],
    'reliability': ['common_reliability_mean', 'tilt_reliability_mean', 'missing_reliability_mean'],
    'density': ['day_average_density_mean']
}

# Replace 'union_df' with your DataFrame with data
union_df = pd.DataFrame()
generate_plots4features_groups_and_diff_sources(group_by=group_by, feature_groups=feature_groups, dataset=union_df,
                                                output_file='abs_diff_feature_percent_groups.html', source_1='click_df',
                                                source_2='pc_df')
