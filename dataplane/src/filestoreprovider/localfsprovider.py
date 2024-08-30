# Stores file in a local fiel system
from filestoreprovider.base import FileStoreProvider
import os
from typing import Annotated
import pandas as pd
from streaming_form_data.targets import FileTarget
import io
import magic
import logging


class LocalFSProvider(FileStoreProvider):

    type = "localfs"

    def __init__(
        self,
        required_directory: Annotated[str, "Directory to store files"],
    ):
        super().__init__()
        self.required_directory = required_directory
        self._create_directory()

    def _create_directory(self):
        if not os.path.exists(self.required_directory):
            os.makedirs(self.required_directory)

    def Target(self, upload_id: str, file_id: str) -> FileTarget:
        filepath = os.path.join(
            self.required_directory,
            f"{upload_id}.{file_id}",
        )
        return FileTarget(filepath)

    def _file_object(self, file_name):
        return os.path.join(self.required_directory, file_name)

    def put_file(
        self,
        file_id: str,
        upload_id: str,
        stream: io.StringIO,
        is_transformed: bool = True,
    ):
        if is_transformed:
            transformed_extension = ".transformed"
        else:
            transformed_extension = ""
        filepath = os.path.join(
            self.required_directory,
            f"{upload_id}.{file_id}{transformed_extension}",
        )
        f = open(filepath, "wb")
        f.write(stream.getvalue().encode("utf-8"))
        f.close()

    def get_file(
        self,
        file_id: str,
        upload_id: str,
        is_transformed: bool = False,
    ) -> pd.DataFrame:
        if is_transformed:
            transformed_extension = ".transformed"
        else:
            transformed_extension = ""
        filepath = os.path.join(
            self.required_directory,
            f"{upload_id}.{file_id}{transformed_extension}",
        )
        try:
            m = magic.from_file(filepath)
        except FileNotFoundError as e:
            raise Exception("Error reading file")

        if m.find("CSV") >= 0:
            df = pd.read_csv(filepath)
        elif m.find("Excel") >= 0 and m.find("OOXML") == -1:
            try:
                df = pd.read_excel(filepath)
            except Exception as e:
                logging.error(
                    f"Error reading excel file: {e} File: {filepath}"
                )
        elif m.find("OOXML") >= 0:
            try:
                df = pd.read_excel(filepath, engine="openpyxl")
            except Exception as e:
                logging.error(
                    f"Error reading excel(xlsx) file: {e} File: {filepath}"
                )
        else:
            raise Exception("File format not supported")

        return df

    def delete_file(self, file_id: str, upload_id: str):

        filepath = os.path.join(
            self.required_directory,
            f"{upload_id}.{file_id}",
        )
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass

        filepath = os.path.join(
            self.required_directory,
            f"{upload_id}.{file_id}.transformed",
        )
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass
