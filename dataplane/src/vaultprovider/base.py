class VaultProvider:

    def __init__(self, vault_url, vault_token):
        self.required_vault_url = vault_url
        self.required_vault_token = vault_token

    def load_secrets(self, secret_key):
        # Load secret from vault
        pass

    def get_secret(self, secret_key):
        # Get secret from vault
        pass

    def generate_config_yaml(self):
        # Configure vault provider
        pass
