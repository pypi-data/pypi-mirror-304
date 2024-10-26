import dataclasses
import json
import warnings
from typing import Optional, Dict, Tuple, List

import pandas as pd
import requests
from brddb.connection import brddbapi, BrddbApiConnection
from brddb.constants import PgColumns, BrddbApiEndpoints
from brddb.credentials import BrddbApiCredentials
from brddb.schemas.pydantic.others import BirdooFilter
from brddb.schemas.pydantic.postgres.piwfha import PIWFHAUpdateRequest, PIWFHA2Update
from bdm2.constants.global_setup.env import BRDDB_API_URL, BRDDB_API_USERNAME, BRDDB_API_PASSWORD

from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.methods import \
    ChPiwfhaMethodsData, PIWFHA_METHODS
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.models import CycleHarvestData, \
    HarvestData, WeightSrcInfo
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


class APIWrapper:

    def __init__(self):
        """
        Create instance of API client

        :param creds_path: path to creds with next struct:
            host: 'https://.../brddbapi' # the same as `host` but named as endpoint in amazon rds console page
            username: 'user'
            password: 'password'
        """
        # self.credentials: BrddbApiCredentials = brddbapi.load_brddbapi_credentials(creds_path)

        self.credentials: BrddbApiCredentials = BrddbApiCredentials(
            host=BRDDB_API_URL,
            username=BRDDB_API_USERNAME,
            password=BRDDB_API_PASSWORD,
            port=None,)
        self.token = None

        self.actual_clients_info_endpoint = f'{self.credentials.host}/api/v1/views/actual-clients-info-storage'

        self.get_specific_piwfha_methods_endpoint = f'{self.credentials.host}/api/v1/slt_interface/specific-piwfha-methods-by-ch'
        self.get_actual_weight_source_info_endpoint = f'{self.credentials.host}/api/v1/slt_interface/weight-source-info-by-ch'

        self.update_harvest_data_endpoint = f'{self.credentials.host}/api/v1/slt_interface/upsert-piwfha-data'
        self.get_harvest_data_endpoint = f'{self.credentials.host}/api/v1/slt_interface/piwfha-data'
        self.devices_endpoint = f'{self.credentials.host}{BrddbApiEndpoints.devices_view}'
    def _update_token(self):
        """
        Update toking for performing requests to API
        :return:
        """
        form_data = BrddbApiConnection.get_form_data(self.credentials)
        token_url = BrddbApiConnection.get_token_url(self.credentials)
        request = requests.post(url=token_url, data=form_data)
        resp = request.json()
        self.token = resp['access_token']

    def _header(self):
        return {
            'Authorization': f"Bearer {self.token}"
        }

    def perform_get_request(self, url, params):
        if self.token is None:
            self._update_token()
        response = requests.get(url, params=params, headers=self._header())
        if response.status_code == 403:
            self._update_token()
            response = requests.get(url, params=params, headers=self._header())
        return response

    def perform_post_request(self, url, params):
        if self.token is None:
            self._update_token()
        response = requests.post(url, json=params, headers=self._header())
        if response.status_code == 403:
            self._update_token()
            response = requests.get(url, json=params, headers=self._header())
        return response

    @staticmethod
    def filter2birdoofilter(filter: Filter) -> BirdooFilter:
        """
        Convert BIRDOO_IP.Filter to brddb.BirdooFilter

        :param filter:
        :return:
        """
        brddb_filter = BirdooFilter(
            clients=None,
            breed_types=None,
            genders=None,
            farms=None,
            cycles=None,
            houses=None,
            devices=None,
            ages=None,
            start_time=None,
            end_time=None
        )
        for key, value in vars(filter).items():
            if key in BirdooFilter.__annotations__ and value != []:
                setattr(brddb_filter, key, value)
        brddb_filter.start_time = None
        brddb_filter.end_time = None
        return brddb_filter

    def get_standards(self) -> Dict[Tuple, pd.Series]:
        """
        Get all standards by combination (client, breed_type, gender)

        :return: standards by combination with next format:
            {
                (client, breed_type, gender): standard,
                 ...
             }
        """
        response = self.perform_get_request(self.actual_clients_info_endpoint, params={})
        # if response.status_code
        output_data = response.json()
        combination_info_df = pd.DataFrame(output_data)

        output_combination_info: Dict[Tuple, pd.Series] = {}
        for _, row in combination_info_df.iterrows():
            if row['standard_weights'] is None:
                continue

            combination = (row[PgColumns.client_name], row[PgColumns.breed_type_name], row[PgColumns.gender_name])
            if type(row['standard_weights']) == str:
                _standard = pd.DataFrame.from_dict(json.loads(row['standard_weights']))
            elif type(row['standard_weights']) == dict:
                _standard = pd.DataFrame.from_dict(row['standard_weights'])
            else:
                raise ValueError(f"Wrong standard_weights format in database for {combination}")

            output_combination_info[combination] = _standard.set_index('age')['Weights']
        return output_combination_info

    @staticmethod
    def additional_filter(filters, res):
        list_of_dicts = json.loads(res.text)

        mid = []
        for d in list_of_dicts:
            if filters.clients:
                if d['client_name'] in filters.clients:
                    pass
                else:
                    continue
            if filters.breed_types:
                if d['breed_type'] in filters.breed_types:
                    pass
                else:
                    continue
            if filters.genders:
                if d['gender'] in filters.genders:
                    pass
                else:
                    continue
            if filters.cycles:
                if d['cycle_house_name'] in filters.cycles:
                    pass
                else:
                    continue
            if filters.houses:
                if d['houses_name'] in filters.houses:
                    pass
                else:
                    continue

            mid.append(d)
        return mid
    def get_harvest_data(self, filters: Filter, weights_postfix: Optional[str]) -> Dict[str, CycleHarvestData]:
        """
        Get harvest data from db, that containds full information about harvest process:
            - cycle-house info
            - slt timetable (data from slt_timetable table: all timestamps, weights, etc)
            - piwfha data (data from piwfha_new table)
        :param filters: filter data to be fetched
        :param weights_postfix: postfix of weight src for piwfha (if None, get actual piwfha)
        :return:
        """

        brddb_filters = self.filter2birdoofilter(filters).__dict__
        res = self.perform_post_request(self.get_harvest_data_endpoint,
                                        params={"filters": brddb_filters,
                                                "piwfha_weight_postfix": weights_postfix,
                                                "drop_empty_slt": True,
                                                # "refresh": True

                                                }
                                        )

        # res = get_harvest_data(brddb_filters, piwfha_weight_src_postfic=weights_postfix)
        mid = self.additional_filter(filters, res)
        res_df = pd.DataFrame(mid)

        _output_data: Dict[str, CycleHarvestData] = {}
        harvest_data_fields = [f.name for f in dataclasses.fields(HarvestData)]
        harvest_day_columns = [c for c in res_df.columns if c in harvest_data_fields]
        cycle_data_fields = [f.name for f in dataclasses.fields(CycleHarvestData)]
        cycle_data_columns = [c for c in res_df.columns if c in cycle_data_fields]
        for ch, data in res_df.groupby(PgColumns.cycle_house_code):
            _harvest_data = []
            for _, r in data.sort_values(PgColumns.harvest_age).iterrows():
                if r[PgColumns.harvest_age] is None or pd.isnull(r[PgColumns.harvest_age]):
                    continue
                _harvest_data.append(HarvestData(**r[harvest_day_columns].to_dict()))

            r = data.iloc[0]
            cycle_data = CycleHarvestData(harvest_data=_harvest_data, **r[cycle_data_columns].to_dict())
            _output_data[str(ch)] = cycle_data
        return _output_data

    def get_specific_piwfha_methods(self,
                                    filters: Optional[Filter]) -> Dict[str, ChPiwfhaMethodsData]:
        """
        Get information about piwfha calculation method for each cycle-house

        :param filters: filter data to be fetched
        :return:
        """
        brddb_filters = None
        if filters is not None:
            brddb_filters = self.filter2birdoofilter(filters).__dict__

        # TODO: get from brddb_api
        res = self.perform_post_request(self.get_specific_piwfha_methods_endpoint,
                                        params={'filters': brddb_filters, })
        # res = get_specific_piwfha_methods(filters=brddb_filters)

        res_df = pd.DataFrame(res.json())
        res_df.columns = [c.replace('piwfha_', '') for c in res_df.columns]
        _fields = [f.name for f in dataclasses.fields(ChPiwfhaMethodsData) if f.name in res_df.columns]

        _output = {}
        for _, row in res_df.iterrows():
            _cycle_house_code = row[PgColumns.cycle_house_code]
            ch_data = ChPiwfhaMethodsData(**row[_fields])
            if ch_data.calc_method_id is not None and not pd.isnull(ch_data.calc_method_id):
                try:
                    ch_data.calc_method = PIWFHA_METHODS[ch_data.calc_method_id]
                except KeyError:
                    warnings.warn(f'Not implemented piwfha method for {_cycle_house_code}:'
                                  f'{ch_data.calc_method_name} (id:{ch_data.calc_method_id})')

            _output[_cycle_house_code] = ch_data
        return _output

    def get_actual_weight_source_info(self,
                                      union_piwfha_postfix: Optional[str] = None,
                                      targets_postfix: Optional[str] = None,
                                      filters: Optional[Filter] = None) -> Dict[str, WeightSrcInfo]:
        """
        Get information about actual weight sources (weight_src_id, weight_src_postfix) for each cycle house:
            - actual targets weight src
            - actual likely_targets weight src
            - actual individual_piwfha weight src
            - actual union_piwfha weight src

        :param union_piwfha_postfix: request specific union_piwfha_postfix.
            individual_piwfha_postfix will be defined automatically.
        :param targets_postfix: unioin postfix for targets and likely_targets
        :param filters :filter data to be fetched
        :return:
        """
        brddb_filters: Dict[str, List[str]] = self.filter2birdoofilter(filters).__dict__

        res = self.perform_post_request(self.get_actual_weight_source_info_endpoint,
                                        params={'filters': brddb_filters,
                                                'union_piwfha_postfix': union_piwfha_postfix,
                                                'targets_postfix': targets_postfix})
        # res = get_actual_weight_source_info(union_piwfha_postfix=union_piwfha_postfix,
        #                                     targets_postfix=targets_postfix,
        #                                     filters=brddb_filters)
        res_df = pd.DataFrame(res.json())

        _fields = [f.name for f in dataclasses.fields(WeightSrcInfo)]
        # check_duplicated
        _duplicated_ch = res_df.loc[res_df.duplicated()][PgColumns.cycle_house_code]
        if len(_duplicated_ch) > 0:
            raise RuntimeError(f"Duplicated cycle_houses in response:\n"
                               f"{_duplicated_ch}")

        output = {}
        for _, row in res_df.iterrows():
            output[row[PgColumns.cycle_house_code]] = WeightSrcInfo(**row[_fields])

        return output

    def update_piwfha_data(self, cycle_house_data: List[CycleHarvestData], hard_update: bool):
        """
        Save data to piwfha table in db as scope.
        If any of entity has a problem during saving. The whole pack will NOT be saved

        :param cycle_house_data: data to be saved
        :return:
        """
        piwfha2update: PIWFHAUpdateRequest = PIWFHAUpdateRequest(hard_update=hard_update,
                                                                 user="piwfha_3.0_api",
                                                                 data=[])
        for ch_data in cycle_house_data:
            for hv_data in ch_data.harvest_data:
                try:
                    agg_features_json = json.dumps(
                        vars(hv_data.piwfha_agg_features)) if hv_data.piwfha_agg_features is not None else None
                    p2u = PIWFHA2Update(
                        cycle_house_code=ch_data.cycle_house_code,

                        slt_id=hv_data.slt_id,
                        weight_src_postfix=hv_data.piwfha_weight_postfix,
                        weight_src_id=hv_data.piwfha_weight_src_id,

                        age=hv_data.harvest_age,
                        weight=hv_data.piwfha_weight,
                        piwfha_dt=hv_data.piwfha_dt,
                        method_id=hv_data.piwfha_method_id,  # if not pd.isnull(hv_data.piwfha_method_id) else None,

                        # fasting_start_dt=hv_data.fasting_start_dt,
                        fasting_start_dt=hv_data.fasting_start_dt if not pd.isnull(hv_data.fasting_start_dt) else None,
                        # fasting_start_weight=hv_data.fasting_start_weight,
                        fasting_start_weight=hv_data.fasting_start_weight if not pd.isnull( hv_data.fasting_start_weight) else None,

                        # fasting_time=hv_data.fasting_period
                        fasting_time=hv_data.fasting_period if not pd.isnull(hv_data.fasting_period) else None,
                        # weight_loss=hv_data.weight_loss,
                        weight_loss=hv_data.weight_loss if not pd.isnull(hv_data.weight_loss) else None,

                        aggregation_features=agg_features_json,
                        comment=hv_data.piwfha_comment
                    )
                    piwfha2update.data.append(p2u)
                except Exception as e:
                    print(f"{ch_data.cycle_house_code} age {hv_data.harvest_age}: {e}")
                    # raise e

        print(f"Upserting:"
              f"\n\t{len(piwfha2update.data)} rows to upsert"
              f"\n\thard_update: {piwfha2update.hard_update}")
        res = self.perform_post_request(self.update_harvest_data_endpoint,
                                        params=piwfha2update.model_dump(mode='json'))
        # with open('test_upsert.json', 'w') as file:
        #     json.dump(piwfha2update.model_dump(mode='json'), file)

        if res.status_code != 200:
            raise RuntimeError(f"Could not save data:\nError {res.status_code}: {res.text}")
        res_content = json.loads(res.content)
        if res_content['error'] is not None:
            raise RuntimeError(res_content['error'])
        if res_content['del_res'] is not None:
            print(f"{len(res_content['del_res'])} were deleted")
        print(f"{len(res_content['upsert_res'])} were upserted")
        print(f"{res_content['upsert_res']}")


    def get_devices(self, filters: Optional[Filter] = None):

        api_filter = self.filter2birdoofilter(filters)
        api_filters = api_filter.__dict__
        api_filters.setdefault("refresh", True)
        api_filters = {'filters': api_filters}

        res = self.perform_post_request(url=self.devices_endpoint,
                                        params=api_filters)

        output_data = res.json()
        df = pd.DataFrame(output_data).reset_index()
        df.rename(columns={"client_name": "client",
                           "farm_name": "farm",
                           "house_name": "house",
                           "device_code": "device",
                           "cycle_house_name": "cycle"}, inplace=True)
        return df

