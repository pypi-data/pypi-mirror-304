"""
Provides classes with some widely used constants
"""

import glob
import os
import re
from pathlib import Path
from typing import Tuple, Dict, List, Iterable, Optional


class FileExtensions:
    splitter: str = "."

    parquet: str = ".parquet"
    feather: str = ".feather"
    txt: str = ".txt"
    csv: str = ".csv"
    bz2: str = ".bz2"

    parquet_key: str = parquet.lstrip(splitter)
    feather_key: str = feather.lstrip(splitter)
    txt_key: str = txt.lstrip(splitter)
    csv_key: str = csv.lstrip(splitter)
    bz2_key: str = bz2.lstrip(splitter)


class ExplicitFileConstants:
    # this splitter attr will be referred in this class' staticmethods
    splitter: str = "."
    forward_run_filename_part: str = "ForwardRun"

    age_part: str = "_age_"
    capture_part: str = "_Capture_"

    explicit_foldername: str = f"{forward_run_filename_part}Viz_explicit"
    rolled_foldername: str = f"{forward_run_filename_part}Viz_rolled"

    explicit_required_filename_part: str = explicit_foldername
    rolled_required_filename_part: str = rolled_foldername

    explicit_or_rolled_gen_regex_pattern: str = f".*{forward_run_filename_part}Viz_*.*"

    explicits_general_search_pattern: str = f"*{explicit_required_filename_part}_*.*"
    rolled_general_search_pattern: str = f"*{rolled_required_filename_part}_*.*"

    available_format_keys: Tuple[str, ...] = (
        FileExtensions.txt_key,
        FileExtensions.csv_key,
        FileExtensions.bz2_key,
        FileExtensions.parquet_key,
        FileExtensions.feather_key,
    )

    available_extensions: Tuple[str, ...] = (
        FileExtensions.txt,
        FileExtensions.csv,
        FileExtensions.bz2,
        FileExtensions.parquet,
        FileExtensions.feather,
    )

    save_kwargs: Dict[str, str] = dict(sep=";", index=False)

    listing_order: Iterable[str] = (
        FileExtensions.parquet,
        FileExtensions.txt,
        FileExtensions.bz2,
        FileExtensions.csv,
        FileExtensions.feather,
    )

    # implemented mainly for ExplicitManager/load_explicit func
    # compare only sets because order of initial attrs really matters
    assert set(available_extensions) == set(listing_order), (
        f"listing order must contain the same number of elements "
        f"as the available_formats does - it will receive list of "
        f"extensions filtered by available formats (!)"
    )

    common_part_key: str = "common_part"

    format_to_extension_mapping: Dict[str, str] = {
        ext.lstrip(FileExtensions.splitter): ext for ext in available_extensions
    }

    #

    @staticmethod
    def get_format(extension: str):
        """
        returns stripped (from left) extension
        """
        output: str = extension.lstrip(ExplicitFileConstants.splitter)
        return output

    @staticmethod
    def get_extension(path: str) -> str:
        """
        must accept only filename (i.e. basename) rather than full path (because of concatenating splitted string)
        if we're going to change some
             extension + splitter
                logic
        edit this func
        """
        output = Path(path).suffix
        # output: str = ExplicitFileConstants.splitter + path.split(ExplicitFileConstants.splitter)[-1]
        return output

    @staticmethod
    def get_common_part(filename: str):
        """
        Since it concatenates strings
            you have to make sure that it accepts basename (filename) rather than full filepath
        """
        output: str = ExplicitFileConstants.splitter.join(
            filename.split(ExplicitFileConstants.splitter)[:-1]
        )
        return output

    @staticmethod
    def get_common_part_to_extension_map(
            files_list: List[str],
    ) -> Dict[str, Dict[str, str]]:
        """
        # TODO: maybe assertion one level above for files_list[0] == os.path.basename(files_list[0])

        Input must be list of FILENAMES
            rather than filepaths (!)
            (otherwise there's no guarantee you'll get appropriate results)

        this func shouldn't take os.path.basename because it will slow the listing (other functions this one uses
            also must take filename (basename)

        use os.listdir()
        """
        # TODO: consider using different types of list (Union[AnyStr, Path])
        #   and cast str_path dynamically like
        #
        #   ```python
        #       for filename in files_list:
        #           str_fn = str(filename)
        #       ...
        #   ```

        # make a map:
        #   file_body -> Map<extension, path>
        #   so you can select faster than iterating over list of tuples
        common_to_formats: Dict[str, Dict[str, str]] = {}
        for filename in files_list:
            # proceed
            c_ext = ExplicitFileConstants.get_extension(filename)
            if c_ext not in ExplicitFileConstants.available_extensions:
                continue
            c_common_part = ExplicitFileConstants.get_common_part(filename)
            # if c_ext in formats:
            if c_common_part not in common_to_formats.keys():
                common_to_formats[c_common_part] = {}  # []
            # append splitter + c_ext due to the fact that in the formats they are with '.'
            common_to_formats[c_common_part][c_ext] = filename

        return common_to_formats

    @staticmethod
    def select_from_common_map_filenames(
            common_map: Dict[str, Dict[str, str]]
    ) -> List[str]:
        """
        Expects common_map as the result of .get_common_part_to_extension_map()
            and simply returns the result of selecting filenames by priority list
        """
        # TODO: replace ExplicitManager.list_explicits()
        #   with this function call (almost the same code)
        selected_filenames: List[str] = []
        for common_part in common_map.keys():
            c_files: Dict[str, str] = common_map[common_part]
            # since you have 'continue' keyword during dict collecting
            #   you don't have to handle zero length case (even though it's handled via <fp is not None>)
            if len(c_files) == 1:
                # append it using generator rather than iterator
                # https://stackoverflow.com/a/3097896
                selected_filenames.append(next(iter(c_files.values())))
            else:
                # now in the following order:
                # first goes parquet, than txt and the last one is bz2
                fp: Optional[str] = None
                for prioritized_ext in ExplicitFileConstants.listing_order:
                    # if prioritized_ext in c_files.keys():
                    fp = c_files.get(prioritized_ext, None)
                    if fp is not None:
                        selected_filenames.append(fp)
                        break

                assert fp is not None, f"fp was not initialized; check for loops"

        return selected_filenames

    @staticmethod
    def replace_extension(path: str, new_ext: str) -> str:
        curr_ext: str = ExplicitFileConstants.get_extension(path)
        assert (
                new_ext in ExplicitFileConstants.available_extensions
        ), f"ext={new_ext} - unknown extension; see {ExplicitFileConstants.available_extensions}"
        # even though there's small chance of it
        #   you may still have .csv or .txt in the middle of some foldername
        #   so take basename exactly
        curr_filename: str = os.path.basename(path)
        new_filename = curr_filename.replace(curr_ext, new_ext)
        # and replace basenames:
        new_path = path.replace(curr_filename, new_filename)
        return new_path

    @staticmethod
    def remove_extension(
            path: str,
    ) -> str:
        new_ext: str = ""
        curr_ext: str = ExplicitFileConstants.get_extension(path)
        # even though there's small chance of it
        #   you may still have .csv or .txt in the middle of some foldername
        #   so take basename exactly
        curr_filename: str = os.path.basename(path)
        new_filename = curr_filename.replace(curr_ext, new_ext)
        # and replace basenames:
        new_path = path.replace(curr_filename, new_filename)
        return new_path

    @staticmethod
    def list_all_rolled(dirpath: str) -> List[str]:
        """
        since it uses glob.glob
            it will return absolute paths (!)
        """
        search_pattern: str = ExplicitFileConstants.rolled_general_search_pattern
        files_available = list(glob.glob(f"{dirpath}/{search_pattern}"))
        return files_available

    @staticmethod
    def list_all_explicits(dirpath: str) -> List[str]:
        """
        since it uses glob.glob
            it will return absolute paths (!)
        """
        search_pattern: str = ExplicitFileConstants.explicits_general_search_pattern
        files_available = list(glob.glob(f"{dirpath}/{search_pattern}"))
        return files_available

    @staticmethod
    def list_unique_explicits(dirpath: str, abs: bool = False) -> List[str]:
        """
        since it uses glob.glob
            it will return absolute paths (!)
        """
        search_pattern: str = ExplicitFileConstants.explicits_general_search_pattern
        files_available = list(glob.glob(f"{dirpath}/{search_pattern}"))
        # TODO: consider replacing it with abs paths
        #   since .get_common... can deal with them
        filenames_available: List[str] = [os.path.basename(p) for p in files_available]
        # now make a map:
        common_to_ext_map: Dict[str, Dict[str, str]] = (
            ExplicitFileConstants.get_common_part_to_extension_map(filenames_available)
        )

        selected_filenames: List[str] = (
            ExplicitFileConstants.select_from_common_map_filenames(common_to_ext_map)
        )

        if abs:
            selected_filepaths: List[str] = [
                os.path.join(dirpath, fn) for fn in selected_filenames
            ]
            return selected_filepaths
        else:
            return selected_filenames

    @staticmethod
    def list_unique_rolled(dirpath: str, abs: bool = False) -> List[str]:
        """
        since it uses glob.glob
            it will return absolute paths (!)
        """
        search_pattern: str = ExplicitFileConstants.rolled_general_search_pattern
        files_available = list(glob.glob(f"{dirpath}/{search_pattern}"))
        # TODO: consider replacing it with abs paths
        #   since .get_common... can deal with them
        filenames_available: List[str] = [os.path.basename(p) for p in files_available]
        # now make a map:
        common_to_ext_map: Dict[str, Dict[str, str]] = (
            ExplicitFileConstants.get_common_part_to_extension_map(filenames_available)
        )

        selected_filenames: List[str] = (
            ExplicitFileConstants.select_from_common_map_filenames(common_to_ext_map)
        )

        if abs:
            selected_filepaths: List[str] = [
                os.path.join(dirpath, fn) for fn in selected_filenames
            ]
            return selected_filepaths
        else:
            return selected_filenames

    @staticmethod
    def replace_capture_to_age_part(
            filename: str,
    ) -> str:
        re_pattern: str = rf".*({ExplicitFileConstants.capture_part}).*"
        match = re.match(re_pattern, string=filename)
        if match is None:
            raise AssertionError(
                f"{filename}: Cannot process string with regex {re_pattern}"
            )
        assert len(match.groups()) == 1, f""
        # replace:
        new_filename: str = filename.replace(
            ExplicitFileConstants.capture_part, ExplicitFileConstants.age_part
        )
        return new_filename


class ArchiveImagesConstants:
    output_part: str = "output"
    capture_copy_foldername: str = "Capture_copy"
    tar_archive_format: str = ".tar.gz"
    folder_format: str = ""

    # === tarfile
    tarfile_open_mode: str = "r:gz"
    tarfile_write_mode: str = "w:gz"

    #
    win_cache_file: str = "Thumbs.db"


class PostgreConstants:
    client_id_colname: str = "client_id"
    client_code_colname: str = "client_code"
    client_name_colname: str = "client_name"

    farm_id_colname: str = "farm_id"
    farm_code_colname: str = "farm_code"
    farm_name_colname: str = "farm_name"

    house_id_colname: str = "house_id"
    house_code_colname: str = "house_code"
    house_name_colname: str = "house_name"

    cycle_house_id_colname: str = "cycle_house_id"
    cycle_house_code_colname: str = "cycle_house_code"
    cycle_house_name_colname: str = "cycle_house_name"

    cycle_start_day_colname: str = "cycle_start_day"

    cycle_id_colname: str = "cycle_id"
    cycles_table_id_colname: str = "cycles_table_id"
    cycle_code_colname: str = "cycle_code"
    gender_name_colname: str = "gender"
    gender_id_colname: str = "gender_id"
    breed_type_name_colname: str = "breed_type"
    breed_type_id_colname: str = "breed_type_id"

    # === devices table constants ===
    device_id_colname: str = "device_id"
    device_name_colname: str = "device_name"

    # === Actual_client_weights table constants ===
    standard_weights_colname: str = "standard_weights"
    statistics_colname: str = "statistics"
    age_colname: str = "age"
    weights_colname: str = "Weights"

    # === density_models table constants ===
    density_model_id_colname: str = "density_model_id"
    density_model_name_colname: str = "density_model_name"
    density_model_config_colname: str = "density_model_config"

    # === engine_configs table constants ===
    engine_configs_id_colname: str = "engine_configs_id"
    engine_version_name_colname: str = "engine_version_name"
    engine_results_postfix_colname: str = "results_postfix"
    engine_configs_comment_colname: str = "engine_configs_comment"

    # === engine_versions table constants ===
    engine_version_id_colname: str = "engine_version_id"
    engine_version_colname: str = "engine_version"

    # defaults:
    default_standard_weights_client_code: str = "CGBRCV"
    default_standard_weights_breed_type_name: str = "ROSS"
    default_standard_weights_gender_name: str = "mix"

    # projection constants:
    projection_model_name_colname: str = "model_name"
    projection_is_verified_colname: str = "is_verified"
    projection_filename_colname: str = "filename"
    projection_model_id_colname: str = "model_id"
    projection_min_input_length_colname: str = r"min_input_length"
    backward_propagation_num_colname: str = "backward_propagation_num"

    projection_model_match_columns: Tuple[str, ...] = (
        client_id_colname,
        breed_type_id_colname,
        gender_id_colname,
    )


class DevicesFileConstants:
    # use the same variable names as for postgre:
    # client_code_colname: str = 'client'
    client_name_colname: str = "client"
    client_code_colname: str = "client_id"

    farm_code_colname: str = "farm_id"
    farm_name_colname: str = "farm"

    house_code_colname: str = "house_id"
    house_name_colname: str = "house"

    cycle_house_code_colname: str = "cycle_id"
    cycle_id_colname: str = "cycle_id"
    cycle_code_colname: str = "cycle_id"

    cycle_house_name_colname: str = "cycle"

    gender_name_colname: str = "gender"
    breed_type_name_colname: str = "breed_type"

    cycle_start_day_colname: str = "cycle_start_day"
    cycle_start_day_datetime_format: str = "%d-%m-%Y"

    # === devices table constants ===
    device_name_colname: str = "device"
    path_colname: str = "path"

    device_label_colname: str = "id"

    required_columns: List[str] = [
        client_name_colname,
        client_code_colname,
        farm_code_colname,
        farm_name_colname,
        house_name_colname,
        house_code_colname,
        cycle_house_code_colname,
        cycle_house_name_colname,
        gender_name_colname,
        breed_type_name_colname,
        cycle_start_day_colname,
        device_name_colname,
        path_colname,
    ]


class DevicesFileToPostgreNamesConstants:
    existing_devices_file_attribute_names: List[str] = [
        "client_name_colname",
        "client_code_colname",
        "farm_code_colname",
        "farm_name_colname",
        "house_code_colname",
        "house_name_colname",
        "cycle_house_code_colname",
        # 'cycle_id_colname',
        "cycle_house_name_colname",
        "gender_name_colname",
        "breed_type_name_colname",
        "cycle_start_day_colname",
        "device_name_colname",
    ]
    renaming_dict: Dict[str, str] = {
        getattr(DevicesFileConstants, attr_name): getattr(PostgreConstants, attr_name)
        for attr_name in existing_devices_file_attribute_names
    }

    inverse_renaming_dict: Dict[str, str] = {
        value: key for key, value in renaming_dict.items()
    }


class MongoConstants:
    age_colname: str = "age"
    cycle_house_code_colname: str = "cycleId"
    farm_code_colname: str = "farmId"
    mass_corr_mean_colname: str = "meanWt"
    projection_colname: str = "isProjection"

    bird_type_colname: str = "birdType"
    breed_type_name_colname: str = "birdType"

    gender_name_colname: str = "birdSex"

    cycle_start_day_colname: str = "startDate"


class CommonDownloaderConstants:
    # matching between database helper constants
    farm_code_exact_pattern: str = r"\w+"
    house_code_exact_pattern: str = r"\w+-\w+"
    cycle_house_code_exact_pattern: str = r"\w+-\w+-\w+"


class GoogleDownloaderConstants:
    # matching between database helper constants
    farm_regex_pattern: str = r"(\w+)-.*"
    farm_house_regex_pattern: str = r"(\w+-\w+)-.*"
    farm_house_cycle_regex_pattern: str = r"\w+-\w+-\w+"
