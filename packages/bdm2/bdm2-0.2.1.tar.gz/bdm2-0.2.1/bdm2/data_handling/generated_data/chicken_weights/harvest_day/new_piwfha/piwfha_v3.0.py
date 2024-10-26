""" Script for calculating and saving PIWFHA data

Script fetch SLT and available PIWFHA data from database. Process it and calculate new PIWFHA features
that will be updated in Database.

The cycle-houses are processed one by one.
1. Define piwfha calculation parameters for cycle-house from database (or based on available slt data)
2. Calculate individual piwfha features for each harvest day
3. Calculate combined piwfha features for cycle house
4. Save (update) individual and  combined piwfha features to database

Script parameters:
    - hard_update: DELETE all previous piwfha data for cycle house in database first and only after that save new data.
        It is important if set of harvest ages was changed.
    - ignore_bad_harvest_ages:
        if False - drop the WHOLE cycle-house if any of harvest age has a problem
        if True  - drop problem ages and CONTINUE process cycle-house without problem harvest days

"""

import copy
import dataclasses
import datetime
import sys
import traceback
import warnings
from pathlib import Path
from typing import Dict, Optional, List

import numpy as np
import pandas as pd
import yaml

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.aggregator import \
    PiwfhaAggregator
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.api_wrapper import APIWrapper
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.methods_factory import \
    PiwfhaMethodFactory

PiwfhaMethodFactory
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter



from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import HarvestData, \
    CycleHarvestData, WeightSrcInfo


@dataclasses.dataclass
class Config:
    # creds_path: str  # r"C:\Users\JemaimaUser\Downloads\anya_user_api.yaml"
    filters: Filter  # Define data that will be processed
    save_weights_postfix: Optional[str]  # "_lifting_final"  # _new_method_union  _new_union

    update_db: bool  # = True
    hard_update: bool  # if True, delete all piwfha data for combination cycle_house_code, weight_src

    # Define problem harvest day strategy
    #   False - drop the WHOLE cycle-house if any of harvest age has a problem
    #   True - drop problem ages and CONTINUE process cycle-house without problem harvest days
    ignore_bad_harvest_ages: bool  # False

    # Default combination that will be used if there is no standard for some combinations
    default_comb_key = ('DEFAULT', 'DEFAULT', 'DEFAULT')

    # Aggregation parameters are stored in database and can be set for client.
    # But if there is no any specific aggregation parameter in database, default values will be used
    # TODO: maybe define default values also in database for DEFAULT client
    default_agg_max_age_diff: Optional[int]
    default_agg_mode: Optional[str]

    # union postfix that will be added to save_weights_postfix for combined values
    _union_postfix_ext: str = "_union"  #

    @property
    def union_postfix(self):
        return None if self.save_weights_postfix is None else self.save_weights_postfix + self._union_postfix_ext

    def __post_init__(self):
        if isinstance(self.filters, dict):
            self.filters = Filter(**self.filters)


class BadCycleHouseData(Exception):
    pass


class BadHarvestDayData(Exception):
    pass


@dataclasses.dataclass
class ProcessStatus:
    is_success: bool = False
    error: Optional[Exception] = None


def get_round(v, decimal):
    if v is None:
        return None
    else:
        return np.round(v, decimal)


def check_before_process(harvest_day_data: HarvestData):
    if harvest_day_data.slt_weight is None or pd.isnull(harvest_day_data.slt_weight):
        raise BadHarvestDayData(
            f'{ch} age {harvest_day_data.harvest_age}: No slt weight information')

    if harvest_day_data.slt_weight < sys.float_info.epsilon:
        raise BadHarvestDayData(
            f'{ch} age {harvest_day_data.harvest_age}: Bad slt weight value: {harvest_day_data.slt_weight}')


def check_before_save(ch_harvest_data: CycleHarvestData):
    for hv_data in ch_harvest_data.harvest_data:
        if hv_data.slt_weight is None or pd.isnull(hv_data.slt_weight):
            raise BadHarvestDayData("slt weight is None")
        if hv_data.piwfha_weight_src_id is None or pd.isnull(hv_data.piwfha_weight_src_id):
            raise BadHarvestDayData("No piwfha weight src info")


def set_weight_src_info(ch_harvest_data: Dict[str, CycleHarvestData],
                        weight_src_info: Dict[str, WeightSrcInfo],
                        mode: str):
    available_modes = ['union', 'individual']
    assert mode in available_modes, f"Wrong mode {mode}. Availabe modes: {available_modes}"
    for ch, ch_data in ch_harvest_data.items():
        for hv_data in ch_data.harvest_data:
            if mode == 'individual':
                hv_data.piwfha_weight_src_id = weight_src_info[ch].piwfha_individual_src_id
                hv_data.piwfha_weight_postfix = weight_src_info[ch].piwfha_individual_src_postfix
            elif mode == 'union':
                hv_data.piwfha_weight_src_id = weight_src_info[ch].piwfha_union_src_id
                hv_data.piwfha_weight_postfix = weight_src_info[ch].piwfha_union_src_postfix


def print_errors(processing_status: Dict[str, ProcessStatus]):
    for _ch, _proc_status in processing_status.items():
        if not _proc_status.is_success:
            print(f"{_ch}: {_proc_status.error}")


def print_final(ch_data_all_comb, ch_data_all_individual, ch_data_all_raw):
    print()
    print(f"FINAL")
    for ch, ch_data in ch_data_all_comb.items():
        print(f"\n========================")
        print(f"{ch} {ch_data.farm_name} {ch_data.house_name}")
        union_harvest_data = ch_data.harvest_data
        individual_harvest_data = ch_data_all_individual[ch].harvest_data
        db_harvest_data = ch_data_all_raw[ch].harvest_data

        for hvd in union_harvest_data:
            _individual_hvd:Optional[HarvestData] = None
            _db_hvd:Optional[HarvestData] = None
            for individual_hvd in individual_harvest_data:
                if individual_hvd.harvest_age == hvd.harvest_age:
                    _individual_hvd = individual_hvd
                    break

            for db_hvd in db_harvest_data:
                if db_hvd.harvest_age == hvd.harvest_age:
                    _db_hvd = db_hvd
                    break

            print(f"Age {hvd.harvest_age} "
                  f"\nSlT = {get_round(hvd.slt_weight, 3)} kg"
                  f"\nPiwfha:"
                  f"\n\tnew combined (piwfha{hvd.piwfha_weight_postfix}): {get_round(hvd.piwfha_weight, 3)} kg - {hvd.piwfha_comment}"
                  f"\n\told combined (piwfha{_db_hvd.piwfha_weight_postfix}):   {get_round(_db_hvd.piwfha_weight, 3)} kg - {_db_hvd.piwfha_comment} "
                  f"\n\tindividual (piwfha{_individual_hvd.piwfha_weight_postfix}):   {get_round(_individual_hvd.piwfha_weight, 3)} kg - {_individual_hvd.piwfha_comment}")


if __name__ == '__main__':
    config_path = Path('piwfha_config.yaml')
    config = Config(**yaml.load(open(config_path), yaml.Loader))

    api = APIWrapper()
    piwfhaMethodFactory = PiwfhaMethodFactory(api,
                                              default_aggregation_mode=config.default_agg_mode,
                                              default_aggregation_max_age_diff=config.default_agg_max_age_diff)

    # =====================================
    # GETTING DATA
    standards = api.get_standards()
    ch_data_all_raw: Dict[str, CycleHarvestData] = api.get_harvest_data(config.filters, None)
    weight_src_info = api.get_actual_weight_source_info(
        union_piwfha_postfix=config.union_postfix,
        filters=config.filters)

    # check if all cycle_houses in ch_data_all are in weight_src_info
    unavailable_ch = set(ch_data_all_raw.keys()).difference(set(weight_src_info.keys()))
    if len(unavailable_ch) > 0:
        raise RuntimeError(f"There is no weight src information for the next cycle_houses: \n{unavailable_ch} ")

    # =====================================
    # INIT
    # cycle-house data for each harvest day
    ch_data_all_individual: Dict[str, CycleHarvestData] = {}  # = copy.deepcopy(ch_data_all_raw)
    # cycle-house data only for aggregated harvest days
    ch_data_all_comb: Dict[str, CycleHarvestData] = {}

    processing_statuses: Dict[str, ProcessStatus] = {}

    for ch, _ch_data in ch_data_all_raw.items():
        try:
            ch_data = copy.deepcopy(_ch_data)
            comb_key = (ch_data.client_name, ch_data.breed_type, ch_data.gender)
            ch_key = (ch_data.farm_name, ch_data.house_name, ch_data.cycle_house_name)
            print()
            print("=======================================================")
            print(f"Processing {ch} ({ch_key}) - {comb_key}")
            print(f"{len(ch_data.harvest_data)} harvest days found")

            # Init process status as False. Set True only in case of reaching the end of processing block
            processing_statuses[ch] = ProcessStatus(is_success=False)

            # get correspondent standard
            if comb_key in standards:
                ch_standard = standards[comb_key]
            else:
                ch_standard = standards[config.default_comb_key]
                warnings.warn(f"DEFAULT STANDARDS IS USED")

            # ===================================================
            # Calculating individual PIWFHA
            # ===================================================
            bad_harvest_days = []

            for harvest_day_ind, harvest_day_data in enumerate(ch_data.harvest_data):
                print(f"Processing {ch} harvest age {harvest_day_data.harvest_age} ")
                try:
                    check_before_process(harvest_day_data)

                    # get piwfha calculation method
                    method = piwfhaMethodFactory.get_calc_piwfha_method(ch, harvest_day_data)
                    if method is None:
                        raise BadHarvestDayData(
                            f"{ch} age {harvest_day_data.harvest_age}: No available piwfha method")
                    print(method.name)

                    # process harvest data
                    method.process_harvest(harvest_day_data, standard=ch_standard, inplace=True)

                    print(f"Age {harvest_day_data.harvest_age} "
                          f"\n\tSlT:            {get_round(harvest_day_data.slt_weight, 3)} kg ({harvest_day_data.slt_dt})"
                          f"\n\tFasting start:  {get_round(harvest_day_data.fasting_start_weight, 3)} kg ({harvest_day_data.fasting_start_dt})"
                          f"\n\tPiwfha:         {get_round(harvest_day_data.piwfha_weight, 3)} kg ({harvest_day_data.piwfha_dt})"
                          f"\n\tFasting period: {get_round(harvest_day_data.fasting_period, 1)} h"
                          f"\n\tWeight loss:    {get_round(harvest_day_data.weight_loss, 3)} %"
                          f"\n\tBirds count:    {get_round(harvest_day_data.birds_count, 0)}")
                except Exception as e:
                    if config.ignore_bad_harvest_ages:
                        print(f"!!! {ch} age {harvest_day_data.harvest_age}: will be skipped as: " + str(e))
                        bad_harvest_days.append(harvest_day_data.harvest_age)
                        continue
                    else:
                        # Go to next cycle_house (->except block on cycle house iterator level)
                        raise e

            if len(bad_harvest_days) > 0:
                # Drop problem harvest days
                ch_data.harvest_data = [hvd for hvd in ch_data.harvest_data if hvd.harvest_age not in bad_harvest_days]

            # Check if any valuable harvest days left
            if len(ch_data.harvest_data) == 0:
                raise BadCycleHouseData(f'{ch}: No valuable harvest data')

            ch_data_all_individual[ch] = ch_data
            # ===================================================
            # Aggregation
            # ===================================================
            agg = PiwfhaAggregator()
            mode = piwfhaMethodFactory.get_aggregation_piwfha_method(cycle_house_code=ch_data.cycle_house_code)
            max_age_diff = piwfhaMethodFactory.get_aggregation_max_age_diff(cycle_house_code=ch_data.cycle_house_code)

            print(f"Aggregation method: {mode}")
            print(f"Max age diff: {max_age_diff}")
            _harvest_data_comb = agg.aggregate_harvest_data(ch_data.harvest_data,
                                                            standard=ch_standard,
                                                            mode=mode,
                                                            max_age_diff_influence=max_age_diff,
                                                            target_age=None)

            print(f"PIWFHA after combination {ch}")
            for hvd in _harvest_data_comb:
                hvd_individual:Optional[HarvestData] = None
                for _hvd in ch_data.harvest_data:
                    if _hvd.harvest_age == hvd.harvest_age:
                        hvd_individual = _hvd
                print(f"Age {get_round(hvd.harvest_age, 0)} "
                      f"SlT weight = {get_round(hvd.slt_weight, 3)} kg "
                      f"Piwfha weight = {get_round(hvd.piwfha_weight, 3)}kg "
                      f"(individual = {get_round(hvd_individual.piwfha_weight, 3) if hvd_individual else None} kg)")

            ch_data_all_comb[ch] = copy.deepcopy(ch_data)
            ch_data_all_comb[ch].harvest_data = copy.deepcopy(_harvest_data_comb)

            processing_statuses[ch].is_success = True
        except BadCycleHouseData as e:
            processing_statuses[ch].error = e
            print(f"!!! {ch} will be skipped as: {e}")
        except BadHarvestDayData as e:
            processing_statuses[ch].error = e
            print(f"!!! {ch} will NOT BE PROCESSED because of bad harvest data: {e}")
        except Exception as e:
            processing_statuses[ch].error = e
            print(traceback.format_exc())
            raise e

    # set piwfha src id for saving
    set_weight_src_info(ch_data_all_individual, weight_src_info=weight_src_info, mode='individual')
    set_weight_src_info(ch_data_all_comb, weight_src_info=weight_src_info, mode='union')

    # ====================================
    # PROCESSING FINALS
    print_final(ch_data_all_comb=ch_data_all_comb,
                ch_data_all_raw=ch_data_all_raw,
                ch_data_all_individual=ch_data_all_individual)
    print_errors(processing_status=processing_statuses)

    # ====================================
    # CHECK DATA BEFORE SAVING
    ch_data_all_to_save: List[CycleHarvestData] = []

    print()
    print(f"Checking final INDIVIDUAL harvest days before saving")
    for ch, ch_data in ch_data_all_individual.items():
        try:
            check_before_save(ch_data)
            ch_data_all_to_save.append(copy.deepcopy(ch_data))
        except Exception as e:
            print(f"{ch} WILL BE SKIPPED AS: {e}")

    print()
    print(f"Checking final COMBINED harvest days before saving")
    for ch, ch_data in ch_data_all_comb.items():
        try:
            check_before_save(ch_data)
            ch_data_all_to_save.append(copy.deepcopy(ch_data))
        except Exception as e:
            print(f"{ch} WILL BE SKIPPED AS: {e}")

    print()
    if config.update_db:
        print(f"Updating piwfha data")
        _st = datetime.datetime.now()
        api.update_piwfha_data(ch_data_all_to_save, hard_update=config.hard_update)
        _end = datetime.datetime.now()
        print(f"Took {get_round((_end - _st).total_seconds(), 3)} s")
    else:
        print(f"DATA WILL NOT BE SAVED AS UPDATE_DB==False")
