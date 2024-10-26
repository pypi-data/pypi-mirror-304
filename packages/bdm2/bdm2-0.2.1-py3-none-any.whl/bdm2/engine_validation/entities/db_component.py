from datetime import datetime
from pathlib import Path
from typing import Optional

from brddb.models.postgres import (
    EngineConfigs,
    Engines,
    Clients,
    BreedTypes,
    Genders,
    ActualClientsInfoTable
)
from brddb.utils.common import colorstr
from sqlalchemy import insert, select, update, and_
from sqlalchemy.orm import sessionmaker

from bdm2.logger import build_logger
from bdm2.utils.schemas.connection import postgres_engine


class DBEnginesComponent:
    """
        Manages database operations related to engine configurations and client information.

        Attributes:
        -----------
        - logger : Logger
            Logger instance for logging operations.
        - engine_v_name : str
            Name of the engine version.
        - results_postfix : str
            Postfix for results.
        - engine_postfix : str
            Postfix for the engine configuration.
        - comment : str
            Comment for the engine configuration.
        - density_model_id : int
            ID of the density model.
        - combination : Combination
            Combination of client, breed type, and gender.
        - engine_v_id : Optional[int]
            ID of the engine version.
        - engine_config_id : Optional[int]
            ID of the engine configuration.
        - session : Session
            SQLAlchemy session for database operations.
        - set_as_actual : Optional[bool]
            Flag to set the engine as actual.

        Methods:
        --------
        __init__(logger, engine_v_name: str, results_postfix: str, comment: str, density_model_id: int, engine_postfix: str, combination)
            Initializes the DBEnginesComponent with provided parameters.

        get_engine_version_id()
            Retrieves the ID of the engine version from the database or registers it if not found.

        register_unknown_engine_version()
            Registers a new engine version in the database.

        check_engine_config_id_is_registered() -> list
            Checks if the engine configuration is already registered in the database.
            Returns: List of IDs if registered.

        register_engine_config() -> Optional[int]
            Registers the engine configuration in the database if not already registered.
            Returns: ID of the engine configuration if successfully registered.

        set_engine_as_actual(combination)
            Sets the engine configuration as actual for the specified combination.
            Parameters:
            - combination: Combination of client, breed type, and gender.

        get_id_by_name(session, name: str, entity) -> Optional[int]
            Retrieves the ID of a table entity by its name.
            Parameters:
            - session: SQLAlchemy session.
            - name: Name of the entity.
            - entity: Entity class.
            Returns: ID of the entity or None if not found.

        get_client_bree_gender_combo_entity(session, client: str, breed_type: str, gender: str)
            Retrieves or creates a client-breed-gender combination entity.
            Parameters:
            - session: SQLAlchemy session.
            - client: Client name.
            - breed_type: Breed type name.
            - gender: Gender name.
            Returns: ActualClientsInfoTable entity.

        add_in_release_history(engine_v_id: int)
            Adds the engine configuration to the release history.
            Parameters:
            - engine_v_id: ID of the engine version.

        run() -> Optional[int]
            Executes the operations to get the engine version ID and register the engine configuration.
            Returns: ID of the engine configuration.
        """

    def __init__(
            self,
            logger,
            engine_v_name,
            results_postfix,
            comment,
            density_model_id,
            engine_postfix,
            combination,
    ):
        self.logger = logger
        self.engine_v_name = engine_v_name
        self.results_postfix = results_postfix
        self.engine_postfix = engine_postfix
        self.engine_v_id = None
        self.comment = comment
        self.density_model_id = density_model_id
        self.session = sessionmaker(bind=postgres_engine)()
        self.set_as_actual = None
        self.combination = combination
        self.engine_config_id = None

    def get_engine_version_id(self):

        stmt = select(Engines.id).where(Engines.name == self.engine_v_name)
        rows = self.session.execute(stmt).scalars().all()
        if len(rows) == 0:
            self.logger.warning(
                f"engine version {self.engine_v_name} is not registered yet.\n"
                f"Will be added to engine versions table automatically"
            )
            self.register_unknown_engine_version()
        if len(rows) >= 1:
            self.engine_v_id = rows[0]
            self.logger.info(
                f"defined registered {self.engine_v_name}, id = {self.engine_v_id}"
            )

    def register_unknown_engine_version(self):

        stmt = insert(Engines).values(name=self.engine_v_name, date=datetime.now())
        self.session.execute(stmt)
        self.session.commit()
        self.get_engine_version_id()

    def check_engine_config_id_is_registered(self):
        stmt_check = select(EngineConfigs.id).where(
            EngineConfigs.engine_id == self.engine_v_id,
            EngineConfigs.name == self.engine_postfix,
            EngineConfigs.results_postfix == self.results_postfix,
            EngineConfigs.density_model_id == self.density_model_id,
        )
        rows = self.session.execute(stmt_check).scalars().all()
        return rows

    def register_engine_config(self):
        # check if is registered already

        rows = self.check_engine_config_id_is_registered()
        if len(rows) == 0:
            try:
                self.logger.info(
                    f"registration {self.engine_postfix} : engine_configs table"
                )
                stmt = insert(EngineConfigs).values(
                    engine_id=self.engine_v_id,
                    name=self.engine_postfix,
                    results_postfix=self.results_postfix,
                    comment=self.comment,
                    density_model_id=self.density_model_id,
                    is_release=True
                )
                self.session.execute(stmt)
                self.session.commit()
                self.engine_config_id = self.check_engine_config_id_is_registered()
            finally:
                self.session.close()
            self.logger.info(
                f"successfully registered {self.engine_postfix} : engine_configs table"
            )
            return self.engine_config_id[0]
        else:
            engine_config_id = rows[0]
            self.logger.warning(
                f"engine {self.engine_postfix} is already registered in engine_configs table!\n"
                f"id = {engine_config_id}. Registration skipped"
            )
            self.engine_config_id = engine_config_id
            return engine_config_id

    def set_engine_as_actual(self, combination):
        client_id_stm = select(Clients.id).where(Clients.name == combination.client)
        breed_id_stm = select(BreedTypes.id).where(
            BreedTypes.name == combination.breed_type
        )
        gender_id_stm = select(Genders.id).where(Genders.name == combination.gender)

        client_id = self.session.execute(client_id_stm).scalars().one()
        breed_id = self.session.execute(breed_id_stm).scalars().one()
        gender_id = self.session.execute(gender_id_stm).scalars().one()

        setting_as_actual_query = (
            update(ActualClientsInfoTable)
            .where(
                ActualClientsInfoTable.client_id == client_id,
                ActualClientsInfoTable.breed_type_id == breed_id,
                ActualClientsInfoTable.gender_id == gender_id,
            )
            .values(engine_config_id=self.engine_config_id)
        )

        self.session.execute(setting_as_actual_query)
        self.session.commit()
        self.session.close()

        self.logger.info(
            f"\nfor {combination.client}|{combination.breed_type}|{combination.gender}"
            f" setted up {self.engine_config_id} engine_config_id"
        )

    @staticmethod
    def get_id_by_name(session, name: str, entity) -> Optional[int]:
        """
        get Postgres table id by name field in table entity (if name is exists for entity and unique)

        :param session:
        :param name:
        :param entity:
        :return:
        """
        rows = session.execute(
            session.query(entity).where(entity.name == name)).scalars().all()
        if len(rows) == 0:
            return None
        if len(rows) > 1:
            print(colorstr('red', f'Execute response has more then 1 output. The first one only will be returned'))
        return rows[0].id

    # @staticmethod
    def get_client_bree_gender_combo_entity(self, session, client: str, breed_type: str, gender: str):
        entities = session.execute(
            session.query(ActualClientsInfoTable).join(Clients, Clients.id == ActualClientsInfoTable.client_id)
            .join(BreedTypes, BreedTypes.id == ActualClientsInfoTable.breed_type_id)
            .join(Genders, Genders.id == ActualClientsInfoTable.gender_id).where(and_(Clients.name == client,
                                                                                      BreedTypes.name == breed_type,
                                                                                      Genders.name == gender)
                                                                                 )).scalars().all()
        if len(entities) == 0:
            client_id = self.get_id_by_name(session, client, Clients)
            breed_type_id = self.get_id_by_name(session, breed_type, BreedTypes)
            gender_id = self.get_id_by_name(session, gender, Genders)
            entity = ActualClientsInfoTable(
                client_id=client_id,
                breed_type_id=breed_type_id,
                gender_id=gender_id
            )
            session.add(entity)
            session.commit()
        else:
            entity = entities[0]

        return entity

    def add_in_release_history(self, engine_v_id: int):
        session = sessionmaker(bind=postgres_engine)()
        cl_br_g_entity = self.get_client_bree_gender_combo_entity(session,
                                                                  client=self.combination.client,
                                                                  breed_type=self.combination.breed_type,
                                                                  gender=self.combination.gender)

        available_combinations = [cl_br_g_entity.id]

        engine_entity = session.execute(
            session.query(EngineConfigs).where(EngineConfigs.id == engine_v_id)).scalars().one()
        engine_entity.is_release = True
        if engine_entity.available_combinations is None:
            engine_entity.available_combinations = [cl_br_g_entity.id]
        else:
            engine_entity.available_combinations = list(set(available_combinations + [cl_br_g_entity.id]))
        session.commit()
        self.logger.info('added in release history')

    def run(self):
        self.get_engine_version_id()
        engine_config_id = self.register_engine_config()
        return engine_config_id


if __name__ == "__main__":
    db_components = DBEnginesComponent(
        logger=build_logger(file_name=f"{Path(__file__)}", save_log=False),
        engine_v_name="v4.0.0.00",
        results_postfix="",
        comment="test",
        density_model_id=175,
        engine_postfix="_test_postfix"
    )
    db_components.run()
