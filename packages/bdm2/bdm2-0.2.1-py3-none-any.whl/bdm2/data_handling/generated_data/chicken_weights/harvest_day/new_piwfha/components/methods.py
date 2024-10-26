import dataclasses
import datetime
from typing import List, Optional, Dict

import numpy as np
import pandas as pd



__all__ = ['PiwfhaMethod', 'ChPiwfhaMethodsData', 'PIWFHA_METHODS',
           'PiwfhaMethodA', 'PiwfhaMethodB', 'PiwfhaMethodC', 'PiwfhaMethodD',
           'PiwfhaMethodMahender1', 'PiwfhaMethodMahender2', 'PiwfhaMethodMahender3']

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import PiwfhaMethodData, \
    HarvestData


def propagate_percent(
        fasting_period: float,
        checkpoints: List[float],
        fasting_coefs: List[float]
):
    """
    Prerequisites:
        coefs must be in % rather than fractions
           Example: [0., 0.25, 0.375]
        checkpoints must reflect new coef update time (in hours)
            Example: [4, 6]
    Calculates steps to get initial weight
        assuming you have multiple processes with corresponding coeffs in % (!)

    """

    def propagate_hours(_hours: float,
                        _checkpoint: float):
        if _hours <= _checkpoint:
            return _hours, 0.
        else:
            return _checkpoint, _hours - _checkpoint

    assert len(checkpoints) + 1 == len(fasting_coefs)
    remaining = fasting_period
    total_percent = 0.
    # divide hours
    # remaining = 0.
    idx = 0
    for checkpoint in checkpoints:
        hours, remaining = propagate_hours(remaining, checkpoint)
        total_percent += hours * fasting_coefs[idx]
        idx += 1
        if remaining == 0.:
            # idx -= 1;
            break
        # repeat
    # execute multiplication one last time:
    # but using remaining
    total_percent += remaining * fasting_coefs[idx]
    # return
    return total_percent


class PiwfhaMethod:
    def __init__(self, method_id: int, method_name: str, fasting_coefs: List[float], checkpoints: List[float]):
        """

        :param method_id: IMPORTANT! The same as in DB
        :param method_name:
        :param fasting_coefs:
        :param checkpoints:
        """
        self.id: int = method_id
        self.name: str = method_name
        self.fasting_coefs = fasting_coefs
        self.checkpoints = checkpoints

        self.piwfha_time = datetime.time(12, 0, 0)
        self.standard_lifting_to_stop_feed_delay = datetime.timedelta(hours=2)

    def __str__(self):
        return self.name

    @staticmethod
    def get_normalized_standard_hour_gain(
            standard: pd.Series,
            slt_age: int,
            fasting_start_weight: float) -> float:
        _standard_daily_gain = standard[slt_age + 1] - standard[slt_age]
        _standard_daily_gain_norm = _standard_daily_gain / standard[slt_age] * fasting_start_weight
        _standard_hour_weight_gain = _standard_daily_gain_norm / 24
        print(f'_standard_daily_gain_norm: {np.round(_standard_daily_gain_norm, 3)}')
        return _standard_hour_weight_gain

    def define_piwfha_dt(self, harvest_data: HarvestData) -> datetime:
        _ref_dt = harvest_data.harvest_date
        piwfha_dt = datetime.datetime(_ref_dt.year, _ref_dt.month, _ref_dt.day,
                                      self.piwfha_time.hour, self.piwfha_time.minute, self.piwfha_time.second)
        return piwfha_dt

    def define_fasting_start_dt(self, harvest_data: HarvestData) -> datetime.datetime:
        """
        Fasting start datetime defined for each method individually

        :param harvest_data:
        :return: fasting start datetime
        """
        ...

    def define_weight_loss(self, harvest_data: HarvestData):
        assert harvest_data.fasting_period is not None, "Could not define_weight_loss as fasting_period is None"
        return propagate_percent(fasting_period=harvest_data.fasting_period,
                                 checkpoints=self.checkpoints,
                                 fasting_coefs=self.fasting_coefs)

    def update_fasting_data(self, harvest_data: HarvestData):
        # define fasting_start_dt
        harvest_data.fasting_start_dt = self.define_fasting_start_dt(harvest_data)

        # define fasting_start_weight
        _weight_loss = self.define_weight_loss(harvest_data)
        harvest_data.fasting_start_weight = harvest_data.slt_weight / (1.0 - _weight_loss)

    def update_piwfha_data(self, harvest_data: HarvestData, standard: pd.Series):
        #  define piwfha_dt
        harvest_data.piwfha_dt = self.define_piwfha_dt(harvest_data)

        # delta time from fasting_start and PIWFHA , h
        piwfha_to_fasting_start_delta_time = harvest_data.fasting_start_to_piwfha_period
        # get normalized standard_hour_weight_gain
        # normalization real weight to standard, because it could be much higher or lower
        standard_hour_weight_gain = self.get_normalized_standard_hour_gain(
            standard=standard,
            slt_age=harvest_data.harvest_age,
            fasting_start_weight=harvest_data.fasting_start_weight)
        harvest_data.piwfha_weight = harvest_data.fasting_start_weight \
                                     + standard_hour_weight_gain * piwfha_to_fasting_start_delta_time

    def process_harvest(self, harvest_data: HarvestData,
                        standard: pd.Series,
                        inplace: bool = False,
                        **kwargs) -> Optional[HarvestData]:
        """
        !! Main function !!
        Define Fasting and PIWFHA features from  harvest_data
        if inplace==True, update input harvest_data and return None,
        else return copy of input harvest_data with updated features

        :param harvest_data: information about harvest process for 1 day
        :param standard: standard weight curve for piwfha weight propagation
        :param inplace: Update input instance or create a copy with updated fields
        :param kwargs:
        :return: if inplace==True, update input harvest_data and return None,
            else return copy of input harvest_data with updated features
        """
        if not inplace:
            _harvest_data = HarvestData(**harvest_data.__dict__)
        else:
            _harvest_data = harvest_data
        # reset piwfha weight data to avoid mismatching
        _harvest_data.reset_piwfha_weight_data()

        # Define Fasting features
        self.update_fasting_data(_harvest_data)
        assert _harvest_data.fasting_start_weight is not None
        assert _harvest_data.fasting_start_dt is not None

        # Define PIWFHA features
        self.update_piwfha_data(_harvest_data, standard=standard)
        assert _harvest_data.piwfha_dt is not None
        assert _harvest_data.piwfha_weight is not None

        _harvest_data.piwfha_comment = self.name
        _harvest_data.piwfha_method_id = self.id

        if inplace:
            return None
        else:
            return _harvest_data


class PiwfhaMethodA(PiwfhaMethod):
    """
    Variant A
    1. SLT weight
    2. SLT time
    3. Lifting time or stop_feed (fasting_start_time = Lifting time )

    Then we can use ready formulas get weight loss % and get farm target weight for lifting time
    and get PIWFHA weight to work with that.
    - If Lifting is not None: fasting_start_dt = lifting_dt
    - If Lifting is None: fasting_start_dt = stop_feed_dt + standard_lifting_stop_feed_delay
    - If Lifting-stop_feed>standard_lifting_stop_feed_delay (2h):
        fasting_start_dt as stop_feed + standard_lifting_stop_feed_delay
    """

    def __init__(self):
        super(PiwfhaMethodA, self).__init__(method_id=1,
                                            method_name="method A",
                                            fasting_coefs=[0., 0.0025, 0.00375],
                                            checkpoints=[2., 6.])

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        """
        fasting_start_dt = lifting_dt
        If lifting_dt is None - define lifting as
        :param harvest_data:
        :return:
        """
        # clarify _lifting_dt and _stop_feed_dt as can be obtained from each other
        _lifting_dt = harvest_data.lifting_dt
        _lifting_dt = None if pd.isnull(_lifting_dt) else _lifting_dt
        _stop_feed_dt = harvest_data.stop_feed_dt
        _stop_feed_dt = None if pd.isnull(_stop_feed_dt) else _stop_feed_dt

        if _lifting_dt is None and _stop_feed_dt is not None:
            _lifting_dt = _stop_feed_dt + self.standard_lifting_to_stop_feed_delay
            print(f"lifting_dt was assigned as stop_feed_dt + 2h")
        if _stop_feed_dt is None and _lifting_dt is not None:
            _stop_feed_dt = _lifting_dt - self.standard_lifting_to_stop_feed_delay
            print(f"_stop_feed_dt was assigned as lifting_dt - 2h")

        # define _fasting_start_dt as
        _fasting_start_dt = None
        # TODO: ensure that it is actual strategy
        if (_lifting_dt - _stop_feed_dt) > self.standard_lifting_to_stop_feed_delay:
            _fasting_start_dt = _stop_feed_dt + self.standard_lifting_to_stop_feed_delay
            print(f"fasting_start_dt was assigned as stop_feed_dt + 2h as _lifting_dt - _stop_feed_dt > 2h")
        else:
            _fasting_start_dt = _lifting_dt

        return _fasting_start_dt


# TODO: DEPRECATE. WRONG IMPLEMENTATION. NOT used now and not allow to set weight loss from src
class PiwfhaMethodB(PiwfhaMethod):
    """
    Variant B
    1. SLT weight
    2. Weight loss, %
    3. Lifting dt
    Then we get weight for fasting_start time and are able to extrapolate it till PIWHA to work with that

    """

    def __init__(self):
        super(PiwfhaMethodB, self).__init__("method B",
                                            fasting_coefs=[],
                                            checkpoints=[])
        raise RuntimeError(f"Method {self.name} is not available "
                           f"as new struct does not allow setting Weight loss as input")

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        assert harvest_data.lifting_dt is not None, f"for {self.name} lifting_dt is required, but lifting_dt is None"
        return harvest_data.lifting_dt


# TODO: DEPRECATE. WRONG IMPLEMENTATION. NOT used now and not allow to set weight loss from src
class PiwfhaMethodC(PiwfhaMethod):
    """
    Variant C
    1. SLT weight
    2. Weight loss, %
    3. SLT time
    Will use the standard ratio (3% loss = 8 hours of fasting time)

    """

    def __init__(self):
        self.standard_fasting_coefficient = 0.003
        super(PiwfhaMethodC, self).__init__("method A",
                                            fasting_coefs=[self.standard_fasting_coefficient],
                                            checkpoints=[])
        raise RuntimeError(f"Method {self.name} is not available "
                           f"as new struct does not allow setting Weight loss as input")

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        # TODO will not work as weight_loss is a property and could not be set
        fasting_delta_time = harvest_data.weight_loss / self.standard_fasting_coefficient
        assert harvest_data.lifting_dt is not None, f"for {self.name} lifting_dt is required, but lifting_dt is None"
        return harvest_data.slt_dt - datetime.timedelta(
            hours=fasting_delta_time)


class PiwfhaMethodD(PiwfhaMethod):
    """
    Variant D
    1. SLT weight
    2. harvest_dt

    fasting start time = harverst time
    fasting time = slt time - fasting start time
    weight loss = 0.0075*fasting time
    """

    def __init__(self):
        super(PiwfhaMethodD, self).__init__(method_id=6,
                                            method_name="method D",
                                            fasting_coefs=[0.0075],
                                            checkpoints=[])

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        if harvest_data.harvest_dt is None or pd.isnull(harvest_data.harvest_dt):
            raise RuntimeError(f"for {self.name} harvest_dt is required, but harvest_dt is None")
        return harvest_data.harvest_dt


class PiwfhaMethodMahender1(PiwfhaMethod):
    """
    Mahender advised to use this for CGCAHU
    ! static coefficient weight loss % 0.0025 per hour from stop feed till slt
    1. SLT weight
    2. SLT time
    3. Stop feed (fasting_start_time = stop feed )
    Then we can use ready formulas get weight loss % and get farm target weight for fasting_start_time
    and get PIWFHA weight to work with that

    """

    def __init__(self):
        super(PiwfhaMethodMahender1, self).__init__(method_id=7,
                                                    method_name="method Mahender 1",
                                                    fasting_coefs=[0.0025],
                                                    checkpoints=[])

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        # clarify _stop_feed_dt as can be obtained from lifting
        _stop_feed_dt = harvest_data.stop_feed_dt
        _stop_feed_dt = None if pd.isnull(_stop_feed_dt) else _stop_feed_dt
        if _stop_feed_dt is None:
            # try to define fasting_start_dt from lifting (lifting - 2h)
            if harvest_data.lifting_dt is None:
                raise ValueError(f"Could not define fasting_start_dt for method {self.name} "
                                 f"as nor stop_feed_dt nor lifting_dt was provided")
            _stop_feed_dt = harvest_data.lifting_dt - self.standard_lifting_to_stop_feed_delay
            print(f"fasting_start_dt was assigned as lifting_dt - 2h")
        fasting_start_dt = _stop_feed_dt
        return fasting_start_dt


class PiwfhaMethodMahender2(PiwfhaMethod):
    """
    Mahender advised to use this for CGTHBG and CGCAHU
    ! static coefficient weight loss % 0.0025 per hour from lifting till slt
    1. SLT weight
    2. SLT time
    3. Lifting time (fasting_start_time = lifting dt )

    Then we can use ready formulas get weight loss % and get farm target weight for lifting time
    and get PIWFHA weight to work with that
    """

    def __init__(self):
        super(PiwfhaMethodMahender2, self).__init__(method_id=8,
                                                    method_name="method Mahender 2",
                                                    fasting_coefs=[0.0025],
                                                    checkpoints=[])

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        # clarify _lifting_dt as can be obtained from stop_feed
        _lifting_dt = harvest_data.lifting_dt
        _lifting_dt = None if pd.isnull(_lifting_dt) else _lifting_dt
        _stop_feed_dt = harvest_data.stop_feed_dt
        _stop_feed_dt = None if pd.isnull(_stop_feed_dt) else _stop_feed_dt
        if _lifting_dt is None and _stop_feed_dt is not None:
            _lifting_dt = _stop_feed_dt + self.standard_lifting_to_stop_feed_delay
            print(f"lifting_dt was assigned as stop_feed_dt + 2h")

        fasting_start_dt = _lifting_dt
        return fasting_start_dt


class PiwfhaMethodMahender3(PiwfhaMethod):
    """
    Variant method Mahender 3
    1. SLT weight
    2. SLT time
    3. Lifting time (fasting_start_time = Lifting time )
    Then we can use ready formulas get weight loss % and get farm target weight for lifting time
    and get PIWFHA weight to work with that

    """

    def __init__(self):
        super(PiwfhaMethodMahender3, self).__init__(method_id=9,
                                                    method_name="method Mahender 3",
                                                    fasting_coefs=[0.0025, 0.004],
                                                    checkpoints=[12])

    def define_fasting_start_dt(self, harvest_data: HarvestData):
        # if harvest_data.lifting_dt is None:
        #     raise ValueError(f"Could not define fasting_start_dt for method {self.name} as lifting_dt is NOT provided")

        # clarify _lifting_dt as can be obtained from stop_feed
        _lifting_dt = harvest_data.lifting_dt
        _lifting_dt = None if pd.isnull(_lifting_dt) else _lifting_dt
        _stop_feed_dt = harvest_data.stop_feed_dt
        _stop_feed_dt = None if pd.isnull(_stop_feed_dt) else _stop_feed_dt

        if _lifting_dt is None and _stop_feed_dt is not None:
            _lifting_dt = _stop_feed_dt + self.standard_lifting_to_stop_feed_delay
            print(f"lifting_dt was assigned as stop_feed_dt + 2h")
        fasting_start_dt = _lifting_dt
        return fasting_start_dt


@dataclasses.dataclass
class ChPiwfhaMethodsData(PiwfhaMethodData):
    """
    Data structure for storing information about specific piwfha method by cycle-house
    """
    # Aggregation mode
    # 'max'  # adjust to max age
    # 'min'  # adjust to min age
    # 'set'  # adjust to the set_target_age.REQUIRE target_age initialization
    # 'save_all'  # adjust to min age, but save all as output
    aggregation_mode: Optional[str]

    # # Aggregation parameter. Define the strength of harvest ages for getting combined (union) weight.
    # # So if max_age_diff = None, all harvest ages aggregated with weight=1.0,
    # #    if max_age_diff > 0, than the further the age is from the target age, the less weight it have in combined value
    aggregation_max_age_diff: Optional[int]

    # will be assigned automatically in code
    calc_method: Optional[PiwfhaMethod] = None


# ! THE SAME AS IN POSTGRES TABLE
PIWFHA_METHODS: Dict[int, PiwfhaMethod] = {
    1: PiwfhaMethodA(),
    # 2: PiwfhaMethodB, NOT IMPLEMENTED
    # 5: PiwfhaMethodC, NOT IMPLEMENTED
    6: PiwfhaMethodD(),
    7: PiwfhaMethodMahender1(),
    8: PiwfhaMethodMahender2(),
    9: PiwfhaMethodMahender3()
}
