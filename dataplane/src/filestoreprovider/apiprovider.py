from filestoreprovider.base import FileStoreProvider
import requests


class APIProvider(FileStoreProvider):
    def __init__(self):
        super().__init__()
        self.required_provider = "api"
        self.required_provider_type = "API"
        self.required_url = "http://api.example.com"

    def put_file(self, file_name: str, file_data: str):
        url = f"{self.required_url}/put"
        response = requests.post(
            url, data={"file_name": file_name, "file_data": file_data}
        )
        if response.status_code != 200:
            raise Exception("Could not put file")

    def get_file(self, file_name: str):
        url = f"{self.required_url}/get"
        response = requests.post(url, data={"file_name": file_name})
        if response.status_code != 200:
            raise Exception("Could not get file")
        return response.text
