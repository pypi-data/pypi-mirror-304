class Feature:
    def __init__(self, name, isRolled=False, isFilterable=False):
        self.name = name
        self.isFilterable = isFilterable
        self.isRolled = isRolled


class FeatureColNames:
    def __init__(self, feature):
        self.mean = f"{feature}_mean"
        self.l_std_coef = f"{feature}_lstdev_coef"
        self.r_std_coef = f"{feature}_rstdev_coef"
        self.std = f"{feature}_stdev"
