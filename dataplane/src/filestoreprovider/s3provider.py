# Stores Files on S3
from filestoreprovider.base import FileStoreProvider
from streaming_form_data.targets import S3Target
import pandas as pd
import boto3
import magic
import io
import logging



class S3Provider(FileStoreProvider):
    type = "s3provider"

    def __init__(self, config: dict):
        super().__init__()
        self.required_provider_type = "s3"
        self.required_aws_key = config.get("fileprovider", "access_key_id")
        self.required_aws_secret = config.get   ("fileprovider", "secret_access_key")
        self.required_bucket = config.get("fileprovider", "bucket")
        self.required_region = config.get("fileprovider", "region")
        self.required_endpoint = config.get("fileprovider", "endpoint_url")
        if self.required_endpoint is not None:
            self.s3client = boto3.client(
                "s3",
                aws_access_key_id=self.required_aws_key,
                aws_secret_access_key=self.required_aws_secret,
                region_name=self.required_region,
                endpoint_url=self.required_endpoint,
            )
        else:
            self.s3client = boto3.client(
                "s3",
                aws_access_key_id=self.required_aws_key,
                aws_secret_access_key=self.required_aws_secret,
                region_name=self.required_region,
            )


    def Target(self, upload_id: str, file_id: str) -> S3Target:
        return S3Target(f"{self.required_bucket}/{upload_id}.{file_id}",
                        mode='wb',
                        transport_params={'client': self.s3client})        

    def put_file(self,
        file_id: str,
        upload_id: str,
        stream: io.StringIO,
        is_transformed: bool = True,):
        if is_transformed:
            transformed_extension = ".transformed"
        else:
            transformed_extension = ""
        
        file_name = f"{upload_id}.{file_id}{transformed_extension}"    
    
        try:
            self.s3client.upload_fileobj(io.BytesIO(stream.getvalue().encode("utf-8")),
                                  self.required_bucket.replace("s3://", ""),
                                  file_name
                                  )
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            raise Exception("Error uploading file")


    def get_file(self,
        file_id: str,
        upload_id: str,
        is_transformed: bool = False) -> pd.DataFrame:
        if is_transformed:
            transformed_extension = ".transformed"
        else:
            transformed_extension = ""
        file_stream = io.BytesIO()
        file_name = f"{upload_id}.{file_id}{transformed_extension}"
        try:
            self.s3client.download_fileobj(self.required_bucket.replace("s3://", ""),
                                    file_name,
                                    file_stream)
        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            raise Exception("Error downloading file")
        
        try:
            m = magic.from_buffer(file_stream.getvalue())
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            raise Exception("Error reading file")
        if m.find("CSV") >= 0:
            file_stream.seek(0)
            df = pd.read_csv(file_stream)
        elif m.find("Excel") >= 0 and m.find("OOXML") == -1:
            try:
                df = pd.read_excel(file_stream)
            except Exception as e:
                logging.error(
                    f"Error reading excel file: {e} File: {file_name}"
                )
                raise Exception("Error reading excel file")
        elif m.find("OOXML") >= 0:
            try:
                df = pd.read_excel(file_stream, engine="openpyxl")
            except Exception as e:
                logging.error(
                    f"Error reading excel(xlsx) file: {e} File: {file_name}"
                )
                raise Exception("Error reading excel(xlsx) file")
        else:
            raise Exception("File format not supported")

        return df
        
        