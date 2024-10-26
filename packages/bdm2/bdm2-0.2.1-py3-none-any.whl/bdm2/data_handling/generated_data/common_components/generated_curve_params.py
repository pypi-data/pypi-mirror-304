from bdm2.constants.global_setup.data import max_age
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.models.data_structures.weights_structure import WEIGHTS_UNITS
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import PostgresActualClientsInfoStorage
from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage
from bdm2.utils.schemas.models.storages.target_weights.sqlalchemy_target_weights_storage import \
    PostgresAlchemyTargetWeightsStorage


class GeneratedWeightsParams:
    max_extrapolated_day = max_age +1 #
    filters = Filter()
    actual_clients_storage = PostgresActualClientsInfoStorage()
    src_devices_storage = PostgresDevicesStorage()
    src_weights_storage = PostgresAlchemyTargetWeightsStorage(src_devices_storage, units=WEIGHTS_UNITS['kg'])
    src_format = src_weights_storage.output_default_format