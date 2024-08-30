# Main for vault provider configuration
import vaultprovider.envfileprovider as envfileprovider
import vaultprovider.envvarprovider as envvarprovider
import vaultprovider.hashicorpprovider as hashicorpprovider
import configparser


class VaultProviderFactory:

    @staticmethod
    def get_provider(config: configparser.ConfigParser):
        provider_type = config.get("vaultprovider", "type")
        if provider_type == "envfile":
            _provider = envfileprovider.EnvFileVaultProvider(
                config.get("vaultprovider", "path"),
                config.get("vaultprovider", "file"),
            )
            return _provider
        elif provider_type == "envvar":
            return envvarprovider.EnvVarProvider()
        elif provider_type == "hashicorp":
            return hashicorpprovider.HashiCorpProvider()
        else:
            return None
