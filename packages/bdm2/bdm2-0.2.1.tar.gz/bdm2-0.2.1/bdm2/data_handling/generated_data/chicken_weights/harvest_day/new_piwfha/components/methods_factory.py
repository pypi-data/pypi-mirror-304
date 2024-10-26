import warnings
from typing import Dict, Optional

import pandas as pd

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.api_wrapper import APIWrapper
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.methods import \
    ChPiwfhaMethodsData, PiwfhaMethod, PIWFHA_METHODS



from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import HarvestData


class PiwfhaMethodFactory:
    """
    Class for handling PIWFHA calculation features for different cycle-houses.

    PIWFHA calculation features:
     - calc method: define how no calculate piwfha from slt data
     - aggregation mode: define how to combine close harvest ages
     - aggregation max age diff: define for far each other harvest days could be for combination

    Uses BRDDB API WRAPPER for all requests to database

    """

    def __init__(self, api_client: APIWrapper,
                 default_aggregation_mode: str,
                 default_aggregation_max_age_diff: int):
        self._specific_method_by_ch_cache: Dict[str, ChPiwfhaMethodsData] = {}
        self.api_client = api_client
        self.default_aggregation_mode = default_aggregation_mode
        self.default_aggregation_max_age_diff = default_aggregation_max_age_diff

    def _update_specific_method_by_client_cache(self):
        self._specific_method_by_ch_cache = self.api_client.get_specific_piwfha_methods(filters=None)

    def get_specific_calc_features(self, cycle_house_code: str) -> Optional[ChPiwfhaMethodsData]:
        """
        Return all specific piwfha calculation fetures:
         - piwfha calc method (name, description, etc.)
         - piwfha aggregation features (mode, max_age_diff, etc.)

        :param cycle_house_code: str, cycle-house of interest
        :return:
        """
        _output: Optional[ChPiwfhaMethodsData] = None
        if cycle_house_code not in self._specific_method_by_ch_cache:
            print(f"Updating specific_method_by_ch_cache")
            self._update_specific_method_by_client_cache()
        if cycle_house_code in self._specific_method_by_ch_cache:
            _output = self._specific_method_by_ch_cache[cycle_house_code]
        return _output

    def get_common_calc_method(self, harvest_data: HarvestData) -> Optional[PiwfhaMethod]:
        """

        Return COMMON piwfha calculation method, based on available harvest_data

        :param harvest_data:
        :return:
        """
        if not pd.isnull(harvest_data.slt_dt) \
                and (not pd.isnull(harvest_data.lifting_dt) or not pd.isnull(harvest_data.stop_feed_dt)):
            return PIWFHA_METHODS[1]  # PiwfhaMethodA()
        elif not pd.isnull(harvest_data.slt_dt) and not pd.isnull(harvest_data.harvest_dt):
            return PIWFHA_METHODS[6]  # PiwfhaMethodD()
        return None

    def get_calc_piwfha_method(self, cycle_house_code: str, harvest_data: HarvestData) -> Optional[PiwfhaMethod]:
        """
        Return correspondent piwfha calculation method.
        Checks if there is a specific method for the given снсду-house. If there is not, then define a common method
        based on the harvest_data

        :param cycle_house_code:
        :param harvest_data: will be required if there is no specific methods defined for cycle_house_code
        :return: orrespondent piwfha calculation method
        """

        # check if cycle_house_code in specific_method_by_client_cache. If not - update specific_method_by_client_cache
        _output = self.get_specific_calc_features(cycle_house_code).calc_method

        # if _output_method is still None (does not have match for specific method) - define it as common
        if _output is None:
            _output = self.get_common_calc_method(harvest_data)
        return _output

    def get_aggregation_piwfha_method(self, cycle_house_code: str) -> Optional[str]:
        """
        Return correspondent piwfha aggregation method.
        Available values:
         - min
         - max
         - save_all

        :param cycle_house_code: str
        :return: str, correspondent piwfha aggregation method
        """

        # check if cycle_house_code in specific_method_by_client_cache. If not - update specific_method_by_client_cache
        _output = self.get_specific_calc_features(cycle_house_code).aggregation_mode

        # if _output_method is None (does not have match for specific method) - define it as default
        if _output is None:
            _output = self.default_aggregation_mode

        return _output

    def get_aggregation_max_age_diff(self, cycle_house_code: str) -> Optional[int]:
        """
        Return correspondent piwfha aggregation feature - max_age_diff

        :param cycle_house_code: str
        :return: int, correspondent max_age_diff for piwfha aggregation
        """

        # check if cycle_house_code in specific_method_by_client_cache. If not - update specific_method_by_client_cache
        _output = self.get_specific_calc_features(cycle_house_code).aggregation_max_age_diff

        # if _output_method is None (does not have match for specific method) - define it as default
        if _output is None:
            _output = self.default_aggregation_max_age_diff

        return _output