import pandas as pd
from streaming_form_data.targets import FileTarget


class FileStoreProvider:

    def __init__(self):
        self.provider = "localfs"
        self.provider_type = "File system"

    @property
    def Target(self, upload_id: str, file_id: str) -> FileTarget:
        filepath = ""
        return FileTarget(filepath)

    def provider_config(self):
        pass

    def put_file(self, file_name: str, file_data: str):
        pass

    def get_file(self, file_name: str) -> pd.DataFrame:
        pass
