from dataclasses import dataclass
from typing import Dict

import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'boto3.Session',
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()

Session = checker.get_module('boto3.Session')
import io
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from brddb.models.postgres import EngineConfigs, DensityModels
from bdm2.constants.global_setup.data import standards_match_columns
from bdm2.constants.global_setup.env import AWS_ACCESS_KEY, AWS_SECRET_KEY
from bdm2.logger import build_logger
from bdm2.utils.process_data_tools.components.brdmath.simple_net_converter import SimpleNet2Keras, check_inputs
from bdm2.utils.process_data_tools.components.centering.mass_by_err import interpolate_and_smooth_coefs, calc_err
from bdm2.utils.process_data_tools.components.birdoo_filter import Filter
from bdm2.utils.schemas.connection import postgres_engine
from bdm2.utils.schemas.models.postgres_actual_clients_info_storage import (
    PostgresActualClientsInfoStorage,
)

import warnings
from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)


def get_s3_bucket() -> Session.resource:
    session = Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="us-east-1",
    )
    return session.resource("s3").Bucket("zbage-trainer")


class MassActualization:
    def __init__(self, dataset_for_actualization: pd.DataFrame, do_centering: bool):

        self.dataset_for_actualization = dataset_for_actualization
        self.logger = build_logger(file_name=f"{Path(__file__)}", save_log=False)
        self.do_centering = do_centering

    @dataclass
    class ColName:
        input_volume_column: str = r"volume_norm_corr_mean"
        models_volume_column: str = r"volume_norm_corr_run"
        default_density_column: str = r"day_average_density_mean"
        default_mass_column: str = r"mass_corr_mean"
        predicted_density_column: str = r"density_predicted"
        predict_mass_column: str = r"centered_mass"
        err_on_new_density_no_centering: str = r"new_error_no_centering"
        target_w_column: str = r"adjusted_weight"
        day_column = r"daynum"

    @property
    def root_bucket(self) -> Session.resource:
        # Get s3 session
        return get_s3_bucket()

    def _download_from_s3(self, key: str):
        obj = self.root_bucket.Object(key)
        response = obj.get()
        data = response['Body'].read()

        return data

    def load_model(self,
                   model_key: str) -> SimpleNet2Keras:

        # Get model, convert bite to lines and create model resource
        model_data = self._download_from_s3(model_key)
        model_lines = model_data.decode('utf-8').splitlines()
        density_model = SimpleNet2Keras(model_lines)
        return density_model

    def load_c_vectors(self,
                       c_vectors_key: str,
                       b_filter: Filter) -> pd.Series:

        # Get c_vectors
        csv_data = self._download_from_s3(c_vectors_key)
        c_vectors_df = pd.read_csv(io.BytesIO(csv_data), sep=';')

        # Define one for target_combination
        target_c_vestors = c_vectors_df.loc[
            (c_vectors_df["client"] == b_filter.clients[0]) &
            (c_vectors_df["breed_type"] == b_filter.breed_types[0]) &
            (c_vectors_df["gender"] == b_filter.genders[0])
            ].reset_index(drop=True)

        # Transform to models necessary format
        target_c_vestors.drop(columns=standards_match_columns, inplace=True)
        tg_cv = target_c_vestors.stack().reset_index()
        tg_cv = tg_cv.drop(columns=['level_0'])
        tg_cv.set_index(['level_1'], inplace=True)

        return tg_cv

    def load_feature_mask(self,
                          feature_mask_key: str) -> list:
        feature_mask_data = self._download_from_s3(feature_mask_key)

        _fm = pd.read_csv(io.BytesIO(feature_mask_data), sep=';', header=None)
        _fm = _fm.transpose()
        _fm = _fm.set_index(1)[0].sort_index()
        return list(_fm.values)

    def center_dataset(self,
                       not_centered_target_combo_df: pd.DataFrame) -> pd.DataFrame:
        # centering mass by error
        smooth_window = 5

        predicted_mean = not_centered_target_combo_df.groupby(
            self.ColName.day_column
        )[self.ColName.default_mass_column].mean()

        target_mean = not_centered_target_combo_df.groupby(
            self.ColName.day_column
        )[self.ColName.target_w_column].mean()

        corr_coefs = target_mean / predicted_mean
        corr_coefs = interpolate_and_smooth_coefs(corr_coefs,
                                                  smooth_window=smooth_window)

        centered_df = not_centered_target_combo_df.copy()
        # estimate tg combo new mass \ err
        centered_df[self.ColName.predict_mass_column] = \
            centered_df[self.ColName.default_mass_column].values * \
            corr_coefs[centered_df[self.ColName.day_column].values].values

        # corrected errors
        centered_df[f'centered_error'] = \
            calc_err(centered_df,
                     pred_col=self.ColName.predict_mass_column,
                     target_col=self.ColName.target_w_column)
        # Rename columns 
        centered_df.rename(
            columns={self.ColName.default_mass_column: f'{self.ColName.default_mass_column}_not_centered'},
            inplace=True)
        centered_df.rename(columns={self.ColName.predict_mass_column: self.ColName.default_mass_column}, inplace=True)

        self.logger.info(f"centering mass done")

        return centered_df

    def get_actual_density_name(self, group: pd.DataFrame):

        session = sessionmaker(bind=postgres_engine)()
        stmt_density_id = select(EngineConfigs.density_model_id).where(
            EngineConfigs.name == group['engine_config_name'].values[0])
        actual_density_id = session.execute(stmt_density_id).scalars().one()
        stmt_density_name = select(DensityModels.name).where(DensityModels.id == actual_density_id)
        actual_density_name = session.execute(stmt_density_name).scalars().one()
        session.close()

        self.logger.info(f"actual density model name: {actual_density_name}")

        return actual_density_name

    @staticmethod
    def generate_filter(client: str, breed: str, gender: str) -> Filter:

        fltr = Filter()
        fltr.clients = [client]
        fltr.breed_types = [breed]
        fltr.genders = [gender]

        return fltr

    @staticmethod
    def _generate_models_source_keys(actual_density_name: str) -> Dict[str, str]:

        return {"extra_features_key_": rf'train_output/{actual_density_name}'
                                       r'/module/zbage_extra_features.csv',

                "model_key_": rf'train_output/{actual_density_name}/module'
                              r'/OtherData/prediction_nets/zbage.net',

                "feature_mask_key_": rf'train_output/{actual_density_name}'
                                     r'/module/OtherData/prediction_nets/featuremask.txt'}

    def run(self):

        final_df = pd.DataFrame()
        postgres_actual_clients_info_storage = PostgresActualClientsInfoStorage()
        postgres_actual_clients_info_df = postgres_actual_clients_info_storage.get()
        postgres_actual_clients_info_df.set_index(standards_match_columns, inplace=True)
        actual_clients_info_df = postgres_actual_clients_info_df.loc[
            postgres_actual_clients_info_df.index.isin(
                set(self.dataset_for_actualization.set_index(standards_match_columns).index.tolist())
            )].reset_index()

        postgres_actual_clients_info_df.reset_index(inplace=True)

        for (cl, br, g), group in actual_clients_info_df.groupby(
                standards_match_columns):

            loc4combination = self.dataset_for_actualization.loc[
                (self.dataset_for_actualization.client == cl) &
                (self.dataset_for_actualization.breed_type == br) &
                (self.dataset_for_actualization.gender == g)]

            # Get density name by engine in engine configs
            actual_density_name = self.get_actual_density_name(group)
            combo_filter = self.generate_filter(cl, br, g)

            self.logger.info(f'work with combination: \n{combo_filter.str()}')

            # Generating of keys for s3 resources
            keys = self._generate_models_source_keys(actual_density_name)

            # Downloading model resources from s3
            density_model = self.load_model(keys["model_key_"])
            cvectors = self.load_c_vectors(keys["extra_features_key_"], combo_filter)
            feature_mask = self.load_feature_mask(keys["feature_mask_key_"])

            self.logger.info("model and sources are downloaded")

            # Check dataset has c_vector cols
            #    if True - change values with new_model's values
            #    if False - add columns and fill with new_model's values
            all_c_vector_cols_in_dataset = all(
                column in loc4combination.columns for column in cvectors.index)
            if not all_c_vector_cols_in_dataset:
                self.logger.warning('no c_vectors columns in input dataset. Adding...')
                for c_v_col in cvectors.index:
                    loc4combination[c_v_col] = round(cvectors.loc[cvectors.index == c_v_col][0][c_v_col], 6)
            else:
                loc4combination[cvectors.index] = cvectors

            # Get prediction from new model, rename columns
            rename_dict = {self.ColName.input_volume_column: self.ColName.models_volume_column}
            loc4combination.rename(columns=rename_dict, inplace=True)
            inp_features = check_inputs(loc4combination,
                                        model=density_model,
                                        inp_features=feature_mask)

            loc4combination.loc[:, self.ColName.predicted_density_column] = \
                density_model.model.predict(loc4combination[inp_features])

            loc4combination.rename(columns={
                self.ColName.default_density_column: f"old_{self.ColName.default_density_column}",
                self.ColName.predicted_density_column: self.ColName.default_density_column,
                self.ColName.default_mass_column: f"old_{self.ColName.default_mass_column}",
            }, inplace=True)

            # Calculate new mass | not centered
            print(f"{f' recalculating mass & error ':-^70}")
            loc4combination[self.ColName.default_mass_column] = \
                loc4combination[self.ColName.models_volume_column] * \
                loc4combination[self.ColName.default_density_column]

            # Estimate new error | not centered
            loc4combination[self.ColName.err_on_new_density_no_centering] = \
                (loc4combination[self.ColName.default_mass_column] /
                 loc4combination[self.ColName.target_w_column]) - 1

            self.logger.info("prediction is finished")

            if self.do_centering:
                centered_combo = self.center_dataset(loc4combination)
                final_df = pd.concat([final_df, centered_combo])
                # return centered_combo
            else:
                final_df = pd.concat([final_df, loc4combination])
                # return self.dataset_for_actualization
        return final_df


if __name__ == '__main__':
    dataset_fp = r'C:\Users\pawlin\Downloads\test_0108.csv'
    dataset = pd.read_csv(dataset_fp, sep=';')

    # Predict by actual model and centering predicted mass if you need to
    ma = MassActualization(dataset_for_actualization=dataset,
                           do_centering=True)
    act_mass_df = ma.run()
    print(act_mass_df)
