from pathlib import Path

import yaml

from bdm2.constants.global_setup.data import Combination
from bdm2.constants.patterns.regexp_patterns import (
    split_engine_pattern,
    aws_engine_pattern,
)
from bdm2.engine_validation.entities.ec2_engine import EC2PushComponent
from bdm2.engine_validation.entities.split_engine import SplitPushComponent
from bdm2.logger import build_logger


# from engine_validation.entities.ec2_engine import *


class ReleaseEngine:
    """
            Manages the process of engines release, support 2 engine types:
             - aws
             - split

            Attributes:
            -----------
            - local_release_paths : list
                list of local filepaths.
            - this_is_release_for: str
                literal sign of release type.
            - commit_message: str
                message which will be added in releases table and git header
            - set_actual:
                bool flag, does no matter for split releases
            - combination:
                target combination, does no matter for split releases

            run()
                Executes the workflow: defines type of release, call an instance of the class
                and starts the loading process into the corresponding source with the specified parameters
            """
    def __init__(
            self,
            local_release_paths: list,
            this_is_release_for: str,
            commit_message: str,
            set_actual: bool,
            combination,
    ):
        self.local_release_paths: list = local_release_paths
        self.this_is_release_for: str = this_is_release_for
        self.commit_message: str = commit_message
        self.logger = build_logger(file_name=f"{Path(__file__)}", save_log=False)
        self.set_actual: bool = set_actual
        self.combination: Combination = Combination(**combination)

    def run(self):
        if self.this_is_release_for == "split":
            self.logger.info("determined the split release")
            split_engine_component = SplitPushComponent(
                local_paths=self.local_release_paths,
                logger=self.logger,
                commit_message=self.commit_message,
                engine_pattern=split_engine_pattern,
            )
            split_engine_component.run()

        elif self.this_is_release_for == "aws":
            ec2_uploader = EC2PushComponent(
                set_actual=self.set_actual,
                engine_pattern=aws_engine_pattern,
                local_paths=self.local_release_paths,
                logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
                commit_message=self.commit_message,
                combination=self.combination,
            )
            ec2_uploader.run()


if __name__ == "__main__":
    release_config = ReleaseEngine(
        **yaml.load(open(r"release_engine_config.yaml"), yaml.Loader)
    )

    release_config.run()


