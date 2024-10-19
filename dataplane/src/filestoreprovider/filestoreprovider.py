# Main for file store configuration
import configparser
import filestoreprovider.apiprovider as apiprovider
import filestoreprovider.gdriveprovider as gdriveprovider
import filestoreprovider.localfsprovider as localfsprovider
import filestoreprovider.s3provider as s3provider
from vaultprovider.base import VaultProvider


class FileStoreProviderFactory:

    @staticmethod
    def get_provider(
        config: configparser.ConfigParser, vaultprovider: VaultProvider
    ):
        if config["fileprovider"]["type"] == "localfs":
            _provider = localfsprovider.LocalFSProvider(
                required_directory=config["fileprovider"]["path"],
            )
            return _provider
        elif config["fileprovider"]["type"] == "s3":
            _provider = s3provider.S3Provider(
                config=config
            )
            return _provider
        
        # elif provider == "gdrive":
        #     return gdriveprovider.GDriveProvider()
        # elif provider == "s3":
        #     return s3provider.S3Provider()
        # elif provider == "api":
        #     return apiprovider.ApiProvider()
        else:
            return None
