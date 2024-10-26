import logging
import time
from functools import lru_cache

import pandas as pd
import requests
from brddb.connection import BrddbApiConnection, brddbapi
from brddb.credentials import BrddbApiCredentials

from bdm2.utils.schemas.models.storages.brddbapi_client import brddb_api_settings



logger = logging.getLogger("brddb_client")


class BrddbApiClient:

    def __init__(
        self,
        login: str = brddb_api_settings.O_USERNAME,
        password: str = brddb_api_settings.PASSWORD,
        grant_type: str = "password",
    ):
        self.access_token = None
        self.login = login
        self.password = password
        self.grant_type = grant_type

        self.url = brddb_api_settings.URL

    @property
    def header(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_token(self):
        _data = {
            "username": self.login,
            "password": self.password,
            "grant_type": self.grant_type,
        }
        token_response = requests.post(
            # self.url + "token",
            self.url + "/token",
            data=_data,
        )
        if token_response.status_code == 200:
            self.access_token = token_response.json()["access_token"]
            return True
        elif token_response.status_code == 401:
            logger.critical(
                "Problem with authorization to Brddb API. Status code: 401.  Message from brddb: %s",
                token_response.text,
            )
        else:
            logger.critical(
                "Problem with connection to Brddb API. Status code: %s. Message from brddb: %s",
                token_response.status_code,
                token_response.text,
            )
        return False

    def _auth(func):
        def wrapper(self, *args, **kwargs):
            if self.access_token is None:
                self.get_token()
            for iteration in range(100):
                response = func(self, *args, **kwargs)
                logger.debug(
                    f"get {response.status_code} from with message {response.text}",
                )
                if response.status_code == 200:
                    break
                elif response.status_code == 403 or 401:
                    self.get_token()
                    continue
                elif response.status_code != 200:
                    time.sleep(1)
            if response.status_code != 200:
                logger.critical(
                    "Problem with connection to Brddb API. Status code: %s. Message from brddb: %s",
                    response.status_code,
                    response.text,
                )
                raise ValueError("Problem with connection to Brddb API")
            return pd.DataFrame(response.json())

        return wrapper

    def _request(self, method, url, **kwargs):
        response = method(url, **kwargs, headers=self._update_token())
        if response.status_code != 200:
            logger.critical(
                "Problem with connection to Brddb API url: '%s'. Status code: %s. Message from brddb: %s",
                url,
                response.status_code,
                response.text,
            )
        return response
    def _update_token(self):
        """
        Update toking for performing requests to API
        :return:
        """
        creds_path = r"E:\PAWLIN\PRJ\MHDR_CHICKEN\development\birdoo-data-manager\DataBase\entities\nastya_user.yaml"
        self.credentials: BrddbApiCredentials = brddbapi.load_brddbapi_credentials(creds_path)
        form_data = BrddbApiConnection.get_form_data(self.credentials)
        token_url = BrddbApiConnection.get_token_url(self.credentials)
        request = requests.post(url=token_url, data=form_data)
        resp = request.json()
        token = resp['access_token']
        return  {
            'Authorization': f"Bearer {token}"
        }
    def _get(self, url, **kwargs):
        return self._request(method=requests.get, url=url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request(method=requests.post, url=url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request(method=requests.patch, url=url, **kwargs)

    @lru_cache(maxsize=1)
    @_auth
    def get_actual_client_info(self):
        return self._get(self.url + "/api/v1/tables/actual-clients-info")

    @lru_cache(maxsize=1)
    @_auth
    def get_weights_soyrces(self):
        return self._get(self.url + "/api/v1/tables/actual-clients-info")

    @lru_cache(maxsize=1)
    @_auth
    def get_cycle_houses(self):
        return self._get(self.url + "/api/v1/weights/extended_info_about_cycle_houses")

    @lru_cache(maxsize=1)
    @_auth
    def get_breed_types(self):
        return self._get(self.url + "/api/v1/tables/breed-types")

    @lru_cache(maxsize=1)
    @_auth
    def get_genders(self):
        return self._get(self.url + "/api/v1/tables/genders")

    @lru_cache(maxsize=1)
    @_auth
    def get_engine_configs(self):
        return self._get(self.url + "/api/v1/tables/engine_configs")

    @_auth
    def get_houses_view(self):
        return self._get(self.url + "/api/v1/views/houses-view")

    @_auth
    def get_houses_table(self):
        return self._get(self.url + "/api/v1/tables/houses")

    @_auth
    def get_cycle_houses_table(self):
        return self._get(self.url + "/api/v1/tables/cycle_houses")

    @_auth
    def get_farms_table(self):
        return self._get(self.url + "/api/v1/tables/farms")

    @lru_cache(maxsize=1)
    @_auth
    def get_device_view(self) -> pd.DataFrame:
        return self._get(self.url + "/api/v1/views/devices-view")

    @lru_cache(maxsize=2)
    @_auth
    def get_actual_targets_by_src_types(self, src_type: str) -> pd.DataFrame:
        return self._get(
            self.url + "/api/v1/weights/target-weights",
            params={"src_type": src_type},
        )

    @lru_cache(maxsize=1)
    def get_for_postgres_aci_storage(self):
        # Get data from brddb_api
        genders_list = self.get_genders()
        ch_info = self.get_cycle_houses()
        all_aci = self.get_actual_client_info()
        engine_info = self.get_engine_configs()
        breed_types_list = self.get_breed_types()
        genders_list.rename(columns={"id": "gender_id", "name": "gender"}, inplace=True)
        genders_list = genders_list[["gender", "gender_id"]]
        breed_types_list.rename(
            columns={"id": "breed_type_id", "name": "breed_type"},
            inplace=True,
        )
        breed_types_list = breed_types_list[["breed_type", "breed_type_id"]]
        cbg_info = pd.DataFrame(
            ch_info.groupby(
                ["client_id", "breed_type", "gender"],
                as_index=False,
            ).first(),
        )
        cbg_info = cbg_info[
            [
                "client_id",
                "client_name",
                "breed_type",
                "gender",
                "actual_chicken_weights_postfix",
                "actual_chicken_weights_source_id",
            ]
        ]
        all_aci = all_aci[
            [
                "client_id",
                "standard_weights",
                "statistics",
                "breed_type_id",
                "gender_id",
                "piwfha_weights_src_id",
                "likely_target_weights_src_id",
                "engine_config_id",
            ]
        ]
        engine_info = engine_info[["id", "name", "results_postfix"]]
        engine_info.rename(
            columns={"id": "engine_config_id", "name": "engine"},
            inplace=True,
        )

        merged_data = pd.merge(all_aci, genders_list, on=["gender_id"])
        merged_data = pd.merge(merged_data, breed_types_list, on=["breed_type_id"])
        merged_data = pd.merge(
            merged_data,
            cbg_info,
            on=["client_id", "breed_type", "gender"],
        )
        merged_data = pd.merge(merged_data, engine_info, on="engine_config_id")
        # column_names = TargetWeightsColumnsNew()
        merged_data.rename(
            columns={
                "client_name": "client",
                "actual_chicken_weights_source_id": "target_weights_src_id",
                "actual_chicken_weights_postfix": "target_weights_postfix",
                "likely_target_weights_src_id": "likely_target_weights_src_id",
                "piwfha_weights_src_id": "piwfha_weights_src_id",
            },
            inplace=True,
        )
        return merged_data


brddb_client = BrddbApiClient()
