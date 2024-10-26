import warnings
from typing import Dict

import pandas as pd

from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.device_data_struct import HouseColumns

WEIGHTS_UNITS: Dict[str, str] = {"kg": "kg", "g": "g"}


class WeightColumns(ColumnsStruct):
    def __init__(self, age: str, weight: str, confidence: str):
        self.age = age
        self.weight = weight
        self.confidence = confidence

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        df_output = df.copy()
        if self.age in df.columns:
            df_output[self.age] = df_output[self.age].astype(int)
        if self.weight in df.columns:
            df_output[self.weight] = df_output[self.weight].astype(float)
        if self.confidence in df.columns:
            df_output[self.confidence] = df_output[self.confidence].astype(float)
        return df_output


class WeightSrcColumns(ColumnsStruct):
    def __init__(self, src_name: str, postfix: str):
        self.src_name = src_name
        self.postfix = postfix

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        df_output = df.copy()
        # Works not good if nans
        # if self.src_name in df.columns:
        #     df_output[self.src_name] = df_output[self.src_name].astype(str)
        # if self.postfix in df.columns:
        #     df_output[self.postfix] = df_output[self.postfix].astype(str)
        return df_output


class TargetWeightsColumns(ColumnsStruct):
    def __init__(
            self,
            house_index: HouseColumns,
            weight: WeightColumns,
            weight_src: WeightSrcColumns,
    ):
        self.house_index: HouseColumns = house_index
        self.weight: WeightColumns = weight
        self.weight_src: WeightSrcColumns = weight_src

    def convert_df_types(self, df: pd.DataFrame) -> pd.DataFrame:
        # TODO: review changes
        df_output = df.copy()
        df_output = self.house_index.convert_df_types(df_output)
        # ---- df_output.loc[df_output['weight'].isnull(), ['weight']] = None ---- don't work
        weights_to_convert = df_output[~df_output[self.weight.weight].isnull()]
        if not len(weights_to_convert) == len(df_output):
            warning_message = (
                f"\nYou have NaN values in your dataframe. Removing them...\n"
            )
            warnings.warn(message=warning_message, category=UserWarning)
            # if weights_to_convert.empty:
            #     raise AssertionError(f"Look at your data: it doesn't contain non-null weights values at all")
        df_output = self.weight.convert_df_types(weights_to_convert)
        df_output = self.weight_src.convert_df_types(df_output)
        return df_output


TARGET_WEIGHTS_COLUMNS = TargetWeightsColumns(
    house_index=HouseColumns(
        farm="farm",
        cycle="cycle",
        house="house",
    ),
    weight=WeightColumns(
        age="age",
        weight="weight",
        confidence="confidence",
    ),
    weight_src=WeightSrcColumns(src_name="src_name", postfix="weights_postfix"),
)

# import copy
# a = TargetWeightsColumns(**copy.deepcopy(TARGET_WEIGHTS_COLUMNS.__dict__))
# a.weight_src.postfix = 'a'
#
# b = TargetWeightsColumns(**copy.deepcopy(TARGET_WEIGHTS_COLUMNS.__dict__))
# b.weight_src.postfix = 'b'
#
# logger.info(f"a: {a.weight_src.postfix}")
# logger.info(f"b: {b.weight_src.postfix}")
