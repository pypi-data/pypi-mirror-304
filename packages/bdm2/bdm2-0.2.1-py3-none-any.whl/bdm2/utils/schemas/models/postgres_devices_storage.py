# import datetime
# from abc import abstractmethod
# from typing import Set, Dict, Any, List, Optional
# import pandas as pd
# import copy
# from dataclasses import dataclass, field
#
# from brddb.models.postgres import Devices, CycleHouses, Houses, Farms, Clients
# from sqlalchemy.orm import sessionmaker, Session
#
# # from BIRDOO_IP.colorstr import colorstr
# from src.utils.process_data_tools.components.birdoo_filter import Filter
# from src.utils.schemas.components.columns import DevicesStorageColumnsNew
# from src.utils.schemas.components.get_and_add_methods import upsert_device_info, get_cycle_houses
# from src.utils.schemas.connection import postgres_engine
# from src.utils.schemas.models.postgres_actual_clients_info_storage import get_rename_dict, StorageBase
#
#
# # upsert_device_info
# # Devices
# # DevicesStorage
# # from BIRDOO_IP.storages.devices.devices_storage import DevicesStorage, DevicesStorageColumnsNew
# # from DataBase.SQLAlchemyTables.clients_storage import Devices, CycleHouses, Houses, Farms, Clients
# # from DataBase.SQLAlchemyTables.utils.clients_utils import upsert_device_info, get_cycle_houses
#
#
# class DevicesStorage(StorageBase):
#
#     @property
#     def output_default_format(self) -> DevicesStorageColumnsNew:
#         """"""
#         # DEPRECATED USING INNER FORMAT COLUMNS. TO COMPLEX TO MANAGE WTH
#         #     output = {}
#         #     loc_inner_format = self.inner_format
#         #     for atr in DevicesStorageColumnsNew.__annotations__:
#         #         output[atr] = loc_inner_format.__dict__[atr]
#         #     return DevicesStorageColumnsNew(**output)
#         return DevicesStorageColumnsNew()
#
#     @property
#     def inner_as_default_format(self) -> DevicesStorageColumnsNew:
#         output = {}
#         loc_inner_format = self.inner_format
#         for atr in DevicesStorageColumnsNew.__annotations__:
#             output[atr] = loc_inner_format.__dict__[atr]
#         return DevicesStorageColumnsNew(**output)
#
#     @property
#     @abstractmethod
#     def inner_format(self) -> DevicesStorageColumnsNew:
#         """ """
#
#     def generate_filter_from_df(self, df: pd.DataFrame, df_format: DevicesStorageColumnsNew) -> Filter:
#         output_filter = Filter()
#
#         all_columns = list(output_filter.__dict__.keys())
#         union_columns = list(set(df.columns).intersection(all_columns))
#         df_not_nan = df.dropna(subset=union_columns)
#
#         if df_format.client_name in df_not_nan.columns:
#             output_filter.clients = list(df_not_nan[df_format.client_name].dropna().unique())
#         if df_format.farm_name in df_not_nan.columns:
#             output_filter.farms = list(df_not_nan[df_format.farm_name].dropna().unique())
#         if df_format.cycle_house_name in df_not_nan.columns:
#             output_filter.cycles = list(df_not_nan[df_format.cycle_house_name].dropna().unique())
#         if df_format.house_name in df_not_nan.columns:
#             output_filter.houses = list(df_not_nan[df_format.house_name].dropna().unique())
#         if df_format.device_name in df_not_nan.columns:
#             output_filter.devices = list(df_not_nan[df_format.device_name].dropna().unique())
#         if df_format.gender in df_not_nan.columns:
#             output_filter.genders = list(df_not_nan[df_format.gender].dropna().unique())
#         if df_format.breed_type in df_not_nan.columns:
#             output_filter.breed_types = list(df_not_nan[df_format.breed_type].dropna().unique())
#         return output_filter
#
#     @abstractmethod
#     def convert_to_input_format(self,
#                                 df: pd.DataFrame,
#                                 src_format: DevicesStorageColumnsNew) -> pd.DataFrame:
#         """
#         Convert df with format src_format to input format, All columns of df that are not in src_format will be lost
#
#         :param df:
#         :param src_format:
#         :return: converted df
#         """
#
#     def dropna(self, df: pd.DataFrame, format: DevicesStorageColumnsNew) -> pd.DataFrame:
#         cols_to_check = [c for c in format.device_columns.get_columns() if c in df.columns]
#         return df.dropna(axis=0, how='any', subset=cols_to_check)
#
#     @abstractmethod
#     def get_devices(self,
#                     filters: Filter,
#                     output_format: Optional[DevicesStorageColumnsNew] = None,
#                     dropna: bool = False
#                     ) -> pd.DataFrame:
#         """
#         return df with all unique devices (including cycle and flocks information), that matches filter
#
#         :param filters: filter for specifying devices scope
#         :param output_format: column names of output data
#         :param dropna: drop rows with nan or None values in main device columns
#         :return: devices df with output_format column's names
#         """
#
#     def get_houses(self,
#                    filters: Filter,
#                    output_format: Optional[DevicesStorageColumnsNew] = None
#                    ) -> pd.DataFrame:
#         """
#         return df with all unique houses (including cycle and flocks information), that matches filter
#
#         :param filters: filter for specifying house scope
#         :param output_format: column names of output data
#         :return: devices df with output_format column's names
#         """
#         if output_format is None:
#             output_format = self.output_default_format
#
#         tmp_devices = self.get_devices(filters, output_format)
#         gpby_columns = output_format.house_columns.get_columns() + [output_format.cycle_house_name]
#         houses = tmp_devices.groupby(gpby_columns, as_index=False).first()
#         return houses
#
#     @abstractmethod
#     def delete_devices(self, filters: Filter):
#         """
#         Add new device info to storage
#
#         :param filters: filter for specifying house scope
#         """
#
#     @abstractmethod
#     def update_devices(self,
#                        df: pd.DataFrame,
#                        src_format: DevicesStorageColumnsNew
#                        ):
#         """
#         Update device info to storage.
#
#         :param df: device data to be updated, has to have src_format columns
#         :param src_format: column's names to be used fir updating
#         :return: None
#         """
#
#
#
# @dataclass
# class PostgresDevicesStorageColumnsNew(DevicesStorageColumnsNew):
#     """
#     Postgres' DevicesStorage has extra columns for storing primary keys.
#     columns names are defined from get_cycle_houses(),
#     where query.set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL) is used
#
#     """
#     client_id: str = field(default='clients_id', init=True)
#     farm_id: str = field(default='farms_id', init=True)
#     house_id: str = field(default='houses_id', init=True)
#     device_id: str = field(default='devices_id', init=True)
#     cycle_house_id: str = field(default='cycle_houses_id', init=True)
#     flock_id: str = field(default='flocks_id', init=True)
#
#     def __post_init__(self):
#         self.client_name = 'clients_name'
#         self.client_code = 'clients_code'
#
#         self.farm_name = 'farms_name'
#         self.farm_code = 'farms_code'
#         self.country = 'farms_country'
#
#         self.house_name = 'houses_name'
#         self.house_code = 'houses_code'
#
#         self.device_name = 'devices_name'
#         self.device_code = 'devices_code'
#         self.rel_path = 'cycle_devices_relative_path'
#
#         self.cycle_house_name = 'cycle_houses_name'
#         self.cycle_house_code = 'cycle_houses_code'
#         self.cycle_device_code = 'cycle_devices_code'
#         self.cycle_start_date = 'cycle_houses_cycle_start_date'
#         self.usable_for_train = 'cycle_devices_usable_for_train'
#         self.comment = 'cycle_devices_comment'
#
#         self.flock_name = 'flocks_name'
#         self.gender = 'genders_name'
#         self.breed_type = 'breed_types_name'
#
#
# class PostgresDevicesStorage(DevicesStorage):
#     _instance = None
#     _update_interval = 60  # min
#     _data = None
#     _last_update = None
#     _inner_format: PostgresDevicesStorageColumnsNew = PostgresDevicesStorageColumnsNew()
#
#     def __new__(class_):
#         if not isinstance(class_._instance, class_):
#             class_._instance = object.__new__(class_)
#         return class_._instance
#
#     @property
#     def inner_format(self) -> PostgresDevicesStorageColumnsNew:
#         return PostgresDevicesStorageColumnsNew(**copy.deepcopy(self._inner_format.__dict__))
#
#     def _check_update(self, session: Optional[Session] = None):
#         _need_update = False
#         if self._data is None or self._last_update is None:
#             _need_update = True
#         elif (datetime.datetime.now()-self._last_update).total_seconds()/60 > self._update_interval :
#             _need_update = True
#         if _need_update:
#             need_to_close_sess = False
#             if session is None:
#                 need_to_close_sess=True
#                 session = sessionmaker(bind=postgres_engine)()
#             self.update_df(session)
#             if need_to_close_sess:
#                 session.close()
#
#     def update_df(self, session:Session):
#         _st_dt = datetime.datetime.now()
#         self._data = get_cycle_houses(session, Filter(), add_devices=True)
#         _end_dt = datetime.datetime.now()
#         self._last_update = datetime.datetime.now()
#         logger.info(f'data was updated. It takes: {(_end_dt - _st_dt).total_seconds():.2f} sec')
#
#     def convert_to_input_format(self,
#                                 df: pd.DataFrame,
#                                 src_format: DevicesStorageColumnsNew) -> pd.DataFrame:
#
#         df_output = pd.DataFrame(columns=self._inner_format.get_columns())
#         rename_dict = {}
#         for col1, col2 in zip(src_format.get_columns(), self._inner_format.get_columns()):
#             rename_dict[col1.strip()] = col2.strip()
#         df_slt = df.rename(columns=rename_dict)
#
#         union_columns = list(set(df_slt.columns).intersection(set(df_output.columns)))
#         df_output = pd.concat([df_output.reset_index(drop=True), df_slt[union_columns].reset_index(drop=True)],
#                               axis=0, ignore_index=True)
#         return df_output
#
#     def get_devices(self,
#                     filters: Filter,
#                     output_format: Optional[DevicesStorageColumnsNew] = None,
#                     dropna: bool = False,
#                     session: Optional[Session] = None
#                     ) -> pd.DataFrame:
#
#         if output_format is None:
#             output_format = self.output_default_format
#         self._check_update(session)
#
#         # Convert to default format to let filtration work with it
#         # Loose info about data
#         rename_dict = get_rename_dict(self.inner_format, DevicesStorageColumnsNew())
#         _data = self._data.rename(columns=rename_dict)
#         _data = filters.filter_devices(_data)
#         if len(_data)==0:
#             logger.info(f"No devices after applying filtration")
#         rename_dict = get_rename_dict(DevicesStorageColumnsNew(), self.inner_format)
#         _data = _data.rename(columns=rename_dict)
#
#         if dropna:
#             _data = self.dropna(_data, self.inner_format)
#
#         if output_format is None:
#             df_output = self.convert_formats(_data,
#                                              input_format=self.inner_format,
#                                              output_format=self.output_default_format,
#                                              save_extra_columns=False
#                                              )
#         else:
#             df_output = self.convert_formats(_data,
#                                              input_format=self.inner_format,
#                                              output_format=output_format,
#                                              save_extra_columns=False)
#
#         return df_output
#
#     def delete_devices(self, filters: Filter,
#                        session: Optional[Session] = None,
#                        do_commit: bool = True):
#         need_to_close_sess = False
#         if session is None:
#             session = sessionmaker(bind=postgres_engine)()
#             need_to_close_sess = True
#
#         logger.info(" get devices .. ")
#         # df = get_cycle_houses(self.session, filtration)
#
#         df = self.get_devices(filters, session=session)
#         for df_iter, df_item in df.iterrows():
#             try:
#                 if len(filters.devices) > 0:
#                     device_id = df_item[self._inner_format.device_id]
#                     delete_items_count = session.query(Devices).filter(Devices.id == device_id).delete()
#                     logger.info(f"Delete device_id : {device_id} ({delete_items_count})")
#
#                 if len(filters.cycles) > 0:
#                     cycle_houses_id = df_item[self._inner_format.cycle_house_id]
#                     delete_items_count = session.query(CycleHouses).filter(
#                         CycleHouses.id == cycle_houses_id).delete()
#                     logger.info(f"Delete cycle_houses : {cycle_houses_id} ({delete_items_count})")
#
#                 if len(filters.houses) > 0:
#                     houses_id = df_item[self._inner_format.house_id]
#                     delete_items_count = session.query(Houses).filter(Houses.id == houses_id).delete()
#                     logger.info(f"Delete houses : {houses_id} ({delete_items_count})")
#
#                 elif len(filters.farms) > 0:
#                     farm_id = df_item[self._inner_format.farm_id]
#                     delete_items_count = session.query(Farms).filter(Farms.id == farm_id).delete()
#                     logger.info(f"Delete farm_id : {farm_id} ({delete_items_count})")
#
#                 elif len(filters.clients) > 0:
#                     clients_id = df_item[self._inner_format.client_id]
#                     delete_items_count = session.query(Clients).filter(Clients.id == clients_id).delete()
#                     logger.info(f"Delete clients_id : {clients_id} ({delete_items_count})")
#
#                 else:
#                     clients_id = df_item[self._inner_format.client_id]
#                     delete_items_count = session.query(Clients).filter(Clients.id == clients_id).delete()
#                     logger.info(f"Delete clients_id : {clients_id} ({delete_items_count})")
#
#             except Exception as ex:
#                 logger.info(f"Error then deleting \n"
#                       f"Exception {ex}")
#
#         if need_to_close_sess:
#             session.commit()
#             logger.info("Commit DONE")
#             session.close()
#         elif do_commit:
#             session.commit()
#             logger.info("Commit DONE")
#         logger.info("Deleting End")
#
#     def update_devices(self,
#                        df: pd.DataFrame,
#                        src_format: DevicesStorageColumnsNew,
#                        session: Optional[Session] = None,
#                        do_commit: bool = True
#                        ):
#         need_to_close_sess = False
#         if session is None:
#             session = sessionmaker(bind=postgres_engine)()
#             need_to_close_sess = True
#
#         if type(df) is pd.Series:
#             df = df.to_frame().T
#
#         loc_df = self.convert_to_input_format(df=df, src_format=src_format)
#         log_file = open("broke_upsert.csv", "w")
#         log_file.write("client;farm;house;cycle;flock;device\n")
#         for _, row in loc_df.iterrows():
#             try:
#                 upsert_device_info(session, row, do_commit=do_commit, format=self._inner_format)
#                 logger.info(f"\tDONE")
#             except Exception as ex:
#                 row_text = f"{row[self._inner_format.client_name]};" \
#                            f"{row[self._inner_format.farm_name]};" \
#                            f"{row[self._inner_format.house_name]};" \
#                            f"{row[self._inner_format.cycle_house_name]};" \
#                            f"{row[self._inner_format.flock_name]};" \
#                            f"{row[self._inner_format.device_name]}" \
#                            f"\n"
#                 logger.info("Error then Upsert\n"
#                       f"{ex}\n"
#                       f"{row_text}")
#
#                 log_file.write(f"Problems with {row}")
#         log_file.close()
#         if need_to_close_sess:
#             session.close()
#
#
# if __name__ == '__main__':
#
#
#     filters = Filter(farms=['BTG'], cycles=['Cycle 2'])
#     st = PostgresDevicesStorage()
#     st_format = st.output_default_format
#
#     start_dt = datetime.datetime.now()
#     st.get_devices(filters)
#     end_dt = datetime.datetime.now()
#     logger.info(f'First try takes: {(end_dt - start_dt).total_seconds():.2f} sec')
#
#     start_dt = datetime.datetime.now()
#     devices = st.get_devices(filters)
#     end_dt = datetime.datetime.now()
#     logger.info(f'Second try takes: {(end_dt - start_dt).total_seconds():.2f} sec')
#     logger.info(f"{len(devices)} devices found")
#     pass
