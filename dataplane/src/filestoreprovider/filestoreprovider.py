# Main for file store configuration
import configparser
import filestoreprovider.apiprovider as apiprovider
import filestoreprovider.gdriveprovider as gdriveprovider
import filestoreprovider.localfsprovider as localfsprovider
import filestoreprovider.s3provider as s3provider


class FileStoreProviderFactory:

    @staticmethod
    def get_provider(config: configparser.ConfigParser):
        if config["fileprovider"]["type"] == "localfs":
            _provider = localfsprovider.LocalFSProvider(
                required_directory=config["fileprovider"]["path"],
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
