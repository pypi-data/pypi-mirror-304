import io

import pandas as pd

from bdm2.utils.dependency_checker import DependencyChecker

# required_modules = [
#     'boto3.Session',
# ]
#
# checker = DependencyChecker(required_modules)
# checker.check_dependencies()
#
# Session = checker.get_module('boto3.Session')

import boto3
class S3Handler:
    def __init__(self, access_key: str, secret_key: str, region_name: str, bucket: str = None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.region_name = region_name
        print(f"{'KNEX' if region_name[-1] == '2' else 'BIRDOO'} aws/s3 will be used")

    def get_s3_bucket(self) -> boto3.Session.resource:
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )
        return session.resource("s3").Bucket(self.bucket) if self.bucket else session.resource("s3")

    def get_s3_resource(self) -> boto3.resource:
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )
        return session.resource("s3")
    @property
    def root_bucket(self) -> boto3.Session.resource:
        return self.get_s3_bucket()

    # def upload_dataframe(self,
    #                      df: pd.DataFrame,
    #                      s3_file_path,
    #                      # folder_name: str,
    #                      # file_name: str
    #                      ):
    #     # Преобразуем DataFrame в CSV
    #     csv_buffer = io.StringIO()
    #     df.to_csv(csv_buffer, index=False)
    #
    #     # Создаем имя файла с учетом папки
    #     # s3_file_path = f"{folder_name}/{file_name}"
    #
    #     # Загружаем CSV в S3
    #     self.root_bucket.put_object(
    #         Key=s3_file_path,
    #         Body=csv_buffer.getvalue(),
    #         ContentType='text/csv'
    #     )
    #     print(f"File {s3_file_path} uploaded successfully.")
