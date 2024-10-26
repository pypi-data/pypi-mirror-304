import glob
import os
import zipfile
from pathlib import Path, PurePosixPath
from typing import Optional, List

import paramiko
from scp import SCPClient

from bdm2.constants.global_setup.data import Combination
from bdm2.constants.global_setup.env import (
    EC2_HOST_PROD,
    EC2_KEY_PROD,
    EC2_USER_PROD,
    EC2_ENGINE_FOLDER_PATH_PROD,
    EC2_USER_HOME_DIR,
)
from bdm2.constants.global_setup.server_paths import results_dir
from bdm2.constants.patterns.regexp_patterns import aws_engine_pattern
from bdm2.engine_validation.entities.db_component import DBEnginesComponent
from bdm2.engine_validation.entities.engine_component import Engine
from bdm2.logger import build_logger


class EC2PushComponent(Engine):
    """
        Handles uploading engine data to an EC2 instance and managing the associated processes.

        Attributes:
        -----------
        - pattern_aws_engine_name : str
            Regex pattern for AWS engine names.
        - ec2_host : str
            Host address of the EC2 instance.
        - ec2_user : str
            Username for EC2 instance.
        - ec2_key : str
            Key file path for EC2 instance.
        - ec2_engine_folder_path : str
            Path on EC2 where engine data is uploaded.
        - ec2_user_home_dir : str
            Home directory of the EC2 user.
        - set_actual : bool
            Flag to set the engine as actual in the database.
        - ssh_client : Optional[paramiko.SSHClient]
            SSH client for EC2 connection.
        - scp_client : Optional[SCPClient]
            SCP client for file transfers.
        - combination : Combination
            Combination object with client, breed type, and gender.

        Methods:
        --------
        __init__(local_paths: List[str], logger, commit_message: str, engine_pattern: str, set_actual: bool, combination: Combination)
            Initializes the component with local paths, logger, commit message, engine pattern, and combination.

        define_results_postfix(self) -> Optional[str]
            Returns results postfix (not defined in this case).

        _upload_callback(filename: str, size: int, sent: int)
            Displays upload progress for a file.

        _create_engine_zip(engine_folder_path: str, zip_file_path: str) -> bool
            Creates a zip file from the engine folder.

        _upload_zip_to_ec2(zip_file_path: str) -> bool
            Uploads the zip file to the EC2 instance.

        _ssh_exec_command(ec2_ssh_command: str)
            Executes a command on the EC2 instance via SSH.

        _pre_upload_process(engine_folder_name: str)
            Prepares EC2 for upload by handling existing folders.

        _after_upload_process(zip_file_path: str)
            Manages post-upload tasks such as unzipping and setting permissions.

        connect_to_ec2(server: str, user: str, p_key_file_path: str, port: int = 22)
            Establishes an SSH connection to the EC2 instance.

        upload_engine_to_ec2(local_engine_folder_path: str) -> bool
            Handles the entire process of zipping, uploading, and post-upload processing of engine data.

        get_results_postfix(dir_name: str) -> str
            Retrieves the results postfix for the specified engine directory.

        run()
            Executes the main workflow: connecting to EC2, uploading data, and updating the database.
        """
    pattern_aws_engine_name = aws_engine_pattern
    ec2_host: str = EC2_HOST_PROD
    ec2_user: str = EC2_USER_PROD
    ec2_key: str = EC2_KEY_PROD
    ec2_engine_folder_path: str = EC2_ENGINE_FOLDER_PATH_PROD
    ec2_user_home_dir: str = EC2_USER_HOME_DIR

    def __init__(
            self,
            local_paths: List[str],
            logger,
            commit_message,
            engine_pattern,
            set_actual,
            combination,
    ):
        super().__init__(local_paths, logger, commit_message, engine_pattern)
        self.set_actual: bool = set_actual
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.scp_client: Optional[SCPClient] = None
        self.combination: Combination = combination

    @property
    def define_results_postfix(self):
        return None

    @staticmethod
    def _upload_callback(filename, size, sent):
        sent = max(sent, 1)  # Prevent division by zero
        progress_percent = 100 / (size / sent)
        print(
            f"Upload: {filename} | Size: {size} bytes | Progress: {progress_percent:.2f} %"
        )

    @staticmethod
    def _create_engine_zip(engine_folder_path: str, zip_file_path: str) -> bool:
        print(f"Creating zip file: {zip_file_path}")
        try:
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for file_name in glob.iglob(
                        engine_folder_path + "**/**", recursive=True
                ):

                    if Path(file_name).is_file():
                        arcname = file_name[len(engine_folder_path) + 1:]
                        zip_file.write(file_name, arcname)
            print(f"Zip file created: {zip_file_path}")
            return True
        except Exception as e:
            print(f"Error creating zip file: {e}")
            return False

    def _upload_zip_to_ec2(self, zip_file_path: str) -> bool:
        # logger.info()
        self.logger.info(f"\n{' starting upload to EC2... ':-^70}")
        try:
            self.scp_client.put(zip_file_path, self.ec2_user_home_dir)
            self.logger.info("upload to EC2 completed.")
            return True
        except Exception as e:
            self.logger.error(f"error uploading to EC2: {e}")
            return False

    def _ssh_exec_command(self, ec2_ssh_command):
        self.logger.info(f"executing command on EC2: {ec2_ssh_command}")
        stdin, stdout, stderr = self.ssh_client.exec_command(ec2_ssh_command)
        stdout.channel.recv_exit_status()

        stdout_lines = stdout.readlines()
        stderr_lines = stderr.readlines()

        for line in stdout_lines:
            line = line.strip(" \n")
            self.logger.info(f"STDOUT: {line}")
        for line in stderr_lines:
            line = line.strip(" \n")
            self.logger.info(f"STDERR: {line}")

        if stderr_lines:
            raise Exception(f"Command execution failed: {ec2_ssh_command}")

    def _pre_upload_process(self, engine_folder_name: str):
        unzip_folder_name = os.path.basename(engine_folder_name)[len("aws_cloud"):]
        full_unzip_folder_path = os.path.join(
            self.ec2_engine_folder_path, unzip_folder_name
        )
        ec2_ssh_command = f"sudo [ -d {full_unzip_folder_path} ] && echo 'exists'"

        stdin, stdout, stderr = self.ssh_client.exec_command(ec2_ssh_command)
        stdout.channel.recv_exit_status()
        is_exists = "exists" in stdout.read().decode("utf-8")

        if is_exists:
            self.logger.info(
                f"Folder already exists: {full_unzip_folder_path}, it will be deleted."
            )
            ec2_ssh_command = f"sudo rm -r {full_unzip_folder_path}"
            self._ssh_exec_command(ec2_ssh_command)
            self.logger.info("Folder deleted.")

    def _after_upload_process(self, zip_file_path: str):
        zip_file_name = os.path.basename(zip_file_path)
        unzip_folder_name = zip_file_name[len("aws_cloud"): -len(".zip")]
        full_zip_file_path = PurePosixPath(self.ec2_engine_folder_path) / zip_file_name

        full_unzip_folder_path = (
                PurePosixPath(self.ec2_engine_folder_path) / unzip_folder_name
        )

        commands = [
            f"sudo mv {self.ec2_user_home_dir}/{zip_file_name} {self.ec2_engine_folder_path}",
            f"sudo unzip -o {full_zip_file_path} -d {full_unzip_folder_path}",
            f"sudo chmod -R 777 {full_unzip_folder_path}",
            f"sudo chown -R {self.ec2_user}:{self.ec2_user} {full_unzip_folder_path}",
            f"sudo rm -r {full_zip_file_path}",
        ]

        for command in commands:
            try:
                self._ssh_exec_command(command)
            except Exception as e:
                self.logger.error(f"Error executing command '{command}': {e}")
                break

    def connect_to_ec2(
            self, server: str, user: str, p_key_file_path: str, port: int = 22
    ):
        self.logger.info(
            f"connecting to EC2:\n"
            f"\tServer: {server}\n"
            f"\tUser: {user}\n"
            f"\tPort: {port}\n"
            f"\tKey: {p_key_file_path}"
        )
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh_client.connect(
                hostname=server, username=user, key_filename=p_key_file_path, port=port
            )
            self.scp_client = SCPClient(
                self.ssh_client.get_transport(), progress=self._upload_callback
            )
            self.logger.info("SSH connection established.")
        except Exception as e:
            self.logger.error(f"SSH connection failed: {e}")
            raise

    def upload_engine_to_ec2(self, local_engine_folder_path: str) -> bool:
        engine_folder_name = os.path.basename(local_engine_folder_path)
        zip_file_path = os.path.join(
            os.path.dirname(local_engine_folder_path), f"{engine_folder_name}.zip"
        )

        if os.path.exists(zip_file_path):
            self.logger.info(
                f"zip file {zip_file_path} already exists and will be deleted."
            )
            os.remove(zip_file_path)
            self.logger.info("existing zip file deleted.")

        if not self._create_engine_zip(local_engine_folder_path, zip_file_path):
            return False

        self._pre_upload_process(engine_folder_name)

        if not self._upload_zip_to_ec2(zip_file_path):
            return False

        self._after_upload_process(zip_file_path)
        return True

    def get_results_postfix(self, dir_name):
        client_root_dir = Path(results_dir) / self.combination.client
        results_path = client_root_dir / f"RESULTS{self.define_engine_name[dir_name]}"
        current_engine_result_dir = [
            i for i in Path(client_root_dir).iterdir() if str(results_path) in str(i)
        ]
        if not len(current_engine_result_dir):
            raise ValueError(f"no results folder for engine {dir_name}")
        else:
            return str(current_engine_result_dir[0]).split(
                self.define_engine_name[dir_name]
            )[1]

        pass

    def run(self):
        for num, directory in enumerate(self.local_paths, start=1):
            self.logger.info(f"{f'engine {num}: {Path(directory).name} ':-^70}")

            self.connect_to_ec2(self.ec2_host, self.ec2_user, self.ec2_key)
            for path in self.local_paths:
                self.upload_engine_to_ec2(path)

            self.logger.info(f"{' work with db ':-^70}")
            dir_name = Path(directory).name
            results_postfix = self.get_results_postfix(dir_name)

            db_component = DBEnginesComponent(
                logger=self.logger,
                engine_v_name=self.engine_versions,
                results_postfix=results_postfix,
                comment=self.commit_message,
                density_model_id=self.define_density_model_id_local,
                engine_postfix=self.define_engine_name[dir_name],
                combination=self.combination
            )
            engine_v_id = db_component.run()

            if self.set_actual is True:
                db_component.set_engine_as_actual(combination=self.combination)
            else:
                self.logger.info("skipped setting as actual")

            db_component.add_in_release_history(engine_v_id=engine_v_id)


if __name__ == "__main__":
    local_release_paths = [
        r"\\PawlinServer\Projects\prj\MHDR\BIRDOO\Releases"
        r"\v4.0.0.00\aws_cloud_v4.0.0.00_CGTHBG_Arbor-Acres_female_0000_final"
    ]
    combination_ = {"client": "DEFAULT", "breed_type": "DEFAULT", "gender": "DEFAULT"}
    combination_ = Combination(**combination_)
    ec2_uploader = EC2PushComponent(
        set_actual=True,
        engine_pattern=aws_engine_pattern,
        local_paths=local_release_paths,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
        commit_message="test",
        combination=combination_,
    )
    ec2_uploader.run()
