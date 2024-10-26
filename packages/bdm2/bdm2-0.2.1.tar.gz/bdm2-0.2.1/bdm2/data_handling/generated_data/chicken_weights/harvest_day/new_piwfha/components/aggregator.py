import copy
import datetime
import sys
import warnings
from typing import List, Optional, Dict

import numpy as np
import pandas as pd

from bdm2.utils.process_data_tools.components.adjustor import adjust_standard_to_values



from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import HarvestData, \
    AggregationFeatures


class PiwfhaAggregator:
    """
    Class for aggregating Harvest data for several ages
    """

    class Mode:
        MAX = 'max'  # adjust to max age
        MIN = 'min'  # adjust to min age
        SET = 'set'  # adjust to the set_target_age.REQUIRE target_age initialization
        SAVE_ALL = 'save_all'  # adjust to min age, but save all as output

    @staticmethod
    def check_method(name: str):
        if name in ['max', 'min', 'set', 'save_all']:
            return True
        return False

    @staticmethod
    def combination_age_weights(ages: List[int],
                                target_ages: List[int],
                                max_age_diff_influence: int) -> Dict[int, Dict[int, float]]:
        """
        Define weight of age to be combined to target age

        :param ages: all ages that will be used for clarification each of target age
        :param target_ages: list of target ages
        :param max_age_diff_influence:
            if age to be combined too far from target age and max_age_diff_influence is set,
                than than weight of combination will be low,
            if max_age_diff_influence==0, than weight of combination will be = 0
        :return: dict of target ages and correspondent ages to combine with impact weights
            {
                target_age_1: {
                    age2combine_1: weight1,
                    age2combine_2: weight2,
                    ..
                    }.
                target_age_2: {
                    age2combine_1: weight1,
                    age2combine_2: weight2,
                    ..
                    }
                ...
            }
        """
        age_combine_weights = {}
        for target_age in target_ages:
            _age_combine_weights = {}
            for age in ages:
                # if age == target_age:
                #     continue
                _age_combine_weights[age] = 1
                if max_age_diff_influence > 0:
                    _age_combine_weights[age] = np.round(
                        (max_age_diff_influence - abs(target_age - age)) / max_age_diff_influence, 3)
                    _age_combine_weights[age] = max(0., _age_combine_weights[age])

            age_combine_weights[target_age] = _age_combine_weights
        return age_combine_weights

    @staticmethod
    def define_aggregation_strategy(
            ages: List[int],
            mode: str,
            max_age_diff_influence: int,
            target_age: Optional[int]):
        """
        Define method how to combine several ages

        :param ages: list of all harvest ages
        :param mode:  ['min', 'max', 'set', 'save_all']
            'max': adjust to max age
            'min': adjust to min age
            'set': adjust to the set_target_age. REQUIRE target_age initialization
            'save_all': adjust to min age, but save all as output
        :param max_age_diff_influence: define weight coefficient for data of different harvest ages.
            The further age to combine from target age the less its impact
        :param target_age: target_age to adjust harvest data if mode == 'set'
        :return: structure with next format
            {
                target_age_1: {
                    age_to_adjust_1: impact_weigh_coefficient,
                    age_to_adjust_2: impact_weigh_coefficient,
                    ...
                },
                target_age_2: {...}
                ...
            }
        """
        if mode == PiwfhaAggregator.Mode.SET:
            age_weights = PiwfhaAggregator.combination_age_weights(ages=ages,
                                                                   target_ages=[target_age],
                                                                   max_age_diff_influence=max_age_diff_influence)
        else:
            # get matching of ages aggregation
            age_weights = PiwfhaAggregator.combination_age_weights(ages=ages,
                                                                   target_ages=ages,
                                                                   max_age_diff_influence=max_age_diff_influence)

            age_weights_upd = {}
            ages_to_not_process = []

            # define ages order to scan
            ages_order = list(age_weights.items())
            if mode == PiwfhaAggregator.Mode.MAX:
                ages_order = reversed(ages_order)
            for age, ages2comb in ages_order:
                if age in ages_to_not_process:
                    continue
                age_weights_upd[age] = {}

                for age2comb, age2comb_w in ages2comb.items():
                    if mode == PiwfhaAggregator.Mode.MIN \
                            and age2comb >= age and age2comb_w > sys.float_info.epsilon:
                        age_weights_upd[age][age2comb] = age2comb_w
                        ages_to_not_process.append(age2comb)

                    elif mode == PiwfhaAggregator.Mode.MAX \
                            and age2comb <= age and age2comb_w > sys.float_info.epsilon:
                        age_weights_upd[age][age2comb] = age2comb_w
                        ages_to_not_process.append(age2comb)

                    elif mode == PiwfhaAggregator.Mode.SAVE_ALL \
                            and age2comb >= age and age2comb_w > sys.float_info.epsilon:
                        age_weights_upd[age][age2comb] = age2comb_w

            age_weights = age_weights_upd

        return age_weights

    @staticmethod
    def adjust_weight_from_to(weight: float,
                              standard: pd.Series,
                              from_age: int,
                              to_age: int) -> [float, Optional[Dict[int, float]]]:
        """
        Project weight of from_age to to_age using standard curve

        :param weight: weight value to be projected
        :param standard: standard curve
        :param from_age: correspondent to weight age
        :param to_age:  target age
        :return: weight value for to_age
        """
        if weight is None or pd.isnull(weight):
            return weight, None
        if from_age == to_age:
            return weight, None
        weight_s = pd.Series([weight], index=[from_age])
        adjusted = adjust_standard_to_values(standard,
                                             weight_s,
                                             vis=False,
                                             smooth_window=1,
                                             useFirstStandardValue=True,
                                             useLastStandardValue=False,
                                             average=1)
        adjusted_dg = adjusted.diff(1).replace(np.nan, None).to_dict()
        return adjusted[to_age], adjusted_dg

    @staticmethod
    def aggregate_harvest_data(harvest_data: List[HarvestData],
                               mode: str,
                               standard: pd.Series,
                               max_age_diff_influence: int,
                               target_age: Optional[int] = None
                               ) -> List[HarvestData]:
        """
        Main function that process harvest data and redefine piwfha weights using all harvest days information.
        1. Define aggregation strategy - define target ages (only target ages will be presented in output data)
            and how other harvest days will affect the target ages (define weight coefficients)
        3. Define if birds count will affect the target ages (only if for all ages to combine birds_count != None)
        4. Recalculate piwfha weights at target ages.
            .. note:: All piwfha fields in output data will be reset (id, src_id, postfix, weight, etc.)

        :param harvest_data:
        :param mode:
        :param standard:
        :param max_age_diff_influence:
        :param target_age:
        :return:
        """
        if mode == PiwfhaAggregator.Mode.SET and target_age is None:
            raise ValueError(f"'set' mode requires set_target_age initialization")
        if len(harvest_data) == 0:
            raise ValueError(f"harvest_data is empty")

        cycle_start_date = harvest_data[0].harvest_date - datetime.timedelta(days=harvest_data[0].harvest_age)
        harvest_data_by_age: Dict[int, HarvestData] = {int(hv.harvest_age): hv for hv in harvest_data}
        all_ages = list(harvest_data_by_age)
        combine_strategy = PiwfhaAggregator.define_aggregation_strategy(all_ages,
                                                                        mode=mode,
                                                                        max_age_diff_influence=max_age_diff_influence,
                                                                        target_age=target_age)
        print(f"Aggregation strategy:")
        print(combine_strategy)

        harvest_data_comb: Dict[int, HarvestData] = {}
        # Do not consider birds count in aggregation if any of harvest age does not have birds_count information
        consider_birds_count = all([not (hv.birds_count is None
                                         or pd.isnull(hv.birds_count)
                                         or hv.birds_count == 0) for hv in harvest_data])
        # Recalculate piwfha weights at target ages
        for target_age, ages2comb in combine_strategy.items():

            aggregation_features = AggregationFeatures(
                mode=mode,
                max_age_diff_influence=max_age_diff_influence,
                aggregation_strategy=ages2comb,
                standard=standard.to_dict(),
                adjusted_dg={}
            )
            weighted_mass_sum = 0.0
            weighs_sum = 0.0
            birds_count = np.nan
            for age2comb, age2comb_w in ages2comb.items():
                raw_piwfha_weight = harvest_data_by_age[age2comb].piwfha_weight
                if raw_piwfha_weight is None or pd.isnull(raw_piwfha_weight):
                    warnings.warn(f"PIWFHA for age {age2comb} will not be considered as None")
                    continue
                _adjusted_weight, _adjusted_dg = PiwfhaAggregator.adjust_weight_from_to(
                    weight=harvest_data_by_age[age2comb].piwfha_weight,
                    standard=standard,
                    from_age=age2comb,
                    to_age=target_age)
                weight_coef = age2comb_w
                if consider_birds_count:
                    weight_coef *= harvest_data_by_age[age2comb].birds_count

                weighted_mass_sum += _adjusted_weight * weight_coef
                weighs_sum += weight_coef
                if consider_birds_count:
                    if pd.isnull(birds_count):
                        birds_count = harvest_data_by_age[age2comb].birds_count
                    else:
                        birds_count += harvest_data_by_age[age2comb].birds_count
                aggregation_features.adjusted_dg[age2comb] = _adjusted_dg

            if weighs_sum == 0 and weighted_mass_sum == 0:
                adjusted_weight = np.nan
            else:
                adjusted_weight = weighted_mass_sum / weighs_sum

            # =============================
            # generate new entity as copy of raw (individual) harvest data with updated piwfha weight fields
            harvest_data_comb[target_age] = copy.deepcopy(harvest_data_by_age[target_age])

            # generate comment with information about aggregation
            _comment = ""
            if len(ages2comb) == 1:
                # reset only database ids and onfo about weight src
                harvest_data_comb[target_age].piwfha_id = None
                harvest_data_comb[target_age].piwfha_weight_src_id = None
                harvest_data_comb[target_age].piwfha_weight_postfix = None

                _comment += 'equal to raw (individual) piwfha data.'

            else:
                # reset piwfha weight fields as combined weight - new entity
                harvest_data_comb[target_age].reset_piwfha_weight_data()
                # add aggregation_features if any ages to combine were used
                harvest_data_comb[target_age].piwfha_agg_features = aggregation_features

                _comment += f"combined. mode: {mode}, {ages2comb}."
                if not consider_birds_count:
                    _comment += " birds_count was NOT used"
                else:
                    _comment += " birds_count was used"

            # assign piwfha_weight to combined value
            harvest_data_comb[target_age].piwfha_weight = adjusted_weight

            target_piwfha_dt = cycle_start_date + datetime.timedelta(days=target_age)
            harvest_data_comb[target_age].piwfha_dt = datetime.datetime(target_piwfha_dt.year,
                                                                        target_piwfha_dt.month,
                                                                        target_piwfha_dt.day,
                                                                        12, 0, 0)

            harvest_data_comb[target_age].piwfha_comment = _comment
            harvest_data_comb[target_age].birds_count = birds_count

        return list(harvest_data_comb.values())
