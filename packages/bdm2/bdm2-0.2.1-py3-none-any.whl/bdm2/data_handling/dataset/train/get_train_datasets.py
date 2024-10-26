import io

import pandas as pd

from bdm2.constants.global_setup.env import AWS_ACCESS_KEY, AWS_SECRET_KEY
from bdm2.logger import build_logger
from bdm2.utils.s3.connector import S3Handler
from pathlib import Path


class TrainerDataset:
    conn_s3 = S3Handler(access_key=AWS_ACCESS_KEY,
                        secret_key=AWS_SECRET_KEY,
                        region_name="us-east-1")

    def __init__(self,
                 base_dataset_name: str):
        self.base_dataset_name: str = f"base-dataset/{base_dataset_name}"
        self.uploaded_base_dataset = None
        self.logger = build_logger(Path(__file__), save_log=False)

    def get_base_dataset(self):
        """
        allows to download base-dataset by fname
        """
        self.logger.info(f"started uploading {self.base_dataset_name} . . .")
        s3_datasets_root = self.conn_s3.root_bucket.Bucket("birdoo-datasets")
        dataset_obj = list(s3_datasets_root.objects.filter(Prefix=self.base_dataset_name))
        dataset_key = dataset_obj[0].key
        obj = s3_datasets_root.Object(dataset_key)
        response = obj.get()
        data = response['Body'].read()
        df = pd.read_csv(io.BytesIO(data), sep=";")
        df.rename(columns={"reliability_mean": "reliability"}, inplace=True)
        self.uploaded_base_dataset = df

    def filter_dataset(self):
        # todo get aprams
        self.logger.info(f"started filtering . . .")
        df = self.uploaded_base_dataset
        # by usable flag
        df = df[df.usable_for_train == True]
        # by na
        df.dropna(subset=['adjusted_weight'], inplace=True)
        # by count
        df = df[df["count"] >= 1000]

        self.uploaded_base_dataset = df

    def get_split_parts(self):
        self.logger.info(f"started splitting on test | train . . .")
        full_df = self.uploaded_base_dataset.copy()
        train_df = full_df[full_df.train_flag == 1]
        test_df = full_df[full_df.train_flag == 0]
        return {
            "full": full_df,
            "train": train_df,
            "test": test_df}

    def upload_to_s3(self, dict2upload):
        for dataset_k, dataset_v in dict2upload.items():
            csv_buffer = io.StringIO()
            dataset_v.to_csv(csv_buffer, index=False, sep=';')

            f_name = self.base_dataset_name.split("/")[1].replace(".csv", "")
            s3_file_path = f"train_datasets/{f_name}/{f_name}_{dataset_k}/collected_df.csv"

            s3_resource = self.conn_s3.get_s3_resource()
            s3_resource.Bucket("birdoo-datasets").put_object(
                Key=s3_file_path,
                Body=csv_buffer.getvalue(),
                ContentType='text/csv'
            )
            self.logger.info(f"File {s3_file_path} uploaded successfully.")

    def run(self):
        self.get_base_dataset()
        self.filter_dataset()
        splits_dict = self.get_split_parts()
        self.upload_to_s3(dict2upload=splits_dict)


if __name__ == '__main__':
    td = TrainerDataset(base_dataset_name="dataset_20241014_002507_default.csv")
    td.run()
