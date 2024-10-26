import datetime
import dataclasses
import warnings
from typing import List, Optional, Dict
import numpy as np

__all__ = ['PiwfhaMethodData', 'HarvestData', 'CycleHarvestData', 'WeightSrcInfo',
           'AggregationFeatures']


@dataclasses.dataclass
class PiwfhaMethodData:
    calc_method_id: int
    calc_method_name: str
    calc_method_description: str


# @dataclasses.dataclass
# class PiwfhaAggregationMethodData:
#     aggregation_method_id: int
#     aggregation_method_name: str
#     # used_standard: Optional[Dict[int, float]] = None
#     # adjusted_dg: Optional[Dict[int, float]]


@dataclasses.dataclass
class AggregationFeatures:
    # Aggregation params
    mode: str
    max_age_diff_influence: Optional[int]
    aggregation_strategy: Optional[Dict]

    # standard weight curve, used for projection during aggregation
    # format: {0: 0.042, 1: 0.072, 2: 1.10, ...}
    standard: Optional[Dict[int, float]]
    # adjusted daily dain for each age to combine
    # format: {
    #   35: {0: 0.0, 1: 0.033, 2: 0.053, ...},
    #   42: {0: 0.0, 1: 0.03, 2: 0.05, ...},
    #   }
    adjusted_dg: Optional[Dict[int, Dict[int, float]]]

    # def to_json(self):
    #     _output = {}
    #     for key, value in vars(self):


@dataclasses.dataclass
class HarvestData:
    """
    Data structure for harvest day features
    """
    # slt data
    slt_id: int  # id in slt_timetable
    harvest_age: int
    harvest_date: datetime.date
    slt_weight: float

    slt_dt: Optional[datetime.datetime]
    lifting_dt: Optional[datetime.datetime]
    stop_feed_dt: Optional[datetime.datetime]
    harvest_dt: Optional[datetime.datetime]

    birds_count: Optional[int]

    slt_comment: str
    slt_updated: datetime.datetime  # no need to redefine, will be updated automatically

    # piwfha data
    piwfha_id: Optional[int] = None
    piwfha_weight: Optional[float] = None

    piwfha_method_id: Optional[int] = None
    piwfha_agg_features: Optional[AggregationFeatures] = None

    piwfha_weight_src_id: Optional[int] = None
    piwfha_weight_postfix: Optional[str] = None

    piwfha_dt: Optional[datetime.datetime] = None
    fasting_start_dt: Optional[datetime.datetime] = None
    fasting_start_weight: Optional[float] = None

    piwfha_comment: Optional[str] = None
    piwfha_updated: Optional[datetime.datetime] = None  # no need to redefine, will be updated automatically

    def __post_init__(self):
        if type(self.harvest_date) == str:
            self.harvest_date = datetime.date.fromisoformat(self.harvest_date)
        if type(self.slt_dt) == str:
            self.slt_dt = datetime.datetime.fromisoformat(self.slt_dt)
        if type(self.stop_feed_dt) == str:
            self.stop_feed_dt = datetime.datetime.fromisoformat(self.stop_feed_dt)
        if type(self.lifting_dt) == str:
            self.lifting_dt = datetime.datetime.fromisoformat(self.lifting_dt)
        if type(self.harvest_dt) == str:
            self.harvest_dt = datetime.datetime.fromisoformat(self.harvest_dt)
        if type(self.piwfha_dt) == str:
            self.piwfha_dt = datetime.datetime.fromisoformat(self.piwfha_dt)
        if type(self.fasting_start_dt) == str:
            self.fasting_start_dt = datetime.datetime.fromisoformat(self.fasting_start_dt)

        if type(self.piwfha_updated) == str:
            self.piwfha_updated = datetime.datetime.fromisoformat(self.piwfha_updated)
        if type(self.slt_updated) == str:
            self.slt_updated = datetime.datetime.fromisoformat(self.slt_updated)

    @property
    def fasting_period(self) -> float:
        if self.fasting_start_dt is None:
            warnings.warn("Could not define fasting_period as fasting_start_dt is None")
            return np.nan
        if self.slt_dt is None:
            warnings.warn("Could not define fasting_period as slt_dt is None")
            return np.nan
        _period = np.round((self.slt_dt - self.fasting_start_dt).total_seconds() / 60 / 60, 1)
        if _period < 0:
            warnings.warn("Unavailable value: fasting_period < 0")
        # assert _period > 0, "Unavailable value: fasting_period < 0"
        return _period

    @property
    def fasting_start_to_piwfha_period(self) -> float:
        if self.fasting_start_dt is None:
            warnings.warn("Could not define fasting_start_to_piwfha_period as fasting_start_dt is None")
            return np.nan

        # assert self.fasting_start_dt is not None, "Could not define fasting2piwfha as fasting_start_dt is None"
        # assert self.piwfha_dt is not None, "Could not define fasting2piwfha as piwfha_dt is None"
        _period = np.round((self.piwfha_dt - self.fasting_start_dt).total_seconds() / 60 / 60, 1)
        return _period

    @property
    def weight_loss(self) -> float:

        if self.slt_weight is None:
            warnings.warn("Could not define weight_loss as slt_weight is None")
            return np.nan
        if self.fasting_start_weight is None:
            warnings.warn("Could not define weight_loss as fasting_start_weight is None")
            return np.nan

        return (self.fasting_start_weight - self.slt_weight) / self.fasting_start_weight

    def reset_piwfha_weight_data(self):
        """
        # Reset piwfha weight fields
        :return:
        """
        for key, value in vars(self).items():
            if key.startswith('piwfha') or key.startswith('fasting_start'):
                self.__setattr__(key, None)


@dataclasses.dataclass
class CycleHarvestData:
    """
    API response
    """
    cycle_house_code: str
    client_name: str
    farm_name: str
    house_name: str
    breed_type: str
    cycle_house_name: str
    gender: str
    cycle_start_date: datetime.date
    harvest_data: List[HarvestData]


@dataclasses.dataclass
class WeightSrcInfo:
    piwfha_union_src_id: int
    piwfha_union_src_postfix: str
    piwfha_individual_src_id: int
    piwfha_individual_src_postfix: str
    targets_src_id: int
    targets_src_postfix: str
    likely_targets_src_id: int
    likely_targets_src_postfix: str
