#  Copyright (c) Anna Sosnovskaya

import datetime
import numbers
import os
import random
import warnings
from typing import List

import numpy as np
import pandas as pd
from loguru import logger

from bdm2.constants.global_setup.data import (
    device_match_columns,
    standards_match_columns,
)
from bdm2.constants.global_setup.encoders import GenderEncoder, BreedTypeEncoder
from bdm2.utils.process_data_tools.components.engine.engine_sessions_utils import (
    get_age_from_sess_folder,
)


class Filter:
    """
    Class for managing/filtering differing data instances
    Can be used for choosing only required clients/farms/houses/etc

    :param clients: head of hierarchy
    :param farms: one client has many farms in different countries
    :param houses: many houses in each farm
    :param devices: many devices in each houses
    :param cycles: each house perform chickens with some time period
    :param flocks: structure that defines chickens from the same parents
    :param breed_types: chickens breed (Ross, Cobb, etc.)
    :param genders: male, female, mix

    Also, can be used for results processing

    :param ages: chicken's ages during cycle
    :param start_time: used for filtering engine results by time
    :param end_time: used for filtering engine results by time
    :param nMax: not used

    """

    def __init__(
            self,
            clients: List[str] = None,
            farms: List[str] = None,
            cycles: List[str] = None,
            flocks: List[str] = None,
            houses: List[str] = None,
            devices: List[str] = None,
            ages: List[int] = None,
            start_time: datetime.datetime = None,
            end_time: datetime.datetime = None,
            genders: List[str] = None,
            breed_types: List[str] = None,
            nMax: int = -1,
    ):

        self.clients: List[str] = []
        self.farms: List[str] = []
        self.cycles: List[str] = []
        self.flocks: List[str] = []  # will be deprecated
        self.houses: List[str] = []
        self.devices: List[str] = []
        self.genders: List[str] = []
        self.breed_types: List[str] = []
        self.ages: List[str] = []

        if clients is not None:
            self.clients: List[str] = clients
        if farms is not None:
            self.farms: List[str] = farms
        if cycles is not None:
            self.cycles: List[str] = cycles
        if flocks is not None:
            self.flocks: List[str] = flocks
        if houses is not None:
            self.houses: List[str] = houses
        if devices is not None:
            self.devices: List[str] = devices

        if genders is not None:
            for gender in genders:
                if gender in GenderEncoder.gender_encoder.keys():
                    self.genders.append(gender)
                else:
                    warnings.warn(
                        f"gender value is not in gender_encoder: {gender}, gender will not be added as filter"
                    )

        if breed_types is not None:
            for breed_type in breed_types:
                if breed_type in BreedTypeEncoder.breed_type_encoder.keys():
                    self.breed_types.append(breed_type)
                else:
                    warnings.warn(
                        f"breed_type is not in breed_type_encoder: {breed_type}, breed type will not be added as filter"
                    )

        if ages is not None:
            try:
                if isinstance(ages, str):
                    ages_params = list(map(int, ages.split("-")))
                    self.ages: List[int] = list(np.arange(*ages_params))
                else:
                    self.ages: List[int] = ages
            except Exception as e:
                logger.info(e)

        if type(start_time) == str:
            start_time = datetime.datetime.strptime(start_time, "%H-%M-%S")
        self.start_time: datetime.datetime = start_time

        if type(end_time) == str:
            end_time = datetime.datetime.strptime(end_time, "%H-%M-%S")
        self.end_time: datetime.datetime = end_time

        self.nMax: int = nMax

    @staticmethod
    def check_types(values, type_val):
        for value in values:
            assert type(value) == type_val

    # todo  maybe use self.str() ?
    def __str__(self):
        return (
            f"Birdoo device filter:\n"
            f"   clients: {self.clients}\n"
            f"   farms: {self.farms}\n"
            f"   cycles: {self.cycles}\n"
            f"   flocks: {self.flocks}\n"
            f"   houses: {self.houses}\n"
            f"   devices: {self.devices}\n"
            f"   genders: {self.genders}\n"
            f"   breed_types: {self.breed_types}\n"
            f"   ages: {self.ages}"
        )

    # todo сделать инверт для фильров
    #
    def __invert__(self, *args, **kwargs):  # real signature unknown
        """~self"""
        pass

    def isempty(self) -> bool:
        if len(self.clients) > 0:
            return False
        if len(self.farms) > 0:
            return False
        if len(self.cycles) > 0:
            return False
        if len(self.flocks) > 0:
            return False
        if len(self.houses) > 0:
            return False
        if len(self.devices) > 0:
            return False
        if len(self.genders) > 0:
            return False
        if len(self.breed_types) > 0:
            return False
        if len(self.ages) > 0:
            return False
        if self.start_time is not None:
            return False
        if self.end_time is not None:
            return False
        return True

    # ===========================================
    # PRINTING
    # ===========================================
    def str(self) -> str:
        output = ""
        if len(self.clients) != 0:
            output += "clients: {}\n".format(", ".join(self.clients))
        if len(self.farms) != 0:
            output += "farms: {}\n".format(", ".join(self.farms))
        if len(self.cycles) != 0:
            output += "cycles: {}\n".format(", ".join(self.cycles))

        #     TODO: CHECK. as flock deprecated
        # if len(self.flocks) != 0:
        #     output += "flocks: {}\n".format(", ".join(self.flocks))

        if len(self.houses) != 0:
            output += "houses: {}\n".format(", ".join(self.houses))
        if len(self.devices) != 0:
            output += "devices: {}\n".format(", ".join(self.devices))
        if len(self.genders) != 0:
            output += "genders: {}\n".format(", ".join(list(map(str, self.genders))))
        if len(self.breed_types) != 0:
            output += "breed_types: {}\n".format(
                ", ".join(list(map(str, self.breed_types)))
            )
        if len(self.ages) != 0:
            output += "ages: {}\n".format(", ".join(list(map(str, self.ages))))
        if self.start_time is not None:
            output += "start_time: {}\n".format(self.start_time.time())
        if self.end_time is not None:
            output += "end_time: {}\n".format(self.end_time.time())
        output = output[:-1]
        return output

    def to_dict(self):
        return_dict = {}

        if len(self.clients) != 0:
            return_dict["clients"] = self.clients
        if len(self.farms) != 0:
            return_dict["farms"] = self.farms
        if len(self.cycles) != 0:
            return_dict["cycles"] = self.cycles
        if len(self.houses) != 0:
            return_dict["houses"] = self.houses
        if len(self.devices) != 0:
            return_dict["devices"] = self.devices
        if len(self.genders) != 0:
            return_dict["genders"] = self.genders
        if len(self.breed_types) != 0:
            return_dict["breed_types"] = self.breed_types
        if len(self.ages) != 0:
            return_dict["ages"] = self.ages
        if self.start_time is not None:
            return_dict["start_time"] = self.start_time.strftime("%H-%M-%S")
        if self.end_time is not None:
            return_dict["end_time"] = self.end_time.strftime("%H-%M-%S")

        return return_dict

    def print(self):
        """
        logger.info filter parameters

        :return: None
        """
        logger.info(self.str())

    def generate_label(
            self,
            client: bool = False,
            farm: bool = True,
            cycle: bool = True,
            flock: bool = True,
            house: bool = True,
            device: bool = True,
            gender: bool = False,
            breed_type: bool = False,
    ):
        """
        Generate label from filter parameters.
        If any of parameters are not set, does not include it in label

        :param farm: True to include in label
        :param cycle: True to include in label
        :param flock: True to include in label
        :param house: True to include in label
        :param device: True to include in label
        :param gender: True to include in label
        :param breed_type: True to include in label
        :return: str
        """
        label = ""
        if len(self.clients) != 0 and client:
            label += "_".join([str(x) for x in self.clients])
        if len(self.farms) != 0 and farm:
            label += "_".join([str(x) for x in self.farms])
        if len(self.genders) != 0 and gender:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.genders])
        if len(self.breed_types) != 0 and breed_type:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.breed_types])
        if len(self.cycles) != 0 and cycle:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.cycles])
        if len(self.flocks) != 0 and flock:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.flocks])
        if len(self.houses) != 0 and house:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.houses])
        if len(self.devices) != 0 and device:
            if label != "":
                label += "_"
            label += "_".join([str(x) for x in self.devices])

        label = label.replace(" ", "")
        if label == "":
            return "full"
        else:
            return label

    # ===========================================
    # STORING. DUMPING. LOADING
    # ===========================================

    def load_from_file(self, filename: str):
        """
        Read filter from filename.

        :param filename: path to filter filename
        :return: None
        """
        if not os.path.exists(filename):
            return False
        with open(filename, "r") as f:
            while True:
                line = f.readline()  # end of file is reached
                if not line:
                    break
                try:
                    name, values = line.split(": ")
                    if values.endswith("\n"):
                        values = values[:-1]
                    if name == "clients":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.clients = values_t
                        continue
                    if name == "farms":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.farms = values_t
                        continue
                    if name == "cycles":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.cycles = values.split(",")
                        continue
                    # TODO: DEPRECATED.. CHECKING
                    # if name == "flocks":
                    #     values_t = values.split(",")
                    #     if not (len(values_t) == 1 and values_t[0] == ""):
                    #         self.flocks = values.split(",")
                    #     continue
                    if name == "houses":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.houses = values.split(",")
                        continue
                    if name == "devices":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.devices = values.split(",")
                        continue

                    if name == "genders":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.genders = values.split(",")
                        continue
                    if name == "breed_types":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.breed_types = values.split(",")
                        continue

                    if name == "ages":
                        values_t = values.split(",")
                        if not (len(values_t) == 1 and values_t[0] == ""):
                            self.ages = [int(x) for x in values.split(",")]
                        continue
                    if name == "start_time":
                        if ":" in values:
                            self.start_time = datetime.datetime.strptime(
                                values, "%H:%M:%S"
                            )
                        elif "-" in values:
                            self.start_time = datetime.datetime.strptime(
                                values, "%H-%M-%S"
                            )
                        continue
                    if name == "end_time":
                        if ":" in values:
                            self.end_time = datetime.datetime.strptime(
                                values, "%H:%M:%S"
                            )
                        elif "-" in values:
                            self.end_time = datetime.datetime.strptime(
                                values, "%H-%M-%S"
                            )
                        continue
                except:
                    pass
        return True

    def dump_to_file(self, filename: str):
        output = open(filename, "w")
        output.write(self.str())
        output.close()

    # =======================================
    # CHECKING FUNCTIONS
    # =======================================

    def check_device(self, device: pd.Series) -> bool:
        """
        Check if device fit Filter

        :param device:
        :return: True if device fit Filter
        """
        if not isinstance(device, pd.Series):
            return False
        # if it's series
        if len(device.dropna()) == 0:
            warnings.warn(
                f"Got empty device containing NaN's: {device}; returning False"
            )
            return False
        try:

            if "gender" in device.index and (len(self.genders) > 0):
                # if "client" in device.index and pd.isnull(device.client):
                #     return False
                if isinstance(device.gender, str):
                    # if gender is as str
                    if (device.gender not in self.genders) and (len(self.genders) != 0):
                        return False
                elif isinstance(device.gender, numbers.Number) and not pd.isnull(
                        device.gender
                ):
                    # if gender is as int code
                    if (
                            GenderEncoder.gender_decoder(gender_code=device.gender)
                            not in self.genders
                    ):
                        return False

            if "breed_type" in device.index and (len(self.breed_types) > 0):
                # if "client" in device.index and pd.isnull(device.client):
                #     return False
                if isinstance(device.breed_type, str):
                    # if breed_type is as str
                    if (device.breed_type not in self.breed_types) and (
                            len(self.breed_types) != 0
                    ):
                        return False
                elif isinstance(device.breed_type, numbers.Number) and not pd.isnull(
                        device.breed_type
                ):
                    # if breed_type is as int code
                    if (
                            BreedTypeEncoder.breed_type_decoder(
                                breed_type_code=device.breed_type
                            )
                            not in self.breed_types
                    ):
                        return False
            if "client" in device.index and (len(self.clients) != 0):
                if pd.isnull(device.client) or (device.client is None):
                    return False
                if device.client.replace(" ", "") not in [
                    x.replace(" ", "") for x in self.clients
                ]:
                    return False
            if "farm" in device.index and (len(self.farms) != 0):
                if pd.isnull(device.farm) or (device.farm is None):
                    return False
                if device.farm.replace(" ", "") not in [
                    x.replace(" ", "") for x in self.farms
                ]:
                    return False

            if "cycle" in device.index and (len(self.cycles) != 0):
                if pd.isnull(device.cycle) or (device.cycle is None):
                    return False
                if device.cycle.replace(" ", "") not in [
                    x.replace(" ", "") for x in self.cycles
                ]:
                    return False

            if "house" in device.index and (len(self.houses) != 0):
                if pd.isnull(device.house) or (device.house is None):
                    return False
                if device.house.replace(" ", "") not in [
                    x.replace(" ", "") for x in self.houses
                ]:
                    return False

            if "device" in device.index and (len(self.devices) != 0):
                if pd.isnull(device.device) or (device.device is None):
                    return False
                if device.device.replace(" ", "") not in [
                    x.replace(" ", "") for x in self.devices
                ]:
                    return False

            return True
        except Exception as e:
            logger.info(str(e))
            device_indexes = [
                device[ind] for ind in device_match_columns if ind in device.index
            ]
            if len(device_indexes) > 0:
                device_id = "_".join(device_indexes)
                logger.info(f"{device_id} has problems with filtering")
            else:
                logger.info(
                    f"UNKNOWN device has now any of this fields: [farm,cycle,flock,house,device]"
                )
            return False

    def check_sess(self, sess: str) -> bool:
        """
        Check if sess folder fit Filter

        :param sess: full path or name of session folder with format output_%y_%m_%d_%H_%M_%S
        :return: True if sess fit Filter
        """
        age = get_age_from_sess_folder(sess)
        if age < 0:
            logger.info(f"Could not define age for {sess}")
            return False
        if not self.check_age(age):
            return False
        if not self.check_time_from_sess(sess):
            return False
        return True

    def check_time_from_sess(self, sess: str) -> bool:
        """
        Checking timestamp of sessname.

        :param sess: name of session folder with format output_%y_%m_%d_%H_%M_%S
        :return: True if time of sess suits Filter
        """
        # if sess is full path
        sess_basename = os.path.basename(sess)
        date_format = "output_%y_%m_%d_%H_%M_%S"
        _, _, _, _, h, m, s = sess_basename.split("_")[: len(date_format.split("_"))]
        return self.check_time("-".join([h, m, s]))

    def check_age(self, age: int) -> bool:
        """
        Check if age suits Filter

        :param age: int
        :return: True if age suits Filter
        """
        if len(self.ages) == 0:
            return True
        if age not in self.ages:
            return False
        return True

    def check_time(self, strTime: str, format: str = "%H-%M-%S") -> bool:
        """
        Check if time suits Filter

        :param strTime: time string
        :param format: correspondent string time format
        :return: True if time suits Filter
        """
        try:
            t = datetime.datetime.strptime(strTime, format)
            if self.start_time is not None and self.end_time is not None:
                if self.start_time.time() < self.end_time.time():
                    if t.time() < self.start_time.time():
                        return False
                    if t.time() > self.end_time.time():
                        return False
                else:
                    logger.info("WARNING start time is more then end time")
                    return True
            elif self.start_time is not None:
                if t.time() < self.start_time.time():
                    return False
            elif self.end_time is not None:
                if t.time() > self.end_time.time():
                    return False
        except:
            logger.info(f"Could not check time for  {strTime}")
            return False
        return True

    # =======================================
    # FILTERING FUNCTIONS
    # =======================================

    def filter_devices(
            self, devices: pd.DataFrame, by_groups: bool = False
    ) -> pd.DataFrame:
        """
        Return devices, that match filters only

        :param devices: pd.Dataframe with any of device_match_columns + standards_match_columns
            (not strict. will be filtered only by available columns)
        :param by_groups: if True, process by groups
            useful, if devices has a lot of duplicates by device_match_columns + standards_match_columns
        :return:
        """
        devices_output = devices.iloc[:0].copy()
        if by_groups:
            device_cols = device_match_columns + standards_match_columns
            union_cols = [c for c in device_cols if c in devices.columns]
            for device_l, device_gr in devices.groupby(union_cols):
                device = pd.Series(device_l, index=union_cols)
                if self.check_device(device):
                    devices_output = pd.concat([devices_output, device_gr])
        else:
            for _, device in devices.iterrows():
                if self.check_device(device):
                    devices_output.loc[len(devices_output), device.index] = (
                        device.copy()
                    )

        if not devices_output.empty:
            devices_output = devices_output[devices.columns]
            devices_output = devices_output.reset_index(drop=True)
        return devices_output

    def filter_res_df_csv(self, res_df: pd.DataFrame, age_col="age") -> pd.DataFrame:
        if res_df.empty:
            return res_df
        index_names = res_df.index.names
        index_names = [c for c in index_names if c is not None]
        device_columns = [
            "client",
            "farm",
            "cycle",
            "flock",
            "house",
            "device",
            "gender",
            "breed_type",
        ]
        device_columns = [
            col
            for col in device_columns
            if col in res_df.reset_index().columns
               and not all(res_df.reset_index()[col].isna())
        ]

        res_df_to_iter = res_df.copy()
        if len(index_names) > 0:
            res_df_to_iter = res_df_to_iter.reset_index()

        devices_output = res_df_to_iter.iloc[:0]
        if len(device_columns):
            for d, group in res_df_to_iter.groupby(device_columns, dropna=False):
                try:
                    device = pd.Series(list(d), index=device_columns)
                except:
                    logger.info(
                        "res_df_csv does not contains any of these columns: {}".format(
                            device_columns
                        )
                    )
                    continue
                if self.check_device(device):
                    # devices_output = devices_output.append(group, ignore_index=True)
                    devices_output = pd.concat(
                        [devices_output, group],
                        # ignore_index=True
                    )
        else:
            devices_output = res_df_to_iter.copy()

        devices_output.sort_index(inplace=True)

        if devices_output.empty:
            return devices_output
        if age_col in devices_output.columns:
            devices_output["age_is_ok"] = devices_output[age_col].apply(self.check_age)
            devices_output = devices_output.loc[devices_output["age_is_ok"]]
            devices_output = devices_output.drop("age_is_ok", axis=1)
        if len(index_names) > 0:
            devices_output = devices_output.set_index(index_names)
        return devices_output

    def filter_birdoo_devices_matching(self, birdoo_devices_matching) -> pd.DataFrame:
        devices_output = pd.DataFrame()
        farm_match = {"CP": "Thailand", "CN": "Cargill-NG", "JP": "Japan", "BTG": "BTG"}
        self_houses_ids = [int(x.split(" ")[-1]) for x in self.houses]
        for _, device in birdoo_devices_matching.iterrows():
            if device["Client"] in list(farm_match.keys()):
                birdoo_farm = farm_match[device["Client"]]
            else:
                birdoo_farm = device["Client"]
            if (device["Knex Id"] not in self.devices) and len(self.devices) != 0:
                continue
            elif (device["House"] not in self_houses_ids) and len(self.houses) != 0:
                continue
            elif (birdoo_farm not in self.farms) and len(self.farms) != 0:
                continue
            else:
                # devices_output = devices_output.append(device)
                devices_output.loc[len(devices_output), device.index] = device.copy()
        return devices_output

    # ===========================================
    # OPERATIONS
    # ===========================================
    def get_filter_by_name(self, name: str):
        """
        Return list of specified filter parameter

        :param name:
        :return: list
        """
        if name == "client":
            return self.farms
        if name == "farm":
            return self.farms
        if name == "cycle":
            return self.cycles
        if name == "flock":
            return self.flocks
        if name == "house":
            return self.houses
        if name == "device":
            return self.devices
        if name == "gender":
            return self.genders
        if name == "breed_type":
            return self.breed_types
        raise NameError("No such parameter of filter as {}".format(name))

    def exclude_from_devices(self, devices: pd.DataFrame):
        if devices.empty:
            return devices
        index_cols = devices.index.names
        index_names = [c for c in index_cols if c is not None]
        if len(index_names):
            devices = devices.reset_index()
        devices_output = devices.iloc[:0].copy()
        for _, device in devices.iterrows():
            if not self.check_device(device):
                devices_output.loc[len(devices_output), device.index] = device.copy()

        if len(index_names) > 0:
            devices_output = devices_output.set_index(index_names)
        return devices_output

    @staticmethod
    def get_device_pattern():
        """
        Get device pattern to fill

        :return: pd.Series of device pattern
        """
        output = pd.Series()
        for atr in device_match_columns:
            output[atr] = ""
        return output

    def get_sublist(self, mylist):
        """
        Return random subsample with length self.nMax

        :param mylist: full data
        :return: shuffled random sublist
        """
        if self.nMax < 0:
            return mylist
        if len(mylist) < self.nMax:
            return mylist
        return random.sample(mylist, self.nMax)


class FilterChild(Filter):
    def __init__(
            self,
            clients: List[str] = None,
            farms: List[str] = None,
            cycles: List[str] = None,
            flocks: List[str] = None,
            houses: List[str] = None,
            devices: List[str] = None,
            ages: List[int] = None,
            start_time: datetime.datetime = None,
            end_time: datetime.datetime = None,
            genders: List[str] = None,
            breed_types: List[str] = None,
            kwargs=None,
    ):

        super().__init__(
            clients,
            farms,
            cycles,
            flocks,
            houses,
            devices,
            ages,
            start_time,
            end_time,
            genders,
            breed_types,
        )
        self.farms: List[str] = []
        self.cycles: List[str] = []
        self.flocks: List[str] = []
        self.houses: List[str] = []
        self.devices: List[str] = []
        self.genders: List[str] = []
        self.breed_types: List[str] = []
        self.ages: List[str] = []

        if not kwargs:
            kwargs = dict()

        self.clients: List[str] = clients or kwargs.get("clients", [])
        self.farms: List[str] = farms or kwargs.get("farms", [])
        self.cycles: List[str] = cycles or kwargs.get("cycles", [])
        self.flocks: List[str] = flocks or kwargs.get("flocks", [])
        self.houses: List[str] = houses or kwargs.get("houses", [])
        self.devices: List[str] = devices or kwargs.get("devices", [])

        # self.genders = genders or kwargs.get("genders")
        # self.breed_types = breed_types or kwargs.get("breed_types")
        genders = genders or kwargs.get("genders")
        if genders:
            for gender in genders:
                if gender in GenderEncoder.gender_encoder.keys():
                    self.genders.append(gender)
                else:
                    self.genders.append("")
                    logger.error(f"Incorrect gender value be carefull: {gender}")

        breed_types = breed_types or kwargs.get("breed_types")
        if breed_types:
            for breed_type in breed_types:
                if breed_type in BreedTypeEncoder.breed_type_encoder.keys():
                    self.breed_types.append(breed_type)
                else:
                    self.breed_types.append("")
                    logger.error(f"Incorrect breed_type value: {breed_type}")

        self.ages = ages or kwargs.get("ages", [])
        if self.ages is not None:
            try:
                if isinstance(self.ages, str):
                    ages_params = list(map(int, self.ages.split("-")))
                    self.ages: List[int] = list(np.arange(*ages_params))
                else:
                    self.ages: List[int] = self.ages
            except Exception as e:
                logger.info(e)
        # additional check when init from dataclass
        if kwargs.get("start_time") == "":
            kwargs.pop("start_time")

        if kwargs.get("end_time") == "":
            kwargs.pop("end_time")

        start_time = start_time or kwargs.get("start_time")
        if type(start_time) == str:
            start_time = datetime.datetime.strptime(start_time, "%H-%M-%S")

        self.start_time: datetime.datetime = start_time

        end_time = end_time or kwargs.get("end_time")
        if type(end_time) == str:
            end_time = datetime.datetime.strptime(end_time, "%H-%M-%S")

        self.end_time: datetime.datetime = end_time
        self.nMax: int = -1

        self.check_types(
            [
                self.clients,
                self.farms,
                self.cycles,
                self.flocks,
                self.houses,
                self.devices,
                self.genders,
                self.breed_types,
                self.ages,
            ],
            list,
        )


def init_filter_from_devices(
        devices: pd.DataFrame, age_column: str = "daynum"
) -> Filter:
    """
    INit filter from devices pd.DataFrame

    :param devices:
    :return:
    """
    output_filter = Filter()

    all_columns = list(output_filter.__dict__.keys())
    union_columns = list(set(devices.columns).intersection(all_columns))
    devices_not_nan = devices.dropna(subset=union_columns)

    if "client" in devices_not_nan.columns:
        output_filter.clients = list(devices_not_nan["client"].dropna().unique())
    if "farm" in devices_not_nan.columns:
        output_filter.farms = list(devices_not_nan["farm"].dropna().unique())
    if "cycle" in devices_not_nan.columns:
        output_filter.cycles = list(devices_not_nan["cycle"].dropna().unique())
    if "house" in devices_not_nan.columns:
        output_filter.houses = list(devices_not_nan["house"].dropna().unique())
    if "device" in devices_not_nan.columns:
        output_filter.devices = list(devices_not_nan["device"].dropna().unique())
    if "gender" in devices_not_nan.columns:
        output_filter.genders = list(devices_not_nan["gender"].dropna().unique())
    if "breed_type" in devices_not_nan.columns:
        output_filter.breed_types = list(
            devices_not_nan["breed_type"].dropna().unique()
        )
    if age_column in devices_not_nan.columns:
        output_filter.ages = list(
            map(int, devices_not_nan[age_column].dropna().unique())
        )
    return output_filter
