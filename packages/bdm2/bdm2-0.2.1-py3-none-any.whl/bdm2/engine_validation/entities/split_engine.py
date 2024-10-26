from pathlib import Path

from bdm2.constants.global_setup.env import GIT_SPLIT_REPO_URL
from bdm2.constants.patterns.regexp_patterns import split_engine_pattern
from bdm2.engine_validation.entities.db_component import DBEnginesComponent
from bdm2.engine_validation.entities.engine_component import Engine
from bdm2.engine_validation.entities.git_comon_component import GitComponent
from bdm2.logger import build_logger


class SplitPushComponent(Engine):
    """
        Manages the process of pushing engine data to a Git repository and updating the database.

        Attributes:
        -----------
        - git_repo_url : str
            URL of the Git repository for split engine data.
        - engine_pattern : str
            Regex pattern for engine names.

        Methods:
        --------
        __init__(local_paths: List[str], logger, commit_message: str, engine_pattern: str)
            Initializes the component with local paths, logger, commit message, and engine pattern.

        run()
            Executes the workflow: logging engine data, updating the database, and pushing updates to the Git repository.
        """
    git_repo_url = GIT_SPLIT_REPO_URL

    def __init__(self, local_paths, logger, commit_message, engine_pattern):
        super().__init__(local_paths, logger, commit_message, engine_pattern)
        self.engine_pattern = split_engine_pattern

    def run(self):
        final_info = []
        for num, directory in enumerate(self.local_paths, start=1):
            self.logger.info(f"{f'engine {num}: {Path(directory).name} ':-^70}")
            self.logger.info(f"{' work with db ':-^70}")
            dir_name = Path(directory).name

            db_components = DBEnginesComponent(
                logger=self.logger,
                engine_v_name=self.engine_versions,
                results_postfix=self.results_postfix,
                comment=self.commit_message,
                density_model_id=self.define_density_model_id_local,
                engine_postfix=self.define_engine_name[dir_name],
                combination=None)
            db_components.run()

            self.logger.info(f"{' work with git ':-^70}")

            branch = self.branch_names[dir_name]
            git_component = GitComponent(
                self.git_repo_url,
                branch_name=branch,
                local_folder_path=directory,
                logger=self.logger,
            )

            git_component.clone_repo()
            git_component.replace_entities_to_git_folder()
            message = git_component.add_commit_push(
                branch_name=branch, commit_message=self.commit_message
            )
            final_info.append(message)
        self.logger.info(*final_info, sep=";")


if __name__ == "__main__":
    local_release_paths = [
        r"\\PawlinServer\Projects\prj\MHDR\BIRDOO\Releases\v4.0.0.00\jetson_split_v4.10.0.00_0101"
    ]

    slit_engine_component = SplitPushComponent(
        local_paths=local_release_paths,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
        commit_message="TEST",
        engine_pattern=split_engine_pattern,
    )
    slit_engine_component.run()
