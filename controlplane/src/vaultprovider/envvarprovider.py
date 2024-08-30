# Get vault from environment variables
import os
from vaultprovider.base import VaultProvider


class EnvVarVaultProvider(VaultProvider):

    type = "envvar"

    def __init__(self, vault_url, vault_token):
        self.secrets = os.environ

    def get_secret(self, secret_key):
        return self.secrets.get(secret_key)
