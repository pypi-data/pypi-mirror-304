from bdm2.constants.global_setup.env import SERVER_CHICKEN_DIR, SERVER_DATA_DIR

server_workdir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\workdir"
results_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\RESULTS"

engines_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Engines"
statistics_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Statistics"
density_models_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\DensityModels"
shape_corrector_models_dir = (
    rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\ShapeCorrectorModels"
)
distance_models_dir = (
    rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\DistanceCorrectorModels"
)
ideal_cv_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\IdealCV"
standards_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Standards"
statistics_fname = r'\\Datasets\chikens\MHDR_Chicken\sources\Statistics\Thailand_Statistics_basic_0311.csv'

current_active_server_data_dir = rf"{SERVER_DATA_DIR}\DATA"
current_active_server_results_dir = rf"{SERVER_DATA_DIR}\RESULTS\RESULTS_from_devices"
current_active_server_spy_results_dir = (
    rf"{SERVER_DATA_DIR}\RESULTS\RESULTS_from_devices_spy"
)

server_data_summary_df_filename = "data_summary.csv"
server_source_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources"
scenario_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\workdir\SCENARIO"
manual_weights_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\ManualWeights"
slt_dir = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\SLUT"

device_csv = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices.csv"
device_to_test_csv = (
    rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices_to_test.csv"
)
devices_for_training_csv = (
    rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\devices_for_training.csv"
)
birdoo_device_matching_xlsx = (
    rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken\sources\Devices\Birdoo Device List-Apr 27.xlsx"
)

actual_engines_info_path = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken"
aws_pem_path = r"\\datasets\chikens\configs\aws_pem\ms_bookawheelkey.pem"

engine_releases_path = r"\\PawlinServer\Projects\prj\MHDR\BIRDOO\Releases"

extra_libs_path = r"C:\libs"
extra_libs_link_name = 'ChickenWeighting.exe.local'

statistics_server_dir = r"\\Datasets\chikens\MHDR_Chicken\sources\datasets\statistics"
