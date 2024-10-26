import os
import time
from pathlib import Path

import clickhouse_connect
from dotenv import load_dotenv
from sqlalchemy import create_engine
from loguru import logger


class POSTGRE_SQL_CREDS:
    dotenv_path: Path = os.getenv("BIRDOO_CREDS_PATH")
    load_dotenv(dotenv_path)

    host: str = os.getenv("POSTGRES__SERVER")
    port: int = os.getenv("POSTGRES__PORT")
    user: str = os.getenv("POSTGRES__USER")
    password: str = os.getenv("POSTGRES__PASSWORD")
    db_name: str = os.getenv("POSTGRES__DATABASE_NAME")


postgres_engine = create_engine(
    f"postgresql://{POSTGRE_SQL_CREDS.user}:{POSTGRE_SQL_CREDS.password}@"
    f"{POSTGRE_SQL_CREDS.host}/{POSTGRE_SQL_CREDS.db_name}",
    pool_size=10,             # Increase pool size if there are concurrent connections
    max_overflow=10,          # Number of extra connections allowed beyond pool_size
    pool_timeout=30,          # Time to wait for a connection before raising an error
    pool_recycle=1800,        # Recycle connections after 30 minutes
    pool_pre_ping=True,
    connect_args={'connect_timeout': 10}
)  #:{POSTGRE_SQL_CREDS.port}


def get_clickhouse_client(retries=10, delay=1):
    attempt = 0
    while attempt < retries:
        try:
            client = clickhouse_connect.get_client(
                host=os.getenv("CLICK_HOST"),
                username=os.getenv("CLICK_USER"),
                password=os.getenv("CLICK_PASSWORD"),
                port=int(os.getenv("CLICK_PORT")),
                secure=True,
            )
            return client
        except Exception as e:
            attempt += 1
            logger.error(f"Connection attempt {attempt} failed: {e}")

            if attempt == retries:
                logger.error("Max retries reached. Unable to connect to the database.")
                raise e
            logger.info(f"Retrying connection in {delay} seconds...")
            time.sleep(delay)
