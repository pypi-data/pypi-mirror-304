import re
from typing import Any, Callable


# import pandas as pd


def get_apply_lambda(pattern) -> Callable:
    # return lambda x: re.search(pattern=pattern, string=x).group(0) if re.search(pattern=pattern,
    #                                                                             string=x) is not None else None
    def apply(x: str) -> Any:
        tmp_r = re.search(pattern=pattern, string=x)
        if tmp_r is None:
            return None
        else:
            return tmp_r.group(0)

    return apply
