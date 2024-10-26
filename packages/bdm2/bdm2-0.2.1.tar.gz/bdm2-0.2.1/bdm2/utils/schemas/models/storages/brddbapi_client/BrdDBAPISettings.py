from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bdm2.constants.global_setup.env import BRDDB_API_USERNAME, BRDDB_API_PASSWORD, BRDDB_API_URL


# class BrdDBAPISettings(BaseSettings):
#     # load_dotenv()
#
#     BRDDB__USERNAME: str = Field(BRDDB_API_USERNAME)
#     BRDDB__PASSWORD: str = Field(BRDDB_API_PASSWORD)
#     BRDDB__URL: str = Field(BRDDB_API_URL)
#
#     model_config = SettingsConfigDict(env_file="../../../.env", extra="ignore")
import os
# from pydantic import BaseSettings, Field

class BrdDBAPISettings(BaseSettings):

    O_USERNAME: str = Field(BRDDB_API_USERNAME)
    PASSWORD: str = Field(BRDDB_API_PASSWORD)
    URL: str = Field(BRDDB_API_URL)


#
# # Пример использования
# components = BrdDBAPISettings()
# print(components.USERNAME)
# print(components.PASSWORD)
# print(components.URL)