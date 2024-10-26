from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'plotly.colors'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

pcolors = checker.get_module('plotly.colors')

def generate_colors(labels):
    """

    @type labels: object
    """
    unique_labels = sorted(set(labels))
    colors = pcolors.qualitative.Plotly
    color_mapping = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels)}
    return color_mapping
