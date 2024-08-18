from vaultprovider.base import VaultProvider


class HashicorpVaultProvider(VaultProvider):

    type = "hashicorpprovider"

    def __init__(self, vault_url, vault_token):
        self.vault_url = vault_url
        self.vault_token = vault_token

    def get_secret(self, secret_key):
        # get secret from hashicorp vault
        pass
