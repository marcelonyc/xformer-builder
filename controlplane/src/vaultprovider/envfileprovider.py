# get vault from .env file
from vaultprovider.base import VaultProvider
from dotenv import load_dotenv, get_key
import os


class EnvFileVaultProvider(VaultProvider):

    type = "envfileprovider"

    def __init__(self, required_path, required_file_name):
        self.required_path = required_path
        self.required_file_name = required_file_name
        self.secrets = self.load_secrets()

    def load_secrets(self):
        return load_dotenv(
            os.path.join(self.required_path, self.required_file_name)
        )

    def get_secret(self, secret_key, default=None):
        _value = get_key(
            os.path.join(self.required_path, self.required_file_name),
            secret_key,
        )
        if _value:
            return _value
        else:
            return default
