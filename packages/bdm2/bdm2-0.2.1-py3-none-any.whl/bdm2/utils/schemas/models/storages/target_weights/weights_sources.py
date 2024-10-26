#  Copyright (c) Anna Sosnovskaya

WEIGHTS_SRC_TYPE = {
    "DOC": "DOC",
    "Farmers": "Farmers",
    "SLT": "SLT",
    "PIWFHA": "PIWFHA",
    "Targets": "Targets",
    "Likely_targets": "Likely_targets",
    # old
    "Likely": "Likely",
    "Manuals": "Manuals",
    "Mahender": "Mahender",
}
"""
Available weights sources names. For more information check :ref:`WeightsSources`
"""


class WrongWeightsSourceType(Exception):
    """
    Occurred when weight source type is not available (not in WEIGHTS_SRC_TYPE.values)

    """

    pass


class ActualPostfixError(Exception):
    """
    Occurred when can not define actual weight postfix

    """

    pass
