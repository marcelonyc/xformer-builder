# Stores Files on S3
from filestoreprovider.base import FileStoreProvider
import pandas as pd


class S3Provider(FileStoreProvider):
    type = "s3provider"

    def __init__(self, provider, provider_type, bucket):
        super().__init__()
        self.required_provider = provider
        self.required_provider_type = provider_type
        self.required_aws_key = None
        self.required_aws_secret = None
        self.required_bucket = bucket

    def put_file(self, file_name: str, file_data: str):
        pass

    def get_file(self, file_name: str) -> pd.DataFrame:
        pass
