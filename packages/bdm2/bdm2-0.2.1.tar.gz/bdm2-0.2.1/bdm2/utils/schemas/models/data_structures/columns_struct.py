import copy
from typing import List, Dict

from loguru import logger
from pandas import DataFrame


class ColumnsStruct:
    def copy(self):
        return copy.deepcopy(self)

    def get_columns(self) -> List[str]:
        output_cols = []
        attributes = self.__dict__
        for attr in attributes:
            if isinstance(attributes[attr], str):
                output_cols.append(attributes[attr])
            elif isinstance(attributes[attr], ColumnsStruct):
                output_cols += attributes[attr].get_columns()
            else:
                logger.warning(
                    f"!! Warning !! Wrong format for attribute {attr}. Could be only str or ColumnsStruct"
                )
        return output_cols

    def convert_df_types(self, df: DataFrame) -> DataFrame:
        return df.copy()


def get_rename_dict(src: ColumnsStruct, target: ColumnsStruct) -> Dict[str, str]:
    """
    Generate rename dict for 2 instances of the same ColumnsStruct objects
    .. note::
        src type can be a child on target type

    :param src:
    :param target:
    :return:
    """

    assert isinstance(src, type(target)) or isinstance(target, type(src)), ValueError(
        f"from_columns and from_columns has to have the same baser class"
    )

    rename_dict = {}
    attributes_1 = src.__dict__
    attributes_2 = target.__dict__
    for attr in attributes_1:
        if attr in attributes_2:
            if isinstance(attributes_1[attr], str):
                rename_dict[attributes_1[attr]] = attributes_2[attr]
            elif isinstance(attributes_1[attr], ColumnsStruct):
                rename_dict.update(
                    get_rename_dict(attributes_1[attr], attributes_2[attr])
                )
            else:
                logger.info(
                    f"!! Warning !! Wrong format for attribute {attr}. Could be only str or ColumnsStruct"
                )

    return rename_dict
