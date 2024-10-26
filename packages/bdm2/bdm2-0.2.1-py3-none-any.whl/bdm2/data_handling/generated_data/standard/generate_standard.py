import json
from pathlib import Path
import numpy as np
import pandas as pd

from bdm2.constants.global_setup.server_paths import standards_dir
from bdm2.constants.global_setup.data import standards_match_columns, WEIGHTS_SRC_TYPE
from bdm2.data_handling.generated_data.common_components.generated_curve_params import GeneratedWeightsParams
from bdm2.data_handling.generated_data.standard.components.standard import Standard
from bdm2.data_handling.generated_data.common_components.targets_generator import TargetsCombiner
from bdm2.logger import build_logger
from brddb.utils.common import colorstr
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


class StandardGenerator(GeneratedWeightsParams):
    """
    Class for generating and updating bird weight standards.

    Attributes:
    ----------
    filter : Filter
        A filter used to generate standards based on client data.
    update_all : bool
        Flag to indicate whether to update all client standards.
    update_default : bool
        Flag to indicate whether to update the default standard.
    server_standards_dir : str
        Directory where the standards will be saved.
    logger : Logger
        Logger instance for logging messages and errors.
    """

    def __init__(self, filter, update_all: bool, update_default: bool):
        """
        Initializes the StandardGenerator with the given filter and flags.

        Parameters:
        ----------
        filter : Filter
            Filter object used for generating standards.
        update_all : bool
            If True, all client standards will be updated.
        """
        self.filter = filter
        self.update_all = update_all
        self.update_default = update_default
        self.server_standards_dir = standards_dir
        self.logger = build_logger(Path(__file__), save_log=False)

    @property
    def unnecessary_clients(self):
        """
        Returns a list of clients to be skipped during the standard generation process.

        Returns:
        -------
        List[str]
            List of client names to exclude.
        """
        return ["CGBRBF", "DEFAULT", "Default", "Client"]

    def generate_all_combos_filters(self):
        """
        Generates filters for all client combinations, excluding unnecessary clients.

        This method generates filters for each client, breed type, and gender,
        while excluding clients that are marked as unnecessary.

        Returns:
        -------
        List[Filter]
            A list of filters for all valid client combinations.
        """
        clients_info = self.actual_clients_storage.actual_info.dropna(subset=['standard_weights'])
        for skipping_client in self.unnecessary_clients:
            clients_info = clients_info[clients_info.client != skipping_client]
            self.logger.info(colorstr('red', f'{skipping_client} was excluded'))

        self.logger.info(f"{'':-^70}")
        self.logger.info(f'update standards for {len(clients_info)} combinations')

        filters4all = []
        for _, row in clients_info.iterrows():
            filters = Filter()
            filters.clients = [row['client']]
            filters.breed_types = [row['breed_type']]
            filters.genders = [row['gender']]
            filters.ages = list(np.arange(0, self.max_extrapolated_day))
            filters4all.append(filters)
        return filters4all

    def process_standard_generation(self, filters, client_info, output_format, output_weights_format):
        """
        Processes standard generation for each client group and updates actual_clients_info.

        This method retrieves weight data, generates standards, and updates the client
        information in the database for each combination of filters.

        Parameters:
        ----------
        filters : Filter
            Filter object containing client, breed, and gender data.
        client_info : pd.DataFrame
            DataFrame containing client information.
        output_format : Any
            Format for the output data.
        output_weights_format : Any
            Format for the output weight data.
        """
        likely_weights = self.src_weights_storage.get_target_weights(
            WEIGHTS_SRC_TYPE['Likely_targets'],
            weights_postfix=None,
            filters=filters,
            output_df_format=None
        )
        houses_df = self.src_devices_storage.get_houses(filters)
        likely_weights = TargetsCombiner.match_device_info(likely_weights, houses_df)

        for client_label, client_group in likely_weights.groupby(standards_match_columns):
            client_params = {col: client_label[i] for i, col in enumerate(standards_match_columns)}
            standard_folder = "_".join(map(str, client_params.values()))

            self.logger.info(colorstr('blue', f"Generating standard for {standard_folder}"))
            client_dst_dir = str(Path(self.server_standards_dir) / standard_folder)

            standard = self.generate_standard(client_group, client_dst_dir, output_weights_format, filters)
            self.update_actual_clients_info(standard, client_label, client_info, output_format)

    def generate_standard(self, client_group, client_dst_dir, output_weights_format, filters):
        """
        Generates and saves the standard for a specific client group.

        Parameters:
        ----------
        client_group : pd.DataFrame
            DataFrame containing the weight data for the client group.
        client_dst_dir : str
            Directory where the generated standard will be saved.
        output_weights_format : Any
            Format for the weight data in the output.
        filters : Filter
            Filter object used to refine the data.

        Returns:
        -------
        pd.DataFrame
            The generated standard as a DataFrame.
        """
        st = Standard(logger=self.logger)
        standard = st.generate_standard(
            weights_df=client_group,
            dst_dir=client_dst_dir,
            age_column=output_weights_format.age,
            house_index_columns=output_weights_format.house_index.get_columns(),
            weight_column=output_weights_format.weight_value,
            title=client_dst_dir,
            vis=False,
            filters=filters
        )
        return standard

    def update_actual_clients_info(self, standard, client_label, client_info, output_format):
        """
        Updates actual_clients_info after generating a new standard.

        Prompts the user for confirmation before updating the client info.

        Parameters:
        ----------
        standard : pd.DataFrame
            The newly generated standard to be saved.
        client_label : tuple
            A tuple containing client identifiers (e.g., client, breed type, gender).
        client_info : pd.DataFrame
            The DataFrame containing client information to be updated.
        output_format : Any
            Format used to update actual_clients_info.
        """
        self.logger.info(colorstr('magenta', f'Update standard for {client_label} in actual_clients_info (y/n)'))
        a = input()
        if a.lower() == 'y':
            self.upsert_actual_clients_table(
                actual_clients_info=self.actual_clients_storage,
                client_label=client_label,
                ac_sl_st_format=output_format,
                update_actual_clients_info=True,
                ac_cl_st=client_info,
                standard=standard
            )

    @staticmethod
    def upsert_actual_clients_table(actual_clients_info, client_label, ac_sl_st_format,
                                    update_actual_clients_info: bool, ac_cl_st, standard):
        """
        Updates the actual_clients_info table with the generated standard.

        Parameters:
        ----------
        actual_clients_info : pd.DataFrame
            The actual_clients_info DataFrame to be updated.
        client_label : tuple
            The client identifier tuple.
        ac_sl_st_format : Any
            Format used for the update.
        update_actual_clients_info : bool
            Flag to indicate whether to update actual_clients_info.
        ac_cl_st : pd.DataFrame
            DataFrame containing client information.
        standard : pd.DataFrame
            The generated standard to be updated in the table.
        """
        actual_clients_info.loc[client_label, ac_sl_st_format.standard_weights] = standard.to_json()
        print(colorstr('blue', f"standard_weights for {client_label} were updated"))
        if update_actual_clients_info:
            ac_cl_st.update(actual_clients_info.reset_index(), ac_sl_st_format)
            print(f"ActualClientsStorage was updated")
        print('Generation standards finished')

    def download_all_standards(self, actual_clients):
        """
        Downloads all standards from the actual_clients storage.

        Parameters:
        ----------
        actual_clients : pd.DataFrame
            DataFrame containing all actual client data with standard weights.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing all combined standards.
        """
        all_combos_df = pd.DataFrame()
        all_combos_df.index = ([i for i in range(0, 60)])
        counter = 0
        for i, row in self.actual_clients_storage.actual_clients.iterrows():
            counter += 1
            stand = row['standard_weights']
            if row["client"] in ["Default", "DEFAULT"]:
                continue

            if isinstance(stand, str):
                standard = pd.DataFrame(json.loads(stand))
            else:
                standard = pd.read_json(stand)
            curr_standard_weight = standard.Weights
            if len(curr_standard_weight) < 59:
                continue

            try:
                all_combos_df[counter] = curr_standard_weight.values
            except Exception as Ex:
                print(Ex)

        return all_combos_df

    def run(self):
        """
        Main method to run the standard generation process.

        Depending on the flags, this method will either update all standards, update the default standard,
        or update standards for specific client breed type gender.
        """
        if self.update_all:
            all_combo_filters = self.generate_all_combos_filters()
            for filters in all_combo_filters:
                client_info = self.actual_clients_storage.get(filters=filters)
                client_info = client_info.set_index(standards_match_columns)
                output_format = self.actual_clients_storage.output_default_format
                output_weights_format = self.src_weights_storage.output_default_format
                self.process_standard_generation(filters, client_info, output_format, output_weights_format)
        elif self.update_default:
            ac_info_df = self.actual_clients_storage.actual_info
            ac_info_df = ac_info_df.dropna(subset='standard_weights')

            res_df = self.download_all_standards(ac_info_df)
            st = Standard(logger=self.logger)
            default_standard = st.generate_default_standard(res_df)
            st.upload_standard_into_db(client='DEFAULT',
                                       breed_type='DEFAULT',
                                       gender='DEFAULT',
                                       new_standard=default_standard)
        else:
            client_info = self.actual_clients_storage.get(filters=self.filter)
            client_info = client_info.set_index(standards_match_columns)
            output_format = self.actual_clients_storage.output_default_format
            output_weights_format = self.src_weights_storage.output_default_format
            self.process_standard_generation(self.filter, client_info, output_format, output_weights_format)


if __name__ == '__main__':
    f = Filter()
    update_all_combinations = False
    update_default = False
    sg = StandardGenerator(filter=f, update_all=update_all_combinations)
    sg.run()
