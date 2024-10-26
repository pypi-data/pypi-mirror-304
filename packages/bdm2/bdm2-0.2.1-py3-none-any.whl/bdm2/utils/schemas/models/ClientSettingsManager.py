import warnings
from typing import Optional, Dict

from bdm2.constants.global_setup.engine import EngineConfig
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


def check_empty(val, name):
    if not len(val):
        raise AssertionError(f"Value: {name} has not length")
    return val


class ClientSettings:
    """
    Data structure that contains all necessary information for data analysis

    :param client_name: client name
    :param engine_postfix: existing engine
    :param results_postfix: results postfix for engine with engine_postfix
    :param gender: DEPRECATED as used in filters
    :param breed_type: DEPRECATED as used in filters
    :param filters: define devices scope of interest
    :param manual_weights_postfix: define target weights that will be used as targets

    """

    def __init__(
            self,
            client_name: Optional[str] = None,
            engine_postfix: Optional[str] = None,
            results_postfix: Optional[str] = None,
            gender: Optional[str] = None,
            breed_type: Optional[str] = None,
            filters: Optional[Filter] = None,
            manual_weights_postfix: Optional[str] = None,
    ):
        #: is used for obtaining statistics and other standards
        self.client_name: str = client_name

        self.gender = gender
        self.breed_type = breed_type
        #: define device scope of interest
        self.filters: Filter = filters
        if isinstance(self.filters, Dict):
            self.filters = Filter(**self.filters)

        #: define target weights that will be used as targets
        self.manual_weights_postfix = manual_weights_postfix

        #: main config, defined from engine_postfix and  results_postfix.
        #: used as data src object
        self.main_config = None
        if engine_postfix is not None and results_postfix is not None:
            self.main_config: EngineConfig = EngineConfig()
            self.main_config.set_another_engine_version(
                engine_postfix, results_postfix, client=client_name
            )
        elif (engine_postfix is not None) or (results_postfix is not None):
            warnings.warn(
                f"ClientSettings.__init__: was set only one of two required params [engine_postfix, results_postfix]."
                f"Can not init main_config!!!!"
            )


class ClientSettingsChild(ClientSettings):

    def __init__(
            self,
            filters: Filter,
            client_name: str = None,
            engine_postfix: Optional[str] = None,
            results_postfix: Optional[str] = None,
            gender: Optional[str] = None,
            breed_type: Optional[str] = None,
            manual_weights_postfix: Optional[str] = None,
            kwargs=None,
    ):

        ClientSettings.__init__(
            self,
            filters=filters,
            client_name=client_name,
            engine_postfix=engine_postfix,
            results_postfix=results_postfix,
            gender=gender,
            breed_type=breed_type,
            manual_weights_postfix=manual_weights_postfix,
        )

        # adding extra features
        if not kwargs:
            kwargs = dict()
        if (
                "engine_postfix" in kwargs.keys()
                and "results_postfix" in kwargs.keys()
                and self.main_config is None
        ):
            self.main_config = EngineConfig()
            self.main_config.set_another_engine_version(
                kwargs[engine_postfix], kwargs["results_postfix"]
            )

        for key, value in kwargs.items():
            if key not in self.__dict__.keys() or self.__getattribute__(key) is None:
                if key == "engine_postfix" or key == "results_postfix":
                    continue
                self.__setattr__(key, value)
