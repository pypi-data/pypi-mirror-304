import os
import socket
import uuid
import warnings

from dotenv import load_dotenv

dotenv_path = os.getenv("BIRDOO_CREDS_PATH")
load_dotenv(dotenv_path)

# --------- EC2 --------- #

EC2_HOST_PROD = os.getenv("EC2_HOST_PROD")
EC2_KEY_PROD = os.getenv("EC2_KEY_PROD")
EC2_USER_PROD = os.getenv("EC2_USER")
EC2_ENGINE_FOLDER_PATH_PROD = os.getenv("EC2_ENGINE_FOLDER_PATH_PROD")
EC2_USER_HOME_DIR = f"/home/{EC2_USER_PROD}"

# --------- GIT --------- #

GIT_SPLIT_REPO_URL = os.getenv("GIT_SPLIT_REPO_URL")

# --------- AWS ACCESS BIRDOO --------- #
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# ----------------------- #

# --------- AWS ACCESS KNEX --------- #

AWS_ACCESS_KEY_KNEX = os.getenv("AWS_ACCESS_KEY_KNEX")
AWS_SECRET_KEY_KNEX = os.getenv("AWS_SECRET_KEY_KNEX")
AWS_REGION_KNEX = os.getenv("AWS_REGION_KNEX")

# --------- STANDARD BOT TG  --------- #
standards_bot_token = os.getenv("standards_bot_token")
standards_bot_chat_id = os.getenv("standards_bot_chat_id")

# --------- MONGO DB --------- #

MONGO_SERVER = os.getenv("MONGO_SERVER")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")
MONGO_CONNECTION_NAME = os.getenv("MONGO_CONNECTION_NAME")
# --------- BRDDB_API ----------- #

BRDDB_API_USERNAME = os.getenv("BRDDB_API_USERNAME")
BRDDB_API_PASSWORD = os.getenv("BRDDB_API_PASSWORD")
BRDDB_API_URL = os.getenv("BRDDB_API_URL")

# ----------------------- #


MACHINE_ID = os.getenv("MACHINE_ID") or socket.gethostname()
SERVER_CHICKEN_DIR = os.getenv("SERVER_CHICKEN_DIR")
SERVER_DATA_DIR = os.getenv("SERVER_DATA_DIR")
SESS_ID = uuid.uuid4().hex[:10]
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["CUDA_VISIBLE_DEVICES"] = os.getenv("CUDA_VISIBLE_DEVICES", "0")

try:
    workdir = os.getenv("MHDR_CHICKEN_WORKDIR")
    if workdir is None:
        raise EnvironmentError(f"No MHDR_CHICKEN_WORKDIR in env")
except Exception as e:
    workdir = r"D:\MHDR_Chicken\workdir"
    warnings.warn(f"{e}\nworkdir will be defined as {workdir}")
