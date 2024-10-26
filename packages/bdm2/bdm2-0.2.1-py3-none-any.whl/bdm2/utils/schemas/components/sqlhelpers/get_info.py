import functools

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
# from DataBase.matching_db import DataBaseConfig
from sqlalchemy.orm import Query, Session

from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.components.sqlhelpers.func_based_wrappers import postgre_wrapper
from bdm2.utils.schemas.components.sqlhelpers.helpers import (compile_query)
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.storages.clients_storage import *


# from DataBase.experiments.config import _mongo_postgre_col_map, _devices_col_map

# from main_config import GlobalConfig
# from BIRDOO_IP import BirdooUtils


# DataBaseConfig
class PostgreClients():
    def __init__(self):
        super().__init__()
        self.database = self.get_cycle_houses(filters=None)
        # Session = sessionmaker(bind=self.postgres_engine)
        # self.session = Session()

    @staticmethod
    def add_filters(query: Query, filters: Filter) -> Query:
        if len(filters.clients):
            query = query.filter(Clients.name.in_(filters.clients))
        if len(filters.farms):
            query = query.filter(Farms.name.in_(filters.farms))
        if len(filters.cycles):
            query = query.filter(CycleHouses.name.in_(filters.cycles))
        if len(filters.houses):
            query = query.filter(Houses.name.in_(filters.houses))
        return query

    @functools.lru_cache()
    @postgre_wrapper(label='==>')  # label='accepting clients ==>'
    def get_clients(self, filters: Filter, session: Session) -> pd.DataFrame:
        """
        Get client information based only on filters.clients
        :param session:
        :param filters:
        :return: pd.DataFrame
        """

        query = session.query(Clients).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).set_label_style(
            LABEL_STYLE_TABLENAME_PLUS_COL)
        if filters:
            query = self.add_filters(query, filters)
        output = pd.read_sql_query(compile_query(query), postgres_engine)
        return output

    @functools.lru_cache()
    @postgre_wrapper(label='==>')  # label='accepting clients ==>'
    def get_farms(self, filters: Filter, session: Session) -> pd.DataFrame:
        """
        Get client, farm information based only on filters.clients, filters.farms
        :param session:
        :param filters:
        :return: pd.DataFrame
        """
        query = session.query(Clients, Farms).join(
            Farms, Farms.client_id == Clients.id, full=True).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
        if filters is not None:
            query = self.add_filters(query, filters)
        output = pd.read_sql_query(compile_query(query), postgres_engine.connect())
        return output

    @functools.lru_cache()
    @postgre_wrapper(label='==>')  # label='accepting clients ==>'
    def get_houses(self, filters: Filter, session: Session) -> pd.DataFrame:
        """
        Get client, farm, house information based only on filters.clients, filters.farms , filters.houses
        :param session:
        :param filters:
        :return: pd.DataFrame
        """
        query = session.query(Clients, Farms, Houses).join(
            Farms, Farms.client_id == Clients.id, full=True).join(
            Houses, Houses.farm_id == Farms.id, full=True).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
        if filters is not None:
            query = self.add_filters(query, filters)
        output = pd.read_sql_query(compile_query(query), postgres_engine)
        return output

    @functools.lru_cache()
    @postgre_wrapper(label='==>')
    def get_cycle_houses(self, filters: Filter, session: Session) -> pd.DataFrame:
        """
        Get client, farm, house, cycle_house information based only on filters.clients, filters.farms , filters.houses, filters.cycle
        :param session:
        :param filters:
        :return: pd.DataFrame
        """
        query = session.query(Clients, Farms, Houses, CycleHouses).join(
            Farms, Farms.client_id == Clients.id, full=True).join(
            Houses, Houses.farm_id == Farms.id, full=True).join(
            CycleHouses, CycleHouses.house_id == Houses.id, full=True).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
        if filters:
            query = self.add_filters(query, filters)

        output = pd.read_sql_query(compile_query(query), postgres_engine.connect())
        return output

    @functools.lru_cache()
    @postgre_wrapper(label='==>')
    def get_cycle_house_id(self, farm, house, cycle, session: Session):
        query = session.query(CycleHouses.id).join(
            Houses, CycleHouses.house_id == Houses.id).join(
            Farms, Houses.farm_id == Farms.id
        )
        query = query.filter(Farms.name == farm).filter(Houses.name == house).filter(CycleHouses.name == cycle)
        ch_id = query.scalar()
        return ch_id

# class MongoClients(DataBaseConfig):
#     def __init__(self):
#         super().__init__()
#         self.database = self.read_mongo()
#         # devices_with_paths.loc[(devices_with_paths[list(cur_filter)] == pd.Series(cur_filter)).all(axis=1), :]
#
#     # @functools.lru_cache()
#     @mongo_wrapper(label='==>')
#     def read_mongo(self, client) -> pd.DataFrame:
#         """
#         Reads both dataframes: cycles and birds
#         NOT Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/
#         """
#         # if you using class_based_wrapper you should have dynamic attribute (which will be deleted later):
#         #   collection = self.dynamic_mongo_client[self.mongo_connection_config.auth_db]
#         # else:
#         collection = client[self.mongo_connection_config.auth_db]
#         farms = collection['farms']
#         cycles = collection['cycles']
#         birds = collection['birds']
#         query = {}
#         cycles_df = pd.DataFrame(list(cycles.find(query)))
#         birds_df = pd.DataFrame(list(birds.find(query)))
#         farms_df = pd.DataFrame(list(farms.find(query)))
#         # set(birds_df.columns).intersection(set(cycles_df.columns))
#         col_to_merge = set(cycles_df.columns).intersection(set(birds_df.columns))
#         # merged = cycles_df.merge(birds_df, on='birdId', how='left')  # cycles_df.merge(birds_df, on='birdId', how='right')
#         birds_df2 = birds_df[['birdId'] + [i for i in birds_df.columns if i not in col_to_merge]]
#         merged = cycles_df.merge(birds_df2, on='birdId', how='left')  # cycles_df.merge(birds_df, on='birdId', how='right')
#         # drop_postfix = '_to_drop'
#         col_to_merge2 = set(merged.columns).intersection(set(farms_df.columns))
#         # merged2 = merged.merge(farms_df, on='farmId', how='left', suffixes=('', drop_postfix)) # suffixes=('_123123', drop_postfix)
#         farms_df2 = farms_df[['farmId'] + [i for i in farms_df.columns if i not in col_to_merge2]]
#         # merged2 = merged.merge(farms_df2, on=list(col_to_merge2), how='left')
#         merged2 = merged.merge(farms_df2, on='farmId', how='left')
#         # col_to_drop = [i for i in merged2 if i.endswith(drop_postfix)]
#         # merged2.drop(columns=[col_to_drop])
#         return merged2
#
#     def some(self):
#         pass
#
#
# class SharedDataBase:
#     def __init__(self, col_to_view: List[str] = None):
#         self.postgre = PostgreClients()
#         self.mongo = MongoClients()
#         self._mongo_postgre_col_map = _mongo_postgre_col_map
#         self._devices_col_map = _devices_col_map
#         self.mongo_db = self.mongo.database.rename(columns=self.mongo_postgre_col_map)
#         self.devices = #BirdooUtils.load_devices_from_csv(GlobalConfig.device_csv)
#         self.level_to_method = {'clients': 'get_clients', 'farms': 'get_farms', 'houses': 'get_houses', 'cycles': 'get_cycle_houses'}
#         self.level_to_device_col = {'clients': 'clients_code', 'farms': 'farms_code', 'houses': 'houses_code', 'cycles': 'cycles_code'}
#         self.devices_additional = ['cycle_start_day', 'cycle_id']
#         if col_to_view is None:
#             self.col_to_view: List[str] = ['clients_name', 'clients_full_name', 'farms_name', 'farms_full_name',
#                               'farms_code', 'farmOwnerName', 'farmName',
#                               'houses_name', 'houses_code', 'cycle_houses_name', 'cycle_houses_code',
#                               'cycle_houses_cycle_start_date',
#                               'breed_type', 'gender', 'mongo_cycle_start_day']
#         else:
#             self.col_to_view = col_to_view
#
#     @property
#     def mongo_postgre_col_map(self):
#         return self._mongo_postgre_col_map
#
#
#     @staticmethod
#     def determine_level(filter: Filter):
#         """
#         Accepts Filter object and determines postgre table with max verbosity;
#         For example, if you have Farm, House you will get houses table, joined with farm
#
#         """
#         level: str = None
#         define_name_later = [len(filter.clients), len(filter.farms), len(filter.houses), len(filter.cycles)]
#         cumsum = np.cumsum(define_name_later)
#
#         if define_name_later[0] > 0:
#             level = 'clients'
#         elif define_name_later[1] > 0:
#             level = 'farms'
#         # then propagate using cumulative sum
#         propagate = cumsum - define_name_later[0]
#         # propagate from the first element since it was farms and then determine later
#         try:
#             result = np.where(propagate[1:] == 0)[0].min()
#         except ValueError:
#             # then it's an empty list (np.array) and you have all filters set
#             result = 3
#         if level is not None:
#             if result == 0:
#                 level = 'clients'
#             elif result == 1:
#                 level = 'farms'
#             elif result == 2:
#                 level = 'houses'
#             else:
#                 level = 'cycles'
#
#         return level
#
#     @staticmethod
#     def col_to_merge(level):
#         col_to_merge = ['clients_code', 'farms_code', 'houses_code', 'cycle_houses_code']
#         if level == 'clients':
#             return col_to_merge[:1]
#         elif level == 'farms':
#             return col_to_merge[:2]
#         elif level == 'houses':
#             return col_to_merge[:3]
#         elif level == 'cycles':
#             return col_to_merge[:4]
#         else:
#             raise NotImplementedError(f"Got unknown level: {level}")
#
#     # def get_devices_start_date(self):
#     #     devices = GlobalConfig.device_csv
#
#     def some(self, filter: Filter, use_local: Optional[bool] = False):
#         level = self.determine_level(filter)
#         if level is None:
#             raise AssertionError(f"Provide filters for at least farms")
#         method_to_use = self.level_to_method[level]
#         method = getattr(self.postgre, method_to_use, None)
#         if method is None:
#             raise SyntaxError(f"Some method you're trying to call does not exist")
#
#         postgre_df = method(filter)
#         # self.postgre.get_cycle_houses(filter)
#         # before merging decide which one you'll be using:
#         current_devices = filter.filter_devices(self.devices)
#         # current_devices[['cycle_houses_code']
#         if use_local:
#             print(colorstr(f'yellow', f"Using local storage due to use_local = {use_local}"))
#             new_filter_clients = list(set(current_devices['client']))
#             new_filter_farms = list(set(current_devices['farm']))
#             new_filter_cycles = list(set(current_devices['cycle']))
#             new_filter_houses = list(set(current_devices['house']))
#             new_filter = Filter(clients=new_filter_clients, farms=new_filter_farms, cycles=new_filter_cycles,
#                                 houses=new_filter_houses)
#             # print(colorstr(f"magenta", f"Using new filters: {new_filter}"))
#             not_dropped_attributes = ['clients', 'farms', 'cycles', 'houses'][::-1]
#             # attr_to_lists: Dict[str, str] = {value[:-1]: value for value in not_dropped_attributes}
#             dropped_attributes: List[str] = []
#             # should_break: bool = False
#             # new_filter = Filter()
#             # for method_name, attr in attr_to_lists:
#             for attr_name in not_dropped_attributes:
#                 # filter_method = getattr(new_filter, attr, None)
#                 # list(set(current_devices[method_name]))
#                 level = self.determine_level(new_filter)
#                 if level is None:
#                     raise AssertionError(f"Provide filters for at least farms")
#                 method_to_use = self.level_to_method[level]
#                 method = getattr(self.postgre, method_to_use, None)
#                 if method is None:
#                     raise SyntaxError(f"Some method you're trying to call does not exist")
#
#                 postgre_df = method(new_filter)
#                 if not postgre_df.empty:
#                     # there's a match
#                     print(colorstr('magenta', f"dropped {', '.join(dropped_attributes)} from filter to " + \
#                                    f"get non-empty postgre df; There probably some mismatch between local and postgre"))
#                     break
#                 else:
#                     setattr(new_filter, attr_name, [])
#                     dropped_attributes.append(attr_name)
#
#             filter = new_filter
#             # self.postgre.get_clients(new_filter)
#         else:
#             # self.postgre.get_clients(filter)
#             pass
#
#         unique_fhc = list(set(current_devices['cycle_id']))
#         col_to_merge = self.col_to_merge(level)
#         if len(col_to_merge) == 1 and col_to_merge == ['clients_code']:
#             col_to_merge = ['farms_code']
#             method_to_use = self.level_to_method['farms']
#             method = getattr(self.postgre, method_to_use, None)
#             if method is None:
#                 raise SyntaxError(f"Some method you're trying to call does not exist")
#
#             postgre_df = method(filter)
#
#         col_intersect = list(set(col_to_merge).intersection(set(self.mongo_db.columns)))
#         if len(col_intersect) != len(col_to_merge):
#             print(colorstr(f"magenta", 'bold', f"some columns do not exist in mongo db: " + \
#                            f"{' ,'.join(list(set(col_to_merge).difference(set(self.mongo_db.columns))))}"))
#
#         merged = postgre_df.merge(self.mongo_db, how='left', on=col_intersect)
#         # add cycle_start_day:
#         # devices[['cycle_houses_code', 'cycle_start_day']]
#         # device_col_to_merge = self.level_to_device_col[level]
#         # devices = self.devices.rename(columns=self._devices_col_map)
#         # devices_cols = ['cycle_houses_code'] + self.devices_additional
#         # result = merged.merge(devices[devices_cols], how='left', on = 'cycle_houses_code')
#         # merged.merge(devices[['cycle_houses_code', 'cycle_start_day']], how='left', on='cycle_houses_code')
#         cols_to_select = [i for i in self.col_to_view if i in merged.columns] # list(set(merged.columns).intersection(set(self.col_to_view)))
#         difference = set(self.col_to_view).difference(set(cols_to_select))
#         if len(difference) > 0:
#             warn_msg = f"There's some columns not existing in merged dataframe: {difference};" + \
#                        f"they will not be used"
#             warnings.warn(colorstr('bright_red', 'bold', warn_msg), category=UserWarning)
#         if 'cycle_houses_code' in merged.columns:
#             returned = merged[merged['cycle_houses_code'].isin(unique_fhc)]
#             print(colorstr('yellow', f"prev len: {len(merged)}; matched by cycle_id: {len(returned)}"))
#             return returned
#         return merged[cols_to_select]
#
# if __name__ == '__main__':
#
#     result_filename = 'result.csv'
#     filter = Filter(farms=['TDIDWD'])
#     use_local: bool = True # use either devices or postgre
#     #   for postgre set to False; for devices.csv set to True
#
#     col_to_view: List[str] = ['clients_name', 'clients_full_name', 'farms_name', 'farms_full_name',
#                               'farms_code', 'farmOwnerName', 'farmName',
#                               'houses_name', 'houses_code', 'cycle_houses_name', 'cycle_houses_code',
#                               'cycle_houses_cycle_start_date',
#                               'breed_type', 'gender', 'mongo_cycle_start_day']
#     postgre_table = PostgreClients()
#     shared = SharedDataBase(col_to_view=col_to_view)
#     # f = postgre_table.get_farms(filter)
#     result = shared.some(filter, use_local=use_local)
#     try:
#         result.to_csv(result_filename, sep=';', index=False)
#     except:
#         print(f"Please close file with the name {result_filename} !!!")
#     # for c in ch.columns:
#     #     print(c)
