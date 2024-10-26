import os
import re
import shutil
import subprocess
from pathlib import Path

from git import Repo
from tqdm import tqdm

from bdm2.logger import build_logger


class ProgressPrinter:
    def __init__(self, total_objects):
        self.total_objects = total_objects
        self.current_progress = 0
        self.pbar = None

    def __call__(self, op_code, cur_count, max_count=None, message=""):
        if self.pbar is None:
            self.pbar = tqdm(total=self.total_objects, unit=" objects")

        if cur_count <= max_count:
            self.pbar.n = cur_count
            self.pbar.refresh()
            self.current_progress = cur_count

        if cur_count == max_count:
            self.pbar.update(self.total_objects - self.current_progress)
            self.pbar.close()
            self.pbar = None


def mask_url(url):
    """Заменяет токен или пароль в URL звездочками"""
    return re.sub(r"(?<=://).*?(?=@)", "*****", url)


class GitComponent:
    """
        Manages Git repository operations such as cloning, branch creation, and committing changes.

        Attributes:
        -----------
        - git_repo_url : str
            URL of the Git repository.
        - branch_name : str
            Name of the branch to work with.
        - local_folder_path : str
            Local folder path containing files to push to the repository.
        - logger : Logger
            Logger instance for logging operations.

        Methods:
        --------
        __init__(git_repo_url: str, local_folder_path: str, logger, branch_name: str)
            Initializes the Git component with repository URL, local path, logger, and branch name.

        git_folder : Path
            Returns the path of the Git folder, creating it if it doesn't exist.

        add_safe_directory()
            Adds the Git folder to the list of safe directories in global Git configuration.

        clean_git_directory()
            Removes all files and directories in the Git folder except the .git directory.

        clone_repo()
            Clones the repository from the Git URL into the Git folder, or reinitializes it if already present.

        create_branch()
            Creates and checks out a new branch with the specified name.

        replace_entities_to_git_folder()
            Copies files from the local folder to the Git folder.

        push_with_progress(remote, refspec: str)
            Pushes changes to the remote repository with progress indication.

        add_commit_push(branch_name: str, commit_message: str) -> str
            Stages, commits, and pushes changes to the specified branch with a commit message.

        count_files_and_folders(folder_path: str) -> int
            Counts the total number of files and directories in the specified folder.
        """

    def __init__(self, git_repo_url, local_folder_path, logger, branch_name):
        self.git_repo_url = git_repo_url
        self.repo = None
        self.branch_name = branch_name
        self.local_folder_path = local_folder_path
        self.logger = logger

    @property
    def git_folder(self):
        new_folder_name = (
                Path(self.local_folder_path).parent
                / f"{Path(self.local_folder_path).name}_git"
        )
        if not Path(new_folder_name).exists():
            os.mkdir(new_folder_name)
            self.logger.info(f"created git folder: \n{new_folder_name}")
        return new_folder_name

    def add_safe_directory(self):
        try:
            git_folder_path = self.git_folder.as_posix()
            safe_dir_command = [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                f"%(prefix)/{git_folder_path}",
            ]
            self.logger.info(f'Running command: {" ".join(safe_dir_command)}')
            result = subprocess.run(
                safe_dir_command, check=True, capture_output=True, text=True
            )
            self.logger.info(f"Successfully added safe directory: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to add safe directory: {e.stderr}")

    def clean_git_directory(self):
        git_dir = self.git_folder / ".git"
        self.logger.info("cleaning git repo folder")
        if git_dir.exists() and git_dir.is_dir():
            # delete all folder \ files except .git
            for item in self.git_folder.iterdir():
                if item.is_dir() and item.name != ".git":
                    shutil.rmtree(item)
                elif item.is_file() and item.name != ".git":
                    item.unlink()

    def clone_repo(self):
        try:
            self.add_safe_directory()
            if os.path.exists(os.path.join(self.git_folder, ".git")):
                self.clean_git_directory()
                self.repo = Repo(self.git_folder)
                self.logger.info(f"identified git_repo folder: \n{self.git_folder}")
            else:
                self.repo = Repo.clone_from(self.git_repo_url, self.git_folder, depth=1)
                masked_url = mask_url(self.git_repo_url)
                self.repo.remote().fetch()
                self.logger.info(
                    f"successfully cloned repository from {masked_url} to {self.git_folder}"
                )
        except Exception as e:
            self.logger.error(f"failed to clone repository: {e}")

    def create_branch(self):
        try:
            self.add_safe_directory()
            new_branch = self.repo.create_head(self.branch_name)
            new_branch.checkout()
            self.logger.info(f'created and checked out new branch "{self.branch_name}"')
        except Exception as e:
            self.logger.error(f"failed to create branch: {e}")

    def replace_entities_to_git_folder(self):
        for item in os.listdir(self.local_folder_path):
            src_path = os.path.join(self.local_folder_path, item)
            dst_path = os.path.join(self.git_folder, item)

            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                self.logger.info(f"Copied: {src_path} to {dst_path}")
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        self.logger.info(
            f"items copied from {self.local_folder_path}\n to \n{self.git_folder}"
        )

    def push_with_progress(self, remote, refspec):
        total_objects = self.count_files_and_folders(self.local_folder_path)
        progress_printer = ProgressPrinter(total_objects)
        remote.push(refspec=refspec, progress=progress_printer, force=True)

    def add_commit_push(self, branch_name, commit_message):
        try:
            self.add_safe_directory()
            self.repo.git.add(A=True)
            self.logger.info("Added all changes to the staging area")

            commit = self.repo.index.commit(commit_message)
            self.logger.info(f'Committed changes with message: "{commit_message}"')
            commit_id = commit.hexsha

            if "origin" not in self.repo.remotes:
                origin = self.repo.create_remote("origin", self.git_repo_url)
                self.logger.info(
                    f"created remote origin with URL {mask_url(self.git_repo_url)}"
                )
            else:
                origin = self.repo.remotes.origin
                origin.set_url(self.git_repo_url)
                self.logger.info(
                    f"updated remote origin with URL {mask_url(self.git_repo_url)}"
                )

            origin = self.repo.remote()
            self.push_with_progress(origin, refspec=f"HEAD:refs/heads/{branch_name}")
            self.logger.info(
                f'successfully pushed to branch "{branch_name}" at {mask_url(self.git_repo_url)}'
            )
            # self.logger.info(f'\n{branch_name} commit_id: {commit_id}')
            return f"\n{branch_name} commit_id: {commit_id}"
        except Exception as e:
            self.logger.info(f"failed to add/commit/push changes: {e}")

    @staticmethod
    def count_files_and_folders(folder_path):
        total_objects = sum(len(files) for _, _, files in os.walk(folder_path))
        total_objects += sum(len(dirs) for _, dirs, _ in os.walk(folder_path))
        return total_objects


if __name__ == "__main__":
    local_folder_path_ = r"\\PawlinServer\Projects\prj\MHDR\BIRDOO\Releases\v4.0.0.00\jetson_split_v4.10.7.46_0101"
    git_repo_url_ = r""
    branch_name = "test_branch2"
    commit_message = "Initial commit"

    git_component = GitComponent(
        git_repo_url_,
        branch_name=branch_name,
        local_folder_path=local_folder_path_,
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
    )
    git_component.clone_repo()
    git_component.replace_entities_to_git_folder()
    git_component.add_commit_push(
        branch_name=branch_name, commit_message=commit_message
    )
