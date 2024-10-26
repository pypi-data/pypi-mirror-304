import pandas as pd

from bdm2.constants.global_setup.data import house_match_columns
from bdm2.logger import build_logger
from bdm2.utils.mongo.connector import MongoDBConnection, MongoCollection
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter

from pathlib import Path

from bdm2.utils.schemas.models.storages.devices.postgres_devices_storage import PostgresDevicesStorage


class MongoFilter:
    """
    A utility class to filter MongoDB collections for specific client, breed, and gender combinations.

    Attributes:
        mongo_bird_id: The bird ID fetched from MongoDB.
        mongo_client_id: The client ID fetched from MongoDB.
        b_filter: An instance of the Filter class to filter client, breed, and gender.
        initial_values: A dictionary holding the initial values for client, breed, and gender.
        logger: A logger instance to track operations and errors.

    Methods:
        get_mongo_combination_names(): Fetches the MongoDB client and bird IDs based on the initial values.
    """

    def __init__(self, b_filter: Filter):
        """
        Initializes the MongoFilter class with client, breed, and gender information.

        Args:
            b_client: The client name or code to filter.
            b_breed: The breed type to filter (e.g., 'Cobb').
            b_gender: The gender to filter (e.g., 'male').
        """
        self.mongo_bird_id = None
        self.mongo_client_id = None
        # self.b_filter = Filter(clients=[b_client], breed_types=[b_breed], genders=[b_gender])
        self.initial_values = b_filter
        self.logger = build_logger(Path(__file__), save_log=False)

    def get_mongo_combination_data(self):
        """
        Fetches MongoDB client and bird IDs based on the initial client, breed, gender, and cycle-house values.

        - If the breed type is 'Cobb', it automatically converts it to uppercase.
        - If the filter contains cycle-house information, it fetches the birdId using the cycle-house-code from the MongoDB 'cycles' collection.
        - If no cycle-house information is provided, the birdId is determined solely from the MongoDB 'birds' collection.

        Logs errors if no matching client or bird is found in the MongoDB collections.

        Returns:
            None if no client or bird is found; otherwise, updates the mongo_bird_id and mongo_client_id attributes.
        """

        if 'Cobb' in self.initial_values.breed_types:
            self.initial_values.breed_types[0] = self.initial_values.breed_types[0].upper()

        with MongoDBConnection() as db:
            collection_partners = MongoCollection(db, "businesspartners")
            collection_birds = MongoCollection(db, "birds")
            collection_cycles = MongoCollection(db, "cycles")

            # Fetch client ID
            all_partners = collection_partners.find_all_documents({'bpCode': self.initial_values.clients[0]})
            if all_partners.empty:
                self.logger.error(f"No business partner found for: {self.initial_values.clients[0]}")
                return None
            self.mongo_client_id = str(all_partners.loc[0, 'ownerId'])

            # if there is cycle-houses - check collection cycles in mongo
            # and define bird_id from it for ch
            if len(self.initial_values.cycles) and len(self.initial_values.houses):
                devices = (
                    PostgresDevicesStorage()
                    .get_devices(filters=self.initial_values)
                    .groupby(house_match_columns, as_index=False)
                    .first()
                )
                self.logger.warning(f"defined cycle-house-code in filter: {devices['cycle_house_id'][0]}\n"
                                 f"will check birdId in 'cycles' collection")
                get_from_mongo_this_cycle = collection_cycles.find_document({"cycleId": devices['cycle_house_id'][0]})
                self.mongo_bird_id = get_from_mongo_this_cycle["birdId"]

                if self.mongo_bird_id:
                    # Fetch bird ID
                    birds_df = collection_birds.find_all_documents(
                        query={'birdType': self.initial_values.breed_types[0],
                               'birdSex': self.initial_values.genders[0],
                               'birdId': self.mongo_bird_id,
                               'standardType': 'Market'},
                        gby={'birdType': 1, 'birdSex': 2, 'birdId': 3, 'ownerId': 4,
                             'standardType': 5, 'birdWtStd': 6}
                    )
                else:
                    birds_df = collection_birds.find_all_documents(
                        query={'birdType': self.initial_values.breed_types[0],
                               'birdSex': self.initial_values.genders[0],
                               'standardType': 'Market'},
                        gby={'birdType': 1, 'birdSex': 2, 'birdId': 3, 'ownerId': 4,
                             'standardType': 5, 'birdWtStd': 6}
                    )
                if birds_df.empty:
                    self.logger.error(f"No bird found for: {self.initial_values}")
                    return None

                self.mongo_bird_id = birds_df.loc[0, 'birdId']
                self.logger.info(f"Bird ID found: {self.mongo_bird_id}")
                return birds_df

    def get_market_standard(self):
        """
        Fetches the market standard for the bird from the MongoDB 'birds' collection.

        Calls get_mongo_combination_data() to retrieve bird data from the MongoDB collection, including birdId,
         birdType, birdSex, and standardType.
        Logs this information and extracts the bird weight standard ('birdWtStd') from the data.

        ! input filter must have cycle-house info for getting correct birdId !
        Returns:
            A pandas DataFrame containing the bird weight standard with the 'age' as the index and 'Weights' as the column name.
        """
        assert len(self.initial_values.cycles) and len(self.initial_values.houses), 'contains input filter ' \
                                                                                    'no provides info about ' \
                                                                                    'cycle-house!'
        df = self.get_mongo_combination_data()
        self.logger.warning(
            f"\nbirdId: {df['birdId'].values}\n"
            f"birdType: {df['birdType'].values}\n"
            f"birdSex: {df['birdSex'].values}\n"
            f"standardType: {df['standardType'].values}\n"
        )
        standard = pd.DataFrame(df["birdWtStd"][0], columns=['Weights'])
        standard.index.name = "age"

        return standard


if __name__ == "__main__":
    filters = Filter(clients=["CGTHBG"], breed_types=["Arbor Acres"], genders=["male"],
                     cycles=['Cycle 1'], houses=['A8'], farms=['BFI B farm'])

    save_folder = r"\\Datasets\chikens\MHDR_Chicken\sources\DensityModels\union\Josephine\KXSAAF\Ross_mix"


    save_f_name = f"{filters.clients[0]}_{filters.breed_types[0]}_{filters.genders[0]}_market_standard.csv"
    mongo_filter = MongoFilter(filters)
    ch_market_standard = mongo_filter.get_market_standard()
    if mongo_filter.mongo_bird_id:
        mongo_filter.logger.info(f"Bird ID: {mongo_filter.mongo_bird_id}")
    save_fp = str(Path(save_folder) / save_f_name)
    ch_market_standard.to_csv(save_fp, sep=';')
    print(f"saved {save_fp}")