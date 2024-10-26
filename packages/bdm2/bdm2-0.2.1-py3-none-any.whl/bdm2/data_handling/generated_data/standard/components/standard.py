import os
from datetime import datetime
from typing import List

import pandas as pd
import yaml
from brddb.models.postgres import BreedTypes, Genders
from matplotlib import pyplot as plt
from pathlib import Path, PurePath

from brddb.utils.common import colorstr
from brdpm.utils.plots import smooth_standard_by_adg_and_plot
from sqlalchemy.orm import sessionmaker

from bdm2.constants.global_setup.data_columns import (
    mean_w, std, min_w, max_w, adg, adg_max, adg_min
)
from bdm2.constants.global_setup.env import standards_bot_token, standards_bot_chat_id
from bdm2.constants.global_setup.server_paths import standards_dir
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.data_handling.generated_data.chicken_weights.harvest_day.new_piwfha.components.api_wrapper import (
    APIWrapper, get_target_weights
)
from bdm2.utils.schemas.components.sqlhelpers.helpers import upsert_entity, get_id_by_name
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.storages.clients_storage import ActualClientsInfoTable, Clients
from bdm2.utils.telegram_bot.birdoo_telebot import telebot

# Configuration
__config_path__ = os.path.join(os.getenv('MHDR_CHICKEN'), r'BIRDOO_IP\TelegramBot\sources\config.yaml')


class Standard:
    standard_columns = [mean_w, std, min_w, max_w, adg, adg_min, adg_max]

    def __init__(self, logger):
        self.logger = logger
        self.server_standards_dir = standards_dir

        # Load configuration
        with open(__config_path__, 'r') as config_file:
            config = yaml.safe_load(config_file)
        self.token = standards_bot_token
        self.stand_bot_chat_id = standards_bot_chat_id
        self.bot = telebot.TeleBot(self.token)

    def targets_completeness_check(self, weights_df: pd.DataFrame, filters: Filter):
        """
        Проверяет наличие целевых данных для всех циклов и домов.
        """
        combinations = weights_df[['breed_type', 'gender', 'farm', 'cycle', 'house']].drop_duplicates().reset_index(
            drop=True)
        targets_df = get_target_weights(filters=filters, src_type='Targets',
                                        weights_postfix=weights_df.weight_postfix.unique().tolist()[0])
        list_dropped = []

        for _, row in combinations.iterrows():
            farm, cycle, house = row['farm'], row['cycle'], row['house']
            target_ages = targets_df.loc[
                (targets_df.farm == farm) & (targets_df.cycle_house == cycle) & (targets_df.house == house), 'age']

            if target_ages.max() <= 21:
                self.logger.warning(
                    f"{farm} {cycle} {house} has no targets beyond 21 days. Dropped from sample for standard generation.")
                weights_df = weights_df[
                    (weights_df.farm != farm) | (weights_df.cycle != cycle) | (weights_df.house != house)]
                list_dropped.append(f'{farm}_{cycle}_{house}: max targets age = {target_ages.max()}')

        if not list_dropped:
            self.logger.info("All cycle-houses have full targets. No data was deleted.")
        return weights_df, list_dropped

    def generate_comparing_graphic(self, smooth_output: pd.DataFrame, save_figpath: str, filters: Filter):
        """
        Генерирует график для сравнения текущих стандартов с новыми.
        """

        cr = r"\\Datasets\chikens\configs\credentials\brddb_api\nastya_user.yaml"
        api = APIWrapper(creds_path=cr)
        # api.postprocess = True
        # api.end_point = r'api/v1/views/actual-clients-info-storage'

        filters.ages = []
        filters = api.filter2birdoofilter(filters)

        combination_info = api.perform_get_request(url=api.actual_clients_info_endpoint,
                                                   params=filters)
        output_data = combination_info.json()
        combination_info= pd.DataFrame(output_data)
        combination_info = combination_info.loc[
            (combination_info.client_name.isin(filters.clients)) &
            (combination_info.breed_type.isin(filters.breed_types)) &
            (combination_info.gender.isin(filters.genders))
                                                ]
        if combination_info['standard_weights'][0] is not None:
            current_actual_standard = pd.read_json(combination_info['standard_weights'][0])['Weights']
            fig, ax = plt.subplots(1, 1, figsize=(8, 5), dpi=100)
            ax.set_title("Standard Changes:")
            ax.plot(smooth_output.index, smooth_output.Weights.values, color='blue', label='Smoothed Standard', linewidth=1)
            ax.plot(current_actual_standard.index, current_actual_standard.values, color='red', label='Old Standard',
                    linewidth=1)
            fig.legend(loc='upper left')

            save_fp = str(Path(save_figpath).parent / 'compare_historic_and_smoothed_std.png')
            fig.savefig(save_fp, pad_inches=0.1)
            return save_fp
        else:
            return None

    def generate_standard(self, weights_df: pd.DataFrame, dst_dir: str, age_column: str, weight_column: str,
                          house_index_columns: List[str], title: str, vis: bool, filters: Filter):
        """
        Генерация стандарта для Birdoo.
        """
        # Проверка полноты целевых данных
        weights_df, list_dropped = self.targets_completeness_check(weights_df, filters)

        # Вычисление стандартов
        grouped_weights = weights_df.groupby(age_column)
        standard_mean = grouped_weights[weight_column].mean().rename(mean_w)
        standard_std = grouped_weights[weight_column].std().rename(std) if len(
            weights_df[house_index_columns].drop_duplicates()) >= 2 else None
        standard_min = grouped_weights[weight_column].min().rename(min_w)
        standard_max = grouped_weights[weight_column].max().rename(max_w)

        adg_values = self.calculate_adg(standard_mean, standard_min, standard_max)

        # Создание директории для сохранения
        dst_dir = Path(dst_dir) / datetime.today().strftime('%Y-%m-%d')
        dst_dir.mkdir(parents=True, exist_ok=True)

        # Сохранение списка удаленных домов и циклов
        self.save_dropped_cycles(list_dropped, dst_dir)

        # Генерация и сглаживание стандартов
        standard = self.create_standard_dataframe(standard_mean, standard_std, standard_min, standard_max, adg_values,
                                                  house_index_columns)

        time_idx_column = age_column
        target_column = standard_mean.name
        min_err_age: int = 30
        max_err_age: int = 50
        standard_series = standard.set_index([time_idx_column])[target_column]
        output = smooth_standard_by_adg_and_plot(standard_series, 'colname', min_err_age, max_err_age)
        smoothed_by_adg_standard_mean = pd.DataFrame(output['smooth_output'])['filtered_by_gain_adjusted_series']
        save_figpath = PurePath(dst_dir, os.path.basename(dst_dir) + '_' + str(datetime.today()) + '.png')
        output['fig'].savefig(save_figpath, bbox_inches='tight', pad_inches=0.1)

        standard.Weights = smoothed_by_adg_standard_mean
        # Сохранение и визуализация данных
        self.save_and_visualize_standard(standard, weights_df,
                                         dst_dir, age_column, weight_column, title, vis,
                                         filt=filters, adg_g_fig_path=save_figpath)

        return standard

    def calculate_adg(self, mean: pd.Series, min_val: pd.Series, max_val: pd.Series):
        """
        Вычисляет средний дневной прирост (ADG) для стандарта.
        """
        adg = (mean - mean.iloc[0]) / mean.index
        adg[0] = 0
        adg.name = 'ADG'
        adg_min = (min_val - min_val.iloc[0]) / min_val.index
        adg_min[0] = 0
        adg_min.name = 'ADG_min'
        adg_max = (max_val - max_val.iloc[0]) / max_val.index
        adg_max[0] = 0
        adg_max.name = 'ADG_max'
        return adg, adg_min, adg_max

    def save_dropped_cycles(self, list_dropped: List[str], dst_dir: Path):
        """
        Сохраняет информацию о пропущенных циклах и домах в файл.
        """
        dropped_fp = dst_dir / 'dropped_cycle_houses.txt'
        with open(dropped_fp, "w") as file:
            file.write("\n".join(list_dropped))
        self.logger.info(f"Saved dropped cycle-houses to {dropped_fp}")

    def create_standard_dataframe(self, mean: pd.Series, std: pd.Series, min_val: pd.Series, max_val: pd.Series,
                                  adg_values: tuple, house_index_columns: List[str]):
        """
        Создает DataFrame для стандарта.
        """
        if std is not None:
            standard_df = pd.concat([mean, std, min_val, max_val, *adg_values], axis=1).reset_index()
        else:
            standard_df = pd.concat([mean, min_val, max_val, *adg_values], axis=1).reset_index()
            self.logger.warning(f"Standard deviation not calculated, only one house present.")
        return standard_df

    def save_and_visualize_standard(self, standard: pd.DataFrame, weights_df: pd.DataFrame, dst_dir: Path,
                                    age_column: str, weight_column: str, title: str, vis: bool,
                                    filt, adg_g_fig_path):
        """
        Сохраняет и визуализирует данные стандарта.
        """
        # Генерация стандартов и изображений
        raw_path = dst_dir / f"raw_{datetime.today().strftime('%Y-%m-%d')}.csv"
        image_path = dst_dir / f"standard_{datetime.today().strftime('%Y-%m-%d')}.png"

        standard_path = dst_dir / f"standard_{datetime.today().strftime('%Y-%m-%d')}.csv"
        standard.to_csv(standard_path, sep=';', index=False)
        self.logger.info(f"Standard saved as {standard_path}")

        # Визуализация
        plt.figure()

        save_figpath = str(PurePath(dst_dir, os.path.basename(dst_dir) + '_' + datetime.today().strftime('%Y-%m-%d') + '.png'))
        compare_gr_path = self.generate_comparing_graphic(standard, save_figpath, filt)

        self.send_graphic2chat(path_to_photo=[compare_gr_path, adg_g_fig_path],
                               message=os.path.basename(PurePath(dst_dir).parent))

    def generate_default_standard(self, all_combos_df):

        standard_mean = all_combos_df.mean(axis=1)
        standard_mean.name = 'Weights'

        standard_mean_min = all_combos_df.min(axis=1)
        standard_mean_min.name = 'min'
        standard_mean_max = all_combos_df.max(axis=1)
        standard_mean_max.name = 'max'
        adg = (standard_mean - standard_mean[0]) / standard_mean.index
        adg[0] = 0
        adg.name = 'ADG'
        adg_min = (standard_mean_min - standard_mean_min[0]) / standard_mean.index
        adg_min[0] = 0
        adg_min.name = 'ADG_min'
        adg_max = (standard_mean_max - standard_mean_max[0]) / standard_mean.index
        adg_max[0] = 0
        adg_max.name = 'ADG_max'

        standard_new = pd.concat([standard_mean, standard_mean_min, standard_mean_max, adg, adg_min, adg_max],
                                 axis=1).reset_index()
        standard_new.rename(columns={'index': 'age'}, inplace=True)

        return standard_new
    @staticmethod
    def upload_standard_into_db(new_standard: pd.DataFrame,
                                client: str, breed_type: str, gender: str):
        session = sessionmaker(bind=postgres_engine)()
        entity = ActualClientsInfoTable()
        entity.client_id = get_id_by_name(session, name=client, entity=Clients)

        entity.breed_type_id = get_id_by_name(session, name=breed_type, entity=BreedTypes)
        entity.gender_id = get_id_by_name(session, name=gender, entity=Genders)
        statndard = new_standard.to_json()
        entity.standard_weights = statndard  # statistics.reset_index().to_json()

        upsert_entity(session, entity, update_on_conflict=True, update_nones=True)
        session.commit()
        print(colorstr('blue', f' stadard for {client, breed_type, gender} was updated'))
    def send_graphic2chat(self, path_to_photo: list, message):
        self.bot.send_message(text=message, chat_id=self.stand_bot_chat_id)

        for picture_fp in path_to_photo:
            if picture_fp is None:
                self.bot.send_message(text=f'❌ no old standard for {message}', chat_id=self.stand_bot_chat_id)
                continue
            photo = open(picture_fp, 'rb')
            self.bot.send_photo(self.stand_bot_chat_id, photo)
