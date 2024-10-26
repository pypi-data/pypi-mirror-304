from typing import Optional

from brddb.utils.common import colorstr
from loguru import logger

from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.ClientSettingsManager import ClientSettings
from bdm2.utils.schemas.models.storages.actual_clients_info_storage.actual_clients_info_storage import (
    ActualClientsInfoStorage,
)


def generate_actual_client_settings(
        actual_info_storage: ActualClientsInfoStorage,
        client_name: Optional[str],
        breed_type: Optional[str] = None,
        gender: Optional[str] = None,
        filters: Optional[Filter] = None,
        engine_postfix: Optional[str] = None,
        results_postfix: Optional[str] = None,
        manual_weights_postfix: Optional[str] = None,
) -> ClientSettings:
    if breed_type is None or client_name is None or gender is None:
        raise ValueError(
            f"Could not generate_actual_client_settings "
            f"as some of client_name, breed_type, gender is None. "
        )
        # logger.info(colorstr('yellow',
        #                          f'Will be used input parameters'))
        # cs = ClientSettings(client_name=client_name, engine_postfix=engine_postfix,
        #                     results_postfix=results_postfix,
        #                     gender=gender, breed_type=breed_type, manual_weights_postfix=manual_weights_postfix,
        #                     filters=filters)
    else:
        actual_engine_postfix, actual_results_postfix = (
            actual_info_storage.get_actual_engine(
                client=client_name, breed_type=breed_type, gender=gender
            )
        )
        if engine_postfix is None:
            engine_postfix = actual_engine_postfix
            logger.info(
                f"For {client_name} {breed_type} {gender} engine_postfix was set as {engine_postfix}"
            )
        if results_postfix is None:
            results_postfix = actual_results_postfix
            logger.info(
                f"For {client_name} {breed_type} {gender} results_postfix was set as {results_postfix}"
            )
        if manual_weights_postfix is None:
            manual_weights_postfix = (
                actual_info_storage.get_actual_target_weights_postfix(
                    client=client_name, breed_type=breed_type, gender=gender
                )
            )
            logger.info(
                f"For {client_name} {breed_type} {gender} target_weights_postfix was set as {manual_weights_postfix}"
            )
        if filters is None:
            filters = Filter()
        cs = ClientSettings(
            client_name=client_name,
            engine_postfix=engine_postfix,
            results_postfix=results_postfix,
            gender=gender,
            breed_type=breed_type,
            manual_weights_postfix=manual_weights_postfix,
            filters=filters,
        )
    return cs


def fill_client_settings_with_actual_info(
        actual_info_storage: ActualClientsInfoStorage, client_settings: ClientSettings
):
    if (
            client_settings.breed_type is None
            or client_settings.client_name is None
            or client_settings.gender is None
    ):
        logger.info(
            colorstr(
                "yellow",
                f"Could not generate_actual_client_settings "
                f"as some of client_name, breed_type, gender is None. ",
            )
        )
        return
    else:

        if client_settings.main_config is None:
            actual_engine_postfix, actual_results_postfix = (
                actual_info_storage.get_actual_engine(
                    client=client_settings.client_name,
                    breed_type=client_settings.breed_type,
                    gender=client_settings.gender,
                )
            )
            client_settings.main_config = EngineConfig()
            client_settings.main_config.set_another_engine_version(
                version=actual_engine_postfix, results_postfix=actual_results_postfix
            )
            logger.info(
                f"For {client_settings.client_name} {client_settings.breed_type} {client_settings.gender} "
                f"main__config was set as {actual_engine_postfix}{actual_results_postfix}"
            )

        if client_settings.manual_weights_postfix is None:
            client_settings.manual_weights_postfix = (
                actual_info_storage.get_actual_target_weights_postfix(
                    client=client_settings.client_name,
                    breed_type=client_settings.breed_type,
                    gender=client_settings.gender,
                )
            )
            logger.info(
                f"For {client_settings.client_name} {client_settings.breed_type} {client_settings.gender} "
                f"target_weights_postfix was set as {client_settings.manual_weights_postfix}"
            )
        if client_settings.filters is None:
            client_settings.filters = Filter()
