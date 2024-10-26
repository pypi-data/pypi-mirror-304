from pathlib import Path
# -------- folders --------#
from typing import Optional

from bdm2.constants.global_setup.env import workdir, SERVER_CHICKEN_DIR, SERVER_DATA_DIR
from bdm2.constants.global_setup.server_paths import server_workdir

OtherData_folder_name = "OtherData"
prediction_nets_folder_name = "prediction_nets"
# --------- files ---------#
density_model_info_file_name = r"density_model_info.txt"

filepath_to_density_model_info_file = (
        Path(OtherData_folder_name)
        / prediction_nets_folder_name
        / density_model_info_file_name
)
from loguru import logger


class EngineConfig:
    """Defines engine params"""

    ForwardRunViz_folder: str = r"ForwardRunViz_explicit"  #: folder name with explicits
    ForwardRunViz_binary_folder: str = (
        r"ForwardRunViz_explicit_binary"  #: folder name with compressed explicits
    )
    ForwardRunViz_rolled_folder: str = (
        r"ForwardRunViz_rolled"  #: folder name with rolled
    )
    ForwardRunViz_rolled_binary_folder: str = (
        r"ForwardRunViz_rolled_binary"  #: folder name with compressed explicits
    )
    ForwardRunViz_images_folder: str = (
        r"ForwardRunViz_images"  #: folder name with explicit images
    )
    Predictions_folder: str = r"Predictions"  #: folder name with predictions
    Markup_folder: str = r"Markup"  #: folder name with markup
    ImageQuality_folder: str = r"ImageQuality"  #: folder name with IMageQualities
    Running_stats_folder: str = r"Running_stats"  #: folder name with explicits
    Results_summary_folder: str = "Results_summary"
    Pose_classifier_folder: str = (
        "pose_classifier"  #: folder name with results summary (statistics)
    )
    gender_crop_folder: str = "gender_crop"  #: folder name with gender_crop images
    SD_Objs_filename: str = "SD_Objs.txt"
    SDM_filename: str = "SDM.txt"
    stats_explicit_filename: str = (
        "Stats_explicit.txt"  #: contains explicit statistics. Updates after each launch
    )
    stats_rolled_filename: str = (
        "Stats_rolled.txt"  #: contains rolled statistics. Updates after each launch
    )

    weight_filename: str = r"PredictedWeights.txt"  #: DEPRECATED
    explicit_filename: str = (
        r"ForwardRunViz_explicit.txt"  #: standard explicit filename after engine run
    )
    explicit_rolled_filename: str = (
        r"ForwardRunViz_rolled.txt"  #: standard rolled filename after engine run
    )
    experiments_map_filename: str = (
        r"experiments_map.csv"  #: filename of rolled statistics
    )
    main_params_filename: str = "main_params.yml"
    density_model_info: str = "density_model_info.txt"  #

    """
    Defined by engine version
    """

    def __init__(self):
        """ "
        Test parameters

        """

        #: engine version format _v{version number}_{engine_postfix}
        self.engine_version: str = ""

        #: postfix for results, format _{results_postfix},
        #: different results_postfix can be used for different ways of engine run.
        #: "" - for engine full run mode, "_restore" - for restore mode, "_restore_fast" - for fast restore mode
        self.results_postfix: str = ""

        #: full path to results
        self.local_results_dir: str = ""

        #: full path to engine_snapshot in local_results_dir
        self.engine_snapshot_dir: str = ""

        #: full path to engine workdir (on server)
        self.engine_dir_on_server: str = ""

        #: local path. full path to engine workdir (on local machine)
        self.engine_dir: str = ""
        #: local path. full path to imagery (on local machine)
        self.imagery_dir: str = ""

        #: full path to results folder with utils markup.
        #: Source makrup can be used during engine_full_run (specified mode)
        #: As default, markup_results_dir = local_results_dir.
        #: Can be referenced to another engine local_results_dir to use predefined markup.
        #: If markup folder is empty - standard engine_full_run mode will be used
        self.markup_results_dir: str = ""

        #: full path to ForwardRunViz_explicit folder after engine run (in engine_dir).
        self.ForwardRunViz_dir: str = ""
        #: full path to ForwardRunViz_rolled folder after engine run (in engine_dir).
        self.ForwardRunViz_rolled_dir: str = ""
        #: full path to Images of ForwardRunViz_explicit folder after engine run (in engine_dir).
        self.ForwardRunViz_images_dir: str = ""
        #: full path to Predictions folder after engine run (in engine_dir).
        self.Predictions_dir: str = ""

        #: full path to main_params.yml file.
        self.main_params_dir: str = ""
        #: DEPRECATED. No usages
        self.main_params_no_detects_filename: str = ""

        #: full path to main_params.yml file.
        self.engine_bat: str = ""
        #: DEPRECATED. No usages
        self.engine_bat_no_detects: str = ""

    evening_time = ""

    def get_engine_version_digits(self, engine_version=None):
        if engine_version is None:
            return self.engine_version[2:].split("_")[0]
        else:
            return engine_version[2:].split("_")[0]

    def get_engine_postfix(self):
        start_ind = self.engine_dir_on_server.rfind("engine") + len("engine")
        return self.engine_dir_on_server[start_ind:]

    def get_local_results_postfix(self):
        start_ind = self.local_results_dir.rfind("RESULTS") + len("RESULTS")
        return self.local_results_dir[start_ind:]

    def set_local_results_dir(self, local_results_dir):
        self.local_results_dir = local_results_dir
        self.engine_snapshot_dir = self.local_results_dir + "\\engine_snapshot"

    def set_another_engine_dir(
            self, new_engine_version: str, client: Optional[str] = None
    ):
        self.engine_dir = workdir + "\\engine{}".format(new_engine_version)
        if client is None:
            client = self.define_client(new_engine_version)

        if client == "":
            self.engine_dir_on_server = server_workdir + f"\\engine{new_engine_version}"
        else:
            self.engine_dir_on_server = (
                    server_workdir + f"\\{client}\\engine{new_engine_version}"
            )

        self.ForwardRunViz_dir = self.engine_dir + "\\" + self.ForwardRunViz_folder
        self.ForwardRunViz_rolled_dir = (
                self.engine_dir + "\\" + self.ForwardRunViz_rolled_folder
        )
        # self.ForwardRunViz_binary_dir = self.engine_dir + "\\" + self.ForwardRunViz_binary_folder
        # self.ForwardRunViz_rolled_binary_dir = self.engine_dir + "\\" + self.ForwardRunViz_rolled_binary_folder
        self.ForwardRunViz_images_dir = (
                self.engine_dir + "\\" + self.ForwardRunViz_images_folder
        )
        self.Predictions_dir = self.engine_dir + "\\" + self.Predictions_folder

        self.main_params_dir = self.engine_dir + "\\main_params.yml"
        self.engine_bat = self.engine_dir + "\\runFromPy.bat"
        self.main_params_no_detects_filename = (
                self.engine_dir + "\\main_params_no_detects.yml"
        )
        self.engine_bat_no_detects = self.engine_dir + "\\runFromPy_no_detects.bat"

    def define_client(self, engine_version: str) -> str:
        true_client = ""
        if engine_version not in ["_from_devices", "_from_devices_spy"]:
            true_client = engine_version.split("_")[2]

        return true_client

    def set_another_engine_version(
            self, version: str, results_postfix: str, client: Optional[str] = None
    ):
        if client is None:
            client = self.define_client(version)
        logger.info(f"Client for {version} was defined as {client}")
        self.engine_version = version
        self.results_postfix = results_postfix

        server_path = rf"{SERVER_CHICKEN_DIR}\MHDR_Chicken"
        if self.engine_version in ["_from_devices", "_from_devices_spy"]:
            server_path = rf"{SERVER_DATA_DIR}"
        if client != "":
            local_results_dir = r"{}\RESULTS\{}\RESULTS{}{}".format(
                server_path, client, self.engine_version, self.results_postfix
            )
        else:
            local_results_dir = r"{}\RESULTS\RESULTS{}{}".format(
                server_path, self.engine_version, self.results_postfix
            )
        self.set_local_results_dir(local_results_dir)

        self.markup_results_dir = self.local_results_dir

        self.imagery_dir = workdir + "\\Imagery{}".format(version)

        self.set_another_engine_dir(self.engine_version, client=client)
        # self.set_another_engine_dir(GlobalConfig.workdir + "\\engine{}".format(version))
