from bdm2.utils.process_data_tools.components.birdoo_filter import Filter


class FilenameManager:
    @staticmethod
    def get_res_fname(feature, engine_postfix, label):
        return "{}_res_df{}{}.csv".format(feature, engine_postfix, label)

    @staticmethod
    def get_res_fname_from_filter(feature: str,
                                  engine_postfix: str,
                                  filters: Filter,
                                  add_client_name: bool = False):

        add_houses_names = True
        add_device_name = False

        n_key_words = 0
        if len(filters.houses) > 3:
            add_houses_names = False
        else:
            n_key_words += len(filters.houses)

        if (n_key_words + len(filters.devices) < 5):
            add_device_name = True

        return "{}_res_df{}{}.csv".format(feature, engine_postfix, filters.generate_label(
            farm=add_client_name,
            flock=False,
            house=add_houses_names,
            device=add_device_name))
