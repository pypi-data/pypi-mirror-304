from pathlib import Path

from bdm2.constants.global_setup.engine import filepath_to_density_model_info_file
from bdm2.constants.patterns.regexp_patterns import (
    split_engine_pattern,
    aws_engine_pattern,
    split_engine_pattern_example,
)


class Engine:
    """
    Handles operations related to engine versioning, pattern matching, and density model identification for different engine release folders.

    Attributes:
    -----------
    - local_paths : list[str]
        A list of paths to local engine release folders.
    - logger : Logger
        Logger instance for logging operations.
    - commit_message : str
        Commit message for version control operations.
    - results_postfix : str
        A postfix to be appended to results, initialized as an empty string.
    - engine_pattern : re.Pattern
        Regular expression pattern to match engine versions and other details from folder names.
    """

    def __init__(self, local_paths, logger, commit_message, engine_pattern):
        self.local_paths = local_paths
        self.logger = logger
        self.commit_message = commit_message
        self.results_postfix = ""
        self.engine_pattern = engine_pattern

    @property
    def _assert_paths_exist(self):
        """
        Checks that `local_paths` is not empty and raises an error if it is.
        @return: bool
        """
        assert len(self.local_paths), self.logger.error(
            "no engine release folder path has been submitted for entry!"
        )
        return True

    def _match_pattern(self, pattern, string):
        """
        Matches a given string against the provided regular expression pattern and logs an error if the match is unsuccessful.
        """
        match = pattern.match(string)
        if not match:
            self.logger.error(
                f"could not identify engine version, check your folder_names satisfied pattern {pattern}"
            )
        return match

    @property
    def engine_versions(self):
        """
        Retrieves the engine version from the folder names based on the provided pattern.
        @return: engine_v
        """
        for eng in self.local_paths:
            engine_name = Path(eng).name
            match = self._match_pattern(self.engine_pattern, engine_name)
            if match:
                return match["engine_v"]

    @property
    def branch_names(self):
        """
        Retrieves branch names by matching folder names against a specific pattern (`split_engine_pattern`).
        """
        if self.engine_pattern == split_engine_pattern:
            matches_dict = {}
            for num, eng in enumerate(self.local_paths):
                engine_name = Path(eng).name
                match = self._match_pattern(self.engine_pattern, engine_name)
                if match:
                    matches_dict[engine_name] = (
                        f"{match['engine_v']}_{match['device_type']}_{match['engine']}"
                    )

            if len(matches_dict):
                separator = " ➡ "
                for num, (key, value) in enumerate(matches_dict.items(), start=1):
                    self.logger.info(
                        f"branch {num} has been identified: {key}{separator}{value}"
                    )
            else:
                self.logger.error(
                    f"could not identify branch_names,"
                    f" check your folder_names satisfied pattern {split_engine_pattern}"
                )
                raise ValueError
            return matches_dict
        else:
            return None

    @property
    def define_density_model_id_local(self):
        """
        Reads and returns the density model ID from the `density_model_info_file.txt` in each release folder.
        """
        for num, eng in enumerate(self.local_paths):
            prediction_nets_filepath = Path(eng) / filepath_to_density_model_info_file
            if not Path(prediction_nets_filepath).is_file():
                self.logger.error(
                    f"density_model_info_file.txt does not exist: {prediction_nets_filepath}"
                )
                return None
            with prediction_nets_filepath.open("r") as file:
                density_model_id = file.readline().strip()
                self.logger.info(
                    f"defined density model id from release folder file: {density_model_id}"
                )
                return int(density_model_id)

    @property
    def define_engine_name(self):
        """
        Determines and returns the engine name based on the provided patterns (`split_engine_pattern` or `aws_engine_pattern`).
        """
        matches_dict = {}
        for num, eng in enumerate(self.local_paths):
            engine_name = Path(eng).name
            match = self._match_pattern(self.engine_pattern, engine_name)
            if self.engine_pattern == split_engine_pattern:
                if match:
                    matches_dict[engine_name] = (
                        f"_{match['engine']}_{match['engine_v']}_{match['release_date']}"
                    )
                else:
                    raise ValueError(
                        f"engine name does not match with release type."
                        f"\n{split_engine_pattern}"
                        f"\nexample: {split_engine_pattern_example}"
                    )
            elif self.engine_pattern == aws_engine_pattern:
                if match:
                    matches_dict[engine_name] = (
                        f"_v{match['engine_v']}_"
                        f"{match['client']}_"
                        f"{match['breed_type']}_"
                        f"{match['gender']}_"
                        f"{match['release_date']}_"
                        f"final"
                    )
                    return matches_dict
                else:
                    raise ValueError(
                        f"engine name does not match with release type."
                        f"\n{aws_engine_pattern}"
                        f"\nexample: {split_engine_pattern_example}"
                    )

        return matches_dict
