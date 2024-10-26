from brddb.models.postgres import ActualClientsInfoTable, ChickenWeights

from .data import max_age


class GeneratedDataFormat:
    max_age = max_age
    actual_info_src = ActualClientsInfoTable()
    weights_src = ChickenWeights()


# import GeneratedDataFormat

# import GeneratedDataFormat


class StandardComponent(GeneratedDataFormat):

    def __init__(self):
        self.filter = filter

    def check_is_combo_has_enough_data(self):
        pass

    def connect_bot(self):
        pass

    def generate_standard(self):
        pass

    def run(self):
        self.connect_bot()
        self.check_is_combo_has_enough_data()
        self.generate_standard()

    # import os

# import socket
# import uuid
# import warnings
# from dataclasses import dataclass
# from dotenv import load_dotenv
#
# # Загрузка переменных из .env файла
# dotenv_path = os.path.join(os.path.dirname(__file__), '...', '.env')  # путь к .env файлу
# load_dotenv(dotenv_path)
#
# # Использование переменных среды
# MACHINE_ID = os.getenv('MACHINE_ID') or socket.gethostname()
# SERVER_CHICKEN_DIR = os.getenv('SERVER_CHICKEN_DIR')
# SERVER_DATA_DIR = os.getenv('SERVER_DATA_DIR')
# SESS_ID = uuid.uuid4().hex[:10]
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# os.environ['CUDA_VISIBLE_DEVICES'] = os.getenv('CUDA_VISIBLE_DEVICES', "0")
#
#
# class GlobalConfig:
#     max_age = 60
#     struct_levels = ["farm", "cycle", "flock", "house", "device"]
#     device_match_columns = ["farm", "cycle", "house", "device"]
#     house_match_columns = ["farm", "cycle", "house"]
#     standards_match_columns = ['client', 'breed_type', 'gender']
#     # age_column = 'age'
#     # breed_type_column = 'breed_type'
#     # gender_column = 'gender'
#
#     default_flock_name = "Flock 1"
#
#     #  drop image_qualities_columns = ["brightness", "height", "missing", "tilt", 'blur']
#
#     valuable_reliability_columns = [
#         "reliability",
#         "common_reliability",
#         "private_reliability",
#         "tilt_reliability",
#         "missing_reliability"
#     ]
#
#     features_list_file = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Features\features.xlsx"
#
#     @dataclass
#     class GroupByConfig:
#         do_grouping: bool
#         reliability: str
#         use_median: bool = False
#
#     # TODO
#     group_by_methods = {
#         'v0': {
#             'group_by_track': GroupByConfig(do_grouping=False, reliability=""),
#             'group_by_sess': GroupByConfig(do_grouping=False, reliability=""),
#             'group_by_age': GroupByConfig(do_grouping=True, reliability=""),
#             'group_by_house': GroupByConfig(do_grouping=True, reliability="")
#         },
#         'v3': {
#             'group_by_track': GroupByConfig(do_grouping=True, reliability="private_reliability"),
#             'group_by_sess': GroupByConfig(do_grouping=False, reliability=""),
#             'group_by_age': GroupByConfig(do_grouping=True, reliability="reliability"),
#             'group_by_house': GroupByConfig(do_grouping=False, reliability="")
#         },
#         'v4': {
#             'group_by_track': GroupByConfig(do_grouping=True, reliability="private_reliability"),
#             'group_by_sess': GroupByConfig(do_grouping=True, reliability=""),
#             'group_by_age': GroupByConfig(do_grouping=True, reliability=""),
#             'group_by_house': GroupByConfig(do_grouping=False, reliability="")
#         },
#     }
#
#     active_group_by_method = 'v4'
#
#     group_by_track_reliability = group_by_methods[active_group_by_method]['group_by_track'].reliability
#     group_by_age_reliability = group_by_methods[active_group_by_method]['group_by_age'].reliability
#     group_by_house_reliability = group_by_methods[active_group_by_method]['group_by_house'].reliability
#
#     gender_encoder = {
#         "male": 0,
#         "mix": 1,
#         "female": 2,
#         'Gender': -1
#     }
#
#     @staticmethod
#     def gender_decoder(gender_code):
#         res = dict((v, k) for k, v in GlobalConfig.gender_encoder.items())
#         return res[gender_code]  # Prints george
#
#     breed_type_encoder_new = {
#         "Arbor Acres": 1,
#         "ROSS": 0,
#         "ROSS_Thailand": 4,
#         "Cobb": 3,
#         "ROSS_breeders": 5,
#         "Cobb_breeders": 6,
#     }
#
#     breed_type_encoder = {
#         "Arbor Acres": 0,
#         "ROSS": 1,
#         "ROSS_Thailand": 2,
#         "Cobb": 3,
#         "ROSS_breeders": 4,
#         "Cobb_breeders": 5,
#         "Lohmann": 6,
#         # "Hubbart": 7,
#         "Hubbard": 7,
#         'BreedType': -1
#     }
#
#     @staticmethod
#     def breed_type_decoder(breed_type_code, new=False):
#         if new:
#             res = dict((v, k) for k, v in GlobalConfig.breed_type_encoder_new.items())
#         else:
#             res = dict((v, k) for k, v in GlobalConfig.breed_type_encoder.items())
#
#         return res[breed_type_code]  # Prints george
#
#         # return GlobalConfig.breed_type_encoder.keys()[GlobalConfig.breed_type_encoder.values().index(breed_type_code)]
#
#     not_critical_params = [
#         "RPrepFactoryParams_imagery_folder",
#         "ObjectQualityEstimatorParams_save_explicit_result_imagery",
#         "ObjectQualityEstimatorParams_save_prediction_result_imagery"
#     ]
#     reader_filters = [
#         "detroi",
#         "eccentricity",
#         "extent"
#     ]
#
#     sess_folder_date_format = "output_%Y_%m_%d_%H_%M_%S"
#     image_date_format = "%Y.%m.%d.%H.%M.%S.%f"
#
#     try:
#         workdir = os.getenv('MHDR_CHICKEN_WORKDIR')
#         if workdir is None:
#             raise EnvironmentError(f"No MHDR_CHICKEN_WORKDIR in env")
#     except Exception as e:
#         workdir = r"D:\MHDR_Chicken\workdir"
#         warnings.warn(f"{e}\nworkdir will be defined as {workdir}")
#     extra_libs_path = r"C:\libs"
#     extra_libs_link_name = 'ChickenWeighting.exe.local'
#
#     tmp_download_dir = workdir + r"\tmp_download"
#
#     server_workdir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\workdir"
#     results_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\RESULTS"
#
#     # ENGINE BLOCKS
#     engines_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Engines"
#     statistics_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Statistics"
#     density_models_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\DensityModels"
#     shape_corrector_models_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\ShapeCorrectorModels"
#     distance_models_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\DistanceCorrectorModels"
#     ideal_cv_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\IdealCV"
#     standards_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Standards"
#     # =============
#
#     current_active_server_data_dir = fr"{SERVER_DATA_DIR}\DATA"
#     # current_active_server_data_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\DATA"
#     current_active_server_results_dir = fr"{SERVER_DATA_DIR}\RESULTS\RESULTS_from_devices"
#
#     current_active_server_spy_results_dir = fr"{SERVER_DATA_DIR}\RESULTS\RESULTS_from_devices_spy"
#
#     server_data_summary_df_filename = "data_summary.csv"
#
#     server_source_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources"
#     # if not os.path.exists(server_source_dir):
#     #     os.makedirs(server_source_dir)
#
#     scenario_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\workdir\SCENARIO"
#     manual_weights_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\ManualWeights"
#     slt_dir = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\SLUT"
#
#     """ Devices information sources """
#     device_csv = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices.csv"
#
#     device_to_test_csv = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices_to_test.csv"
#     devices_for_training_csv = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices_for_training.csv"
#     birdoo_device_matching_xlsx = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\Birdoo Device List-Apr 27.xlsx"
#
#     actual_engines_info_path = fr"{SERVER_CHICKEN_DIR}\MHDR_Chicken"
#
#     postgres_configs_path = fr''
#     git_configs_path = fr''
