from bdm2.utils.schemas.models.data_structures.columns_struct import ColumnsStruct
from bdm2.utils.schemas.models.data_structures.device_data_struct import HouseColumns


class SLTTimetableColumns(ColumnsStruct):
    def __init__(
            self,
            date: str,
            slt_age: str,
            slt_dt: str,
            harvest_dt: str,
            lifting_dt: str,
            stop_feed_dt: str,
    ):
        self.date = date
        self.slt_age = slt_age

        self.slt_dt = slt_dt
        self.harvest_dt = harvest_dt
        self.lifting_dt = lifting_dt
        self.stop_feed_dt = stop_feed_dt


class PIWFHAColumns(ColumnsStruct):
    def __init__(self, piwfha_dt: str, fasting_start_dt: str):
        self.piwfha_dt = piwfha_dt
        self.fasting_start_dt = fasting_start_dt


class SLTDataColumns(ColumnsStruct):

    def __init__(
            self,
            house_index: HouseColumns,
            slt_timetable: SLTTimetableColumns,
            piwfha_timetable: PIWFHAColumns,
            slt_weight: str,
            piwfha_weight: str,
            fasting_start_weight: str,
            weight_loss: str,
            method: str,
            fasting_time_col: str = "fasting_time",
            comment: str = "comment",
            piwfha_postfix: str = "piwfha_postfix",
    ):
        self.house_index = house_index
        self.slt_timetable = slt_timetable
        self.piwfha_timetable = piwfha_timetable

        self.slt_weight = slt_weight
        self.piwfha_weight = piwfha_weight
        self.piwfha_postfix = piwfha_postfix

        self.fasting_start_weight = fasting_start_weight

        self.weight_loss = weight_loss
        self.method = method
        self.fasting_time_col = fasting_time_col
        self.comment = comment


"""
GLOBAL SLT/PIWFHA data format
"""

SLT_HOUSE_COLUMNS = HouseColumns(
    farm="farm",
    cycle="cycle",
    house="house",
)

SLT_DATA_COLUMNS = SLTDataColumns(
    house_index=HouseColumns(
        farm="farm",
        cycle="cycle",
        house="house",
    ),
    slt_timetable=SLTTimetableColumns(
        date="date",
        slt_age="slt_age",
        slt_dt="slt_dt",
        harvest_dt="harvest_dt",
        lifting_dt="lifting_dt",
        stop_feed_dt="stop_feed_dt",
    ),
    piwfha_timetable=PIWFHAColumns(
        piwfha_dt="piwfha_dt", fasting_start_dt="fasting_start_dt"
    ),
    slt_weight="slt_weight",
    piwfha_weight="piwfha_weight",
    fasting_start_weight="fasting_start_weight",
    weight_loss="weight_loss",
    method="method",
    # TODO: approve changes:
    fasting_time_col="fasting_time",
)
